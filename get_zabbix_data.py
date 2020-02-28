#!/usr/bin/env python2

import sys
import configparser
import time
import datetime
import pprint
from zabbix_methods import ZabbixConnection

NUMERIC_FLOAT = 0
CHARACTER = 1
LOG = 2
NUMERIC_UNSIGNED = 3
TEXT = 4

def main():
    config = configparser.ConfigParser()
    config_file = "/home/naved/zabbix-usage/config.ini"
    config.read(config_file)

    USER = config['general']['API_USER']
    PASSWORD = config['general']['PASSWORD']
    ZABBIX_SERVER = config['general']['ZABBIX_SERVER']

    host_name = sys.argv[1] # Specify VM UUID as first arg

    # This list does not include DISK and NIC stats (those are a bit more complex to get)
    # Also it's quite weird that I have to tell the data type of the metric, shouldn't it already know that?
    item_keys = [("libvirt.cpu[cpu_time]", NUMERIC_UNSIGNED), # CPU time (stright from libvirt API)
                 ("libvirt.cpup[cpu_time]", NUMERIC_FLOAT),  # percentage CPU utilization (calculated in zabbix)
                 ("libvirt.cpu[core_count]", NUMERIC_UNSIGNED),
                 ("libvirt.memory[available]", NUMERIC_UNSIGNED),
                 ("libvirt.memory[current_allocation]", NUMERIC_UNSIGNED),
                 ("libvirt.memory[free]", NUMERIC_UNSIGNED),
                 ("libvirt.instance[project_name]", CHARACTER),
                 ("libvirt.instance[project_uuid]", CHARACTER),
                 ("libvirt.instance[user_uuid]", CHARACTER),
                 ("libvirt.instance[user_name]",  CHARACTER)]

    with ZabbixConnection(USER, "https://" + ZABBIX_SERVER, PASSWORD) as zabbix_api:
        host_id = zabbix_api.get_host_id(host_name)
        time_till = int(time.time()) # epoch_time
        # time_till = datetime.datetime(2019, 2, 27, 1, 0).strftime('%s')
        time_from = datetime.datetime(2019, 2, 26, 0, 0).strftime('%s')
        for item_key in item_keys:
            value = zabbix_api.get_history(host_id, item_key[0], item_type=item_key[1], limit=3, time_from=time_from, time_till=time_till)
            print(item_key[0])
            pprint.pprint(value)

if __name__ == "__main__":
    if len(sys.argv) != 2: 
        sys.exit("Not enough args")
    main()
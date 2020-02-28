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
    config_file = "/home/naved/zabbix-playground/config.ini"
    config.read(config_file)

    USER = config['general']['API_USER']
    PASSWORD = config['general']['PASSWORD']
    ZABBIX_SERVER = config['general']['ZABBIX_SERVER']

    # This list does not include DISK and NIC stats (those are a bit more complex to get)
    # Also it's quite weird that I have to tell the data type of the metric, shouldn't it already know that?
    item_keys = [("libvirt.cpup[cpu_time]", NUMERIC_FLOAT),  # percentage CPU utilization (calculated in zabbix)
                 ("libvirt.cpu[core_count]", NUMERIC_UNSIGNED),
                 ("libvirt.memory[current_allocation]", NUMERIC_UNSIGNED)]

    time_till = int(time.time())  # epoch_time
    time_from = datetime.datetime(2019, 2, 1, 0, 0).strftime('%s')

    with ZabbixConnection(USER, "https://" + ZABBIX_SERVER, PASSWORD) as zabbix_api:
        hosts = zabbix_api.get_hosts()
        import pdb
        pdb.set_trace()
        output = {}

        for host in hosts:
            metrics = {}
            for item_key in item_keys:
                value = zabbix_api.get_history(
                    host[1], item_key[0], item_type=item_key[1], limit=30000, time_from=time_from, time_till=time_till)
                metrics[item_key[0]] = value
            output[host[0]] = metrics


if __name__ == "__main__":
    main()

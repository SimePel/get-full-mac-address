#!/usr/bin/python
from netmiko import Netmiko
import sys
import os

def get_full_mac() -> str:
    campus_switches = {"m": "sw-102-0-mc.noc.asu.ru", "l": "sw-104-1-lc.noc.asu.ru",
                       "d": "sw-024-1-dc.noc.asu.ru", "s": "sw-102-1-sc.noc.asu.ru",
                       "k": "sw-403-1-kc.noc.asu.ru"}

    switch = campus_switches["m"]
    if len(sys.argv) == 3:
        switch = campus_switches[sys.argv[2]]
    if len(sys.argv) == 1:
        print("./mac.py [short mac] [letter of campus(m,l,d,s,k)]")
        sys.exit(1)

    cisco = Netmiko(
        switch,
        username=os.getenv("CISCO_LOGIN"),
        password=os.getenv("CISCO_PASS"),
        device_type="cisco_ios",
    )

    mac = sys.argv[1]
    output = cisco.send_command('show mac address-table | include ' + mac)
    if output == '':
        return 'Мак адрес не найден'

    return output.split()[1]

if __name__ == "__main__":
    print(get_full_mac())

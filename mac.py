import sys
import os

import paramiko

def get_full_mac() -> str:
    username = os.getenv("CISCO_LOGIN")
    password = os.getenv("CISCO_PASS")
    campus_switches = {"m" : "sw-102-0-mc.noc.asu.ru", "l" : "sw-104-1-lc.noc.asu.ru",
                    "d" : "sw-024-1-dc.noc.asu.ru", "s" : "sw-102-1-sc.noc.asu.ru",
                    "k" : "sw-403-1-kc.noc.asu.ru"}

    if len(sys.argv) != 3:
        print("python3 mac.py [short mac] [letter of campus(m,l,d,s,k)]")
        sys.exit(1)

    mac = sys.argv[1]
    switch = campus_switches[sys.argv[2]]

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    client.connect(hostname=switch, username=username, password=password, allow_agent=False, look_for_keys=False)
    _, stdout, _ = client.exec_command('show mac address-table | include ' + mac)
    data = str(stdout.read())
    rindex = data.rfind(mac)
    
    return data[rindex-10:rindex+4]

if __name__ == "__main__":
    print(get_full_mac())

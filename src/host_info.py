
#
# Dump host system information
#
# Thanks to:
#   https://www.geeksforgeeks.org/get-your-system-information-using-python-script/
#

import subprocess
import pandas as pd
import sys
from io import StringIO


def host_info_brief():
    keep = [
        "OS Name",
        "OS Version",
        "System Manufacturer",
        "System Model",
        "System Type",
    #    "Processor(s)",
        "Total Physical Memory"
    ]

    sysinfo_text = subprocess.check_output(['systeminfo', '/fo', 'csv']).decode('utf-8')
    host_info = pd.read_csv(StringIO(sysinfo_text), usecols=keep).to_string(index=False)

    return host_info


def host_info_all():
    sysinfo_text = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')

    host_info = []     
    for item in sysinfo_text:
        host_info.append(str(item.split("\r")[:-1]))

    return host_info


if __name__ == '__main__':

    print('\nGet information about this host...\n')

    choice = input('\n\nChoose \'brief\' or \'all\' host information: ').lower()

    if choice == 'brief':
        print('\n', host_info_brief())

    elif choice == 'all':
        for i in host_info_all():
            print(i[2:-2])

    else:
        sys.exit()

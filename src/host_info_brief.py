
# Better host information report

import subprocess
import pandas as pd
from io import StringIO

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
sysinfo_df = pd.read_csv(StringIO(sysinfo_text), usecols=keep)

print('\n', sysinfo_df)

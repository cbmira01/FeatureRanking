
# Dump host system information
#
# Thanks to:
#   https://www.geeksforgeeks.org/get-your-system-information-using-python-script/

import subprocess
 
id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
new = []
 
for item in id:
    new.append(str(item.split("\r")[:-1]))

for i in new:
    print(i[2:-2])

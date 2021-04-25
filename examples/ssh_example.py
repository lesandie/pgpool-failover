# The main difference is that subprocess.run executes a command and waits for it to finish, 
# while with subprocess.Popen you can continue doing your stuff while the process finishes 
# and then just repeatedly call subprocess.communicate yourself to pass and receive data 
# to your process
# stdout and stderr attributes are of binary form. Therefore result needs to be decoded().

import subprocess
result = subprocess.run(["ssh", "root@xx.xx.xx.xx", "python3 -v"],
                        shell=False,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        check=False)
print(result.stdout.decode())
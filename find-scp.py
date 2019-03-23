import os
import paramiko

# required variables
save     = ''                         # if left empty will copy to current dir
user     = 'user01'                   # username - required
passwrd  = 'zxczxc'                   # password - required
remote   = 'remote.computer.org.au'   # remote computer - required

# user input
rem_fol  = input("Remote folder: ")                       # folder to get files from in remote location
file_typ = input("File types to download (eg xyz): ")     # file types, separate by spaces
parntfol = rem_fol.rsplit('/', 1)[1]

# command to find recursively all of file types
cmd = 'find ' + rem_fol + ' -type f -name'

# append file types to find command
file_typ = file_typ.split()
for i, typ in enumerate(file_typ):
    typ = " *" + typ
    if i == 0:
        cmd = cmd + typ
    else:
        cmd = cmd + ' -o -name' + typ

# ssh client open
# ------------------------------

ssh = paramiko.SSHClient()
ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(remote, username=user, password=passwrd)
sftp = ssh.open_sftp()

stdin, stdout, stderr = ssh.exec_command(cmd)
paths = stdout.read().decode(encoding='UTF-8').split('\n')
print(paths)

new_paths = []

for path in paths:
    # MAY CONTAIN EMPTY STR
    if path != '':
        # REMOVE FILE NAME - FULL PATH TO FILE
        root2f, Filename   = path.rsplit('/', 1)
        # REMOVE PRECEEDING FOLDERS FROM SAVE PLACE
        shrtroot = parntfol + '/' + root2f.replace(rjn_fol, '')
        print('shrtroot', shrtroot)
        print('Remote path :', root2f)
        print('Make path   :', save + shrtroot)
        if not os.path.exists(save + shrtroot):
            os.makedirs(save + shrtroot)
        print(path)
        sftp.get(path, save + shrtroot + '/' + Filename)
sftp.close()
ssh.close()

# ------------------------------

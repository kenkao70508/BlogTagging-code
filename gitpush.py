import os, pexpect, time

os.system('git add .')
os.system('git commit -m "update"')
child = pexpect.spawn('git push')
child.expect('Username for "https://github.com"')
child.sendline(kenkao70508)
import os, pexpect, time

os.system('git add .')
os.system('git commit -m "update"')
os.system('git push')
time.sleep(5)
os.system('kenkao70508')
time.sleep(3)
os.system('nw344556')
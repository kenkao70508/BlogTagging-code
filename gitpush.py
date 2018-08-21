import os, pexpect, time

child = pexpect.spawn('ssh kenkao70508@cl5.learner.csie.ntu.edu.tw')
child.expect("kenkao70508@cl5.learner.csie.ntu.edu.tw\'s password: ")
child.sendline("miulab")
child.sendline("ls")
print(child.after)

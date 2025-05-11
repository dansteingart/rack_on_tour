from subprocess import getoutput as go
from time import sleep

while True:
    foo = go("python3 vtt_get.py")
    foo = go("python3 vtt_inspect.py")
    foo = go("python3 vtt_analysis.py")
    sleep(60)

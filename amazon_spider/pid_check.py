# coding: utf-8
#!/usr/bin/python3

"""
爬虫程序运行自检
@Author ：Patrick Lam
@Date ：2023-02-13
"""
import win32event
import win32api
import time
import sys

if __name__ == '__main__':
    mutex = win32event.CreateMutex(None, False, 'program_name')
    if win32api.GetLastError() > 0:
        print('程序已运行...')
        sys.exit(0)
    while True:
        time.sleep(1)
        print("running")

# import os
# import psutil
# import time
#
# def write_pid():
#     pid = os.getpid()
#     fp = open("pid.log", 'w')
#     fp.write(str(pid))
#     fp.close()
#
# def read_pid():
#     if os.path.exists("pid.log"):
#         fp = open("pid.log", 'r')
#         pid = fp.read()
#         fp.close()
#         return pid
#     else:
#         return False
#
# def write_log(log_content):
#     time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     log_content = time_now+"---->"+log_content+os.linesep
#     fp = open('recognition.log','a+')
#     fp.write(log_content)
#     fp.close()
#
# def run():
#     pid = read_pid()
#     #print pid
#     pid = int(pid)
#     if pid:
#         running_pid = psutil.pids()
#         if pid in running_pid:
#             log_content =  "process is running..."
#             write_log(log_content)
#         else:
#             write_pid()
#             time.sleep(20)
#     else:
#         write_pid()
#         time.sleep(20)
#
# if __name__ == "__main__":
#     run()
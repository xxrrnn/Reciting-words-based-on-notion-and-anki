import multiprocessing
import time
import os
import signal
import random

# 定义需要上传数据的函数
def upload_data():
    # 这里模拟一个可能会出现卡顿的操作，可以替换为实际的上传数据操作
    a = 0
    print(a)
    if a < 1:
        time.sleep(15)  # 模拟上传数据耗时15秒
    else:
        time.sleep(5)

# 定义一个函数来执行上传数据并检查是否超时
def run_upload_with_timeout():
    while True:
        upload_process = multiprocessing.Process(target=upload_data)
        upload_process.start()
        upload_process.join(timeout=10)  # 主进程等待上传进程最多10秒

        if not upload_process.is_alive():
            break  # 如果上传进程已完成，退出循环
        else:
            print("函数执行时间超过10秒，停止当前进程并重新执行程序")
            os.kill(upload_process.pid, signal.SIGTERM)  # 终止上传进程

if __name__ == "__main__":
    run_upload_with_timeout()  # 执行上传数据函数
    print("继续执行后续程序")

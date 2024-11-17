import os
import multiprocessing
import time
import signal
import sys

# 子プロセスで実行する処理A
def process_a():
    try:
        ## @todo 下記を子プロセスで実行したいスクリプトに置き換える。
        while True:
            print(f"子プロセスA (PID {os.getpid()}): 実行中...")
            time.sleep(1)
    except KeyboardInterrupt:
        print(f"子プロセスA (PID {os.getpid()}): 終了します")
        sys.exit()

# 親プロセス終了時に子プロセスを終了させる処理
def terminate_processes(processes):
    for p in processes:
        if p.is_alive():
            print(f"子プロセス (PID {p.pid}): を終了します")
            p.terminate()
            p.join()

if __name__ == "__main__":
    child_process = multiprocessing.Process(target=process_a)

    # 終了時のクリーンアップ設定
    def cleanup(signum, frame):
        print(f"親プロセス (PID {os.getpid()}): 終了処理を開始します")
        terminate_processes([child_process])
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)  # Ctrl+C（SIGINT）でクリーンアップ
    signal.signal(signal.SIGTERM, cleanup)  # 外部からの終了シグナルでクリーンアップ

    child_process.start()

    try:
        # @todo 下記を親プロセスで実行したいスクリプトにする。
        while True:
            print(f"親プロセス (PID {os.getpid()}): 実行中...")
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup(None, None)

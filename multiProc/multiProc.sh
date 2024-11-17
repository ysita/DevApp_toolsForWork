#!/bin/bash

# 子プロセスで実行する処理A
process_a() {
    while true; do
        echo "子プロセスA (PID $!): 実行中..."
        sleep 1
    done
}

# 親プロセス終了時に子プロセスを終了させる処理
cleanup() {
    echo "親プロセス (PID $$): 終了処理を開始します"
    if [[ -n "$CHILD_PID" ]]; then
        echo "子プロセス (PID $CHILD_PID): を終了します"
        kill "$CHILD_PID" 2>/dev/null
        wait "$CHILD_PID" 2>/dev/null
    fi
    exit 0
}

# シグナルハンドリングの設定
trap "cleanup" SIGINT SIGTERM

# 子プロセスを起動
(process_a) &
CHILD_PID=$!

# 親プロセスで実行する処理B
while true; do
    echo "親プロセス (PID $$): 実行中..."
    sleep 1
done

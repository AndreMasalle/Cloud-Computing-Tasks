import zmq
import sys
import time
from common import DataToWorker, PORT_DISTRIBUTOR, PORT_WORKER_1, PORT_WORKER_2

def run_worker(worker_id=None):
    if not worker_id and len(sys.argv) > 1:
        worker_id = sys.argv[1].strip()

    if not worker_id:
        worker_id = "1"

    if str(worker_id) == "1":
        worker_name = "Worker #1"
        push_port = PORT_WORKER_1  # 9933 (Binded)
    elif str(worker_id) == "2":
        worker_name = "Worker #2"
        push_port = PORT_WORKER_2  # 9932 (Binded)
    else:
        print(f"[Error] Pilihan worker '{worker_id}' tidak valid. Gunakan '1' atau '2'.")
        sys.exit(1)

    context = zmq.Context()

    # 1. Soket PULL: Connect ke Distributor port 9921
    pull_socket = context.socket(zmq.PULL)
    pull_endpoint = f"tcp://localhost:{PORT_DISTRIBUTOR}"
    pull_socket.connect(pull_endpoint)

    # 2. Soket PUSH: Bind ke port masing-masing worker (9933 untuk Worker 1, 9932 untuk Worker 2)
    push_socket = context.socket(zmq.PUSH)
    push_endpoint = f"tcp://*:{push_port}"
    push_socket.bind(push_endpoint)

    print("=" * 65, flush=True)
    print(f"      ZMQ WORKER NODE: {worker_name}       ", flush=True)
    print("=" * 65, flush=True)
    print(f"[{worker_name}] PULL Socket: Terhubung ke Distributor di {pull_endpoint}", flush=True)
    print(f"[{worker_name}] PUSH Socket: Terikat (Bind) untuk Collector di {push_endpoint}", flush=True)
    print(f"[{worker_name}] Menunggu tugas penjumlahan dari Distributor...\n", flush=True)

    task_count = 0
    try:
        while True:
            # Terima data biner serialisasi pickle dari Distributor
            payload_bytes = pull_socket.recv()
            task_data = DataToWorker.deserialize(payload_bytes)
            task_count += 1

            num1 = task_data.num1
            num2 = task_data.num2
            result = num1 + num2

            print(f"[{worker_name}] [TUGAS DITERIMA #{task_count}] Menghitung: {num1} + {num2}", flush=True)

            # Simulasi sedikit waktu komputasi
            time.sleep(0.3)

            # Perbarui properti objek data
            task_data.set_result(result)
            task_data.set_executor(worker_name)
            task_data.set_message(f"Operasi penjumlahan {num1} + {num2} = {result} berhasil dieksekusi.")

            # Kirim objek yang telah diperbarui ke Tasks Collector via soket PUSH
            push_socket.send(task_data.serialize())
            print(f"[{worker_name} -> PUSH] Hasil dikirim ke Collector (Port {push_port}): {result}\n", flush=True)

    except KeyboardInterrupt:
        print(f"\n[{worker_name}] Menghentikan worker.", flush=True)
    finally:
        pull_socket.close()
        push_socket.close()
        context.term()

if __name__ == "__main__":
    run_worker()

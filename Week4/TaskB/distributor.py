import zmq
import time
import random
from common import DataToWorker, PORT_DISTRIBUTOR

def run_distributor(total_tasks=10):
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    
    # BIND ke socket port 9921 sesuai diagram soal
    endpoint = f"tcp://*:{PORT_DISTRIBUTOR}"
    socket.bind(endpoint)

    print("=" * 65, flush=True)
    print(f"      ZMQ TASKS DISTRIBUTOR - TASK B (PORT {PORT_DISTRIBUTOR})       ", flush=True)
    print("=" * 65, flush=True)
    print(f"[Distributor] Soket PUSH terikat ke {endpoint}", flush=True)
    print("[Distributor] Menunggu worker terhubung (sleep 2 detik)...", flush=True)
    time.sleep(2)

    print(f"[Distributor] Memulai pendistribusian {total_tasks} tugas penjumlahan secara Round-Robin...\n", flush=True)

    task_id = 1
    try:
        while task_id <= total_tasks:
            # 1. Bangkitkan 2 bilangan bulat acak
            x = random.randint(1, 100)
            y = random.randint(1, 100)

            # 2. Bungkus ke objek data DataToWorker
            task_data = DataToWorker(num1=x, num2=y, operation="sum")
            serialized_payload = task_data.serialize()

            # 3. Kirim ke worker melalui soket PUSH
            print(f"[Distributor -> PUSH] Mengirim Tugas #{task_id:02d}: {x} + {y} (menunggu worker yang siap)...", flush=True)
            socket.send(serialized_payload)
            print(f"[Distributor -> PUSH] Tugas #{task_id:02d} BERHASIL terkirim!", flush=True)

            task_id += 1
            time.sleep(1.2)

        print("\n" + "=" * 65, flush=True)
        print(f"[Distributor] Seluruh {total_tasks} tugas telah selesai didistribusikan.", flush=True)
        print("=" * 65, flush=True)

    except KeyboardInterrupt:
        print("\n[Distributor] Dihentikan oleh pengguna.", flush=True)
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    run_distributor()

import zmq
from common import DataToWorker, PORT_WORKER_1, PORT_WORKER_2

def run_collector():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)

    # CONNECT ke kedua port worker (9933 & 9932) sesuai diagram soal
    endpoint_w1 = f"tcp://localhost:{PORT_WORKER_1}"
    endpoint_w2 = f"tcp://localhost:{PORT_WORKER_2}"

    pull_socket.connect(endpoint_w1)
    pull_socket.connect(endpoint_w2)

    print("=" * 65, flush=True)
    print("      ZMQ TASKS COLLECTOR - TASK B       ", flush=True)
    print("=" * 65, flush=True)
    print(f"[Collector] PULL Socket 1: Terhubung ke Worker #1 di {endpoint_w1}", flush=True)
    print(f"[Collector] PULL Socket 2: Terhubung ke Worker #2 di {endpoint_w2}", flush=True)
    print("[Collector] Menunggu hasil komputasi dari para worker...\n", flush=True)

    collected_count = 0
    try:
        while True:
            # Terima hasil komputasi yang siap dari worker mana pun (fair-queueing otomatis oleh ZMQ)
            payload_bytes = pull_socket.recv()
            task_result = DataToWorker.deserialize(payload_bytes)
            collected_count += 1

            executor = task_result.exe
            num1 = task_result.num1
            num2 = task_result.num2
            result = task_result.result
            msg = task_result.message

            print(f"[Collector] [HASIL #{collected_count:02d} DITERIMA]")
            print(f"  * Sumber Eksekutor : {executor}")
            print(f"  * Operasi          : {num1} + {num2} = {result}")
            print(f"  * Pesan Status     : {msg}")
            print("-" * 65, flush=True)

    except KeyboardInterrupt:
        print("\n[Collector] Menghentikan collector.", flush=True)
    finally:
        pull_socket.close()
        context.term()

if __name__ == "__main__":
    run_collector()

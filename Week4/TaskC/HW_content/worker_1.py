import pickle
import time
import main_constants as mc
from data_worker import DataToWorker
import zmq
import random

def calculate(task_data: DataToWorker):
    if task_data.op == mc.SUM:
        return task_data.num1 + task_data.num2
    if task_data.op == mc.MUT:
        return task_data.num1 * task_data.num2
    if task_data.op == mc.DIV:
        return task_data.num1 / task_data.num2
    raise ValueError(f"Unsupported operation: {task_data.op}")


def run_worker():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(f"tcp://{mc.DISTRIBUTOR_HOST}:{mc.DISTRIBUTOR_PORT}")
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind(f"tcp://*:{mc.WORKER_1_PORT}")
    print(f"[{mc.WORKER_1}] Waiting for tasks", flush=True)

    task_count = 0
    try:
        while True:
            task_data: DataToWorker = pickle.loads(pull_socket.recv())
            task_count += 1
            print(
                f"[{mc.WORKER_1}] Received {task_data.op.upper()}: "
                f"{task_data.num1}, {task_data.num2}",
                flush=True,
            )
            time.sleep(random.uniform(0.5, 1))
            result = calculate(task_data)
            task_data.set_result(result)
            task_data.set_executor(mc.WORKER_1)
            task_data.set_message(
                f"{task_data.op.upper()} completed by {mc.WORKER_1}"
            )
            push_socket.send(pickle.dumps(task_data))
            print(f"[{mc.WORKER_1} -> Collector] Result: {result}", flush=True)
    except KeyboardInterrupt:
        print(f"[{mc.WORKER_1}] Stopped", flush=True)
    finally:
        pull_socket.close(linger=0)
        push_socket.close(linger=0)
        context.term()


if __name__ == "__main__":
    run_worker()

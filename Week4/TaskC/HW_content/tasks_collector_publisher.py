import zmq
import pickle
from data_worker import DataToWorker
import main_constants as mc
import time

def topic_for_operation(operation: str) -> str:
    topics = {
        mc.SUM: mc.TOPIC_SUM,
        mc.MUT: mc.TOPIC_MUT,
        mc.DIV: mc.TOPIC_DIV,
    }
    try:
        return topics[operation]
    except KeyError as error:
        raise ValueError(f"Unsupported operation: {operation}") from error


def run_collector_publisher():
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.connect(f"tcp://{mc.WORKER_1_HOST}:{mc.WORKER_1_PORT}")
    pull_socket.connect(f"tcp://{mc.WORKER_2_HOST}:{mc.WORKER_2_PORT}")

    publisher = context.socket(zmq.PUB)
    publisher.bind(f"tcp://*:{mc.PUBLISHER_PORT}")
    print("Tasks collector is receiving results and publishing SUM/MUT/DIV", flush=True)

    try:
        while True:
            result: DataToWorker = pickle.loads(pull_socket.recv())
            topic = topic_for_operation(result.op)
            result.set_message(f"{topic} result published by {result.exe}")
            print(
                f"[Collector] Received from {result.exe}: {result.num1} "
                f"{result.op} {result.num2} = {result.result}",
                flush=True,
            )
            publisher.send_multipart([topic.encode("utf-8"), pickle.dumps(result)])
            print(f"[Collector -> PUB] Published on {topic}", flush=True)
    except KeyboardInterrupt:
        print("[Collector] Stopped", flush=True)
    finally:
        pull_socket.close(linger=0)
        publisher.close(linger=0)
        context.term()


if __name__ == "__main__":
    run_collector_publisher()
    


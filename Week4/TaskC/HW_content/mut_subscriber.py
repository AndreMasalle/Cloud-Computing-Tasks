import pickle
import zmq

import main_constants as mc
from data_worker import DataToWorker


def run_subscriber():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.setsockopt_string(zmq.SUBSCRIBE, mc.TOPIC_MUT)
    subscriber.connect(f"tcp://{mc.PUBLISHER_HOST}:{mc.PUBLISHER_PORT}")
    print(f"[MUT subscriber] Listening for {mc.TOPIC_MUT}", flush=True)
    try:
        while True:
            topic, payload = subscriber.recv_multipart()
            result: DataToWorker = pickle.loads(payload)
            print(
                f"[{topic.decode()} subscriber] {result.num1} * {result.num2} "
                f"= {result.result}; {result.message}; executor={result.exe}",
                flush=True,
            )
    except KeyboardInterrupt:
        print("[MUT subscriber] Stopped", flush=True)
    finally:
        subscriber.close(linger=0)
        context.term()


if __name__ == "__main__":
    run_subscriber()

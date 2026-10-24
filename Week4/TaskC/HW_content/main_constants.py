import os

SUM: str = "sum"
DIV: str = "div"
MUT: str = "mut"

TOPIC_SUM: str = "SUM"
TOPIC_MUT: str = "MUT"
TOPIC_DIV: str = "DIV"

DISTRIBUTOR_PORT: str = "5555"
WORKER_1_PORT: str = "5556"
WORKER_2_PORT: str = "5557"
PUBLISHER_PORT: str = "5558"

DISTRIBUTOR_HOST: str = os.getenv("DISTRIBUTOR_HOST", "127.0.0.1")
WORKER_1_HOST: str = os.getenv("WORKER_1_HOST", "127.0.0.1")
WORKER_2_HOST: str = os.getenv("WORKER_2_HOST", "127.0.0.1")
PUBLISHER_HOST: str = os.getenv("PUBLISHER_HOST", "127.0.0.1")

WORKER_1: str = "WORKER #1"
WORKER_2: str = "WORKER #2"

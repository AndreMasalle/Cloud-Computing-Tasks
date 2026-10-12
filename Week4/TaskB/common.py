import pickle

# Konfigurasi Port Jaringan Sesuai Diagram Soal Task B
PORT_DISTRIBUTOR = "9921"
PORT_WORKER_1 = "9933"
PORT_WORKER_2 = "9932"

class DataToWorker:
    """
    Kelas data representasi tugas komputasi antar-proses.
    Diserialisasi menggunakan pustaka pickle untuk transmisi melalui soket ZeroMQ.
    """
    def __init__(self, num1: int, num2: int, operation: str = "sum"):
        self.num1 = int(num1)
        self.num2 = int(num2)
        self.op = str(operation)
        self.result = 0
        self.message = ""
        self.exe = ""

    def set_result(self, res: float):
        self.result = res

    def set_executor(self, exe: str):
        self.exe = exe

    def set_message(self, message: str):
        self.message = message

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    @staticmethod
    def deserialize(data_bytes: bytes) -> "DataToWorker":
        return pickle.loads(data_bytes)

    def __repr__(self) -> str:
        return (f"DataToWorker(num1={self.num1}, num2={self.num2}, op='{self.op}', "
                f"result={self.result}, exe='{self.exe}', message='{self.message}')")

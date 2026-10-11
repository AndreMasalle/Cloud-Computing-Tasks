class DataToWorker:
    def __init__(self, num1: int, num2: int, operation: str):
        self.num1 = num1
        self.num2 = num2
        self.op = operation
        self.result = 0
        self.message = ""
        self.exe = ""

    def set_result(self, res: float):
        self.result = res

    def set_executor(self, exe: str):
        self.exe = exe

    def set_message(self, message: str):
        self.message = message

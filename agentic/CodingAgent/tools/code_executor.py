import subprocess

class CodeExecutor:
    def __init__(self, code, n_retry):
        self.code = code
        self.n_retry = n_retry

    def code_executor(self):
        while self.n_retry > 0:
            try:
                return subprocess.run(self.code)
            except Exception as e:
                subprocess.run(self.code)
import subprocess

class CheckHost():
    def __init__(self, host):
        self.host = host
    
    def check(self):
        STATUS_HOST = 0
        try:
            output = subprocess.check_output(
                ["ping", "-c", "1", self.host],  # Для Linux/Mac
                # ["ping", "-n", "1", host],  # Для Windows
                stderr=subprocess.STDOUT,
                universal_newlines=1
            )
            STATUS_HOST = True
            return STATUS_HOST
            #print(output)  # Полный вывод ping
        except subprocess.CalledProcessError:
            STATUS_HOST = 0
            return STATUS_HOST
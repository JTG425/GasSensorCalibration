import random

class randomInputGen():
    def __init__(self):
        self.data = open("data.txt", "w")
        current = 0
        for i in range(100):
            increase = random.uniform(0.5, 1.5)
            self.data.write(str(current + increase) + "\n")
            current = current + increase
        self.data.close()
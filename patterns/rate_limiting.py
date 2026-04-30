import time 

class TokenBucket:
    def __init__(self, rate, capacity):
        self.rate = rate # tokens added per second 
        self.capacity = capacity # maximum tokens bucket can hold (burst limit)
        self.tokens = capacity
        self.last_refill = time.time()


    def refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        added = elapsed * self.rate
        self.tokens = min(self.capacity, self.tokens + added)
        self.last_refill = now

    def acquire(self, tokens = 1):
        self.refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False
    
    def wait_and_acquire(self):
        while not self.acquire():
            time.sleep(0.5)
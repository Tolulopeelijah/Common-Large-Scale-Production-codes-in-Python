import time

OPEN = 'open'
CLOSED = 'closed'
HALF_OPEN = 'half_open'

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.state = CLOSED
        self.opened_at = None

    def call(self, func, *args, **kwargs):
        if self.state == OPEN:
            if time.time() - self.opened_at >= self.recovery_timeout:
                self.state = HALF_OPEN
            else:
                raise Exception(f"Circuit is OPEN — service unavailable, retry after {self.recovery_timeout}s")

        try:
            result = func(*args, **kwargs)
            if self.state == HALF_OPEN:
                self.failure_count = 0
                self.state = CLOSED     # probe succeeded, fully recover
            return result

        except Exception:
            if self.state == HALF_OPEN:
                self.state = OPEN       # flaky recovery — trip back immediately
                self.opened_at = time.time()
            else:
                self.failure_count += 1
                if self.failure_count >= self.failure_threshold:
                    self.state = OPEN
                    self.opened_at = time.time()
            raise

# closed is when there is no issue with the tool call again
# open is when an issue has occurred 
# half-open is when it is allowed to retry now but not sure if there will be issue or not 

# dec 2: because we want a state that captures something ready to retry 
# I don't know dec 3 and 4 very well


''' EXAMPLE USAGE '''
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=30)

def search_tool(query):
    return requests.get(f"https://search-api.com?q={query}")

# agent tool call
try:
    result = breaker.call(search_tool, "latest papers on RL")
except Exception as e:
    # fall back to another tool or report cleanly
    result = fallback_tool(query)
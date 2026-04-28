# Thread-safe batch processor
# Runs jobs concurrently across num_workers threads
# Each worker pulls from a shared queue, processes jobs, and stores results
# Main thread blocks until all jobs are complete via queue.join()
# Note: concurrent.futures.ThreadPoolExecutor does the same thing 

from threading import Thread
from queue import Queue

def worker(queue, results):
    while True:
        job = queue.get()
        if job is None:
            queue.task_done()
            break
        try:
            result = job()
            results.put(result)
        except Exception as e:
            results.put(e)
        finally:
            queue.task_done()

def run_batch(jobs, num_workers):
    queue = Queue()
    results = Queue()
    threads = []

    for _ in range(num_workers):
        t = Thread(target=worker, args=(queue, results), daemon=True)
        t.start()
        threads.append(t)

    for job in jobs:
        queue.put(job)

    for _ in range(num_workers):
        queue.put(None)

    queue.join()

    return list(results.queue)
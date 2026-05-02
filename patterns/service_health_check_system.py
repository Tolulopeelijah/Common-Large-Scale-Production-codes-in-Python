""""Service health check system

Real scenario: you're running multiple services — an LLM inference server, a vector DB, a Redis cache, a Postgres instance. 
Kubernetes, load balancers, and monitoring systems all call a /health endpoint to decide whether to route traffic to your service or restart it. 
You need to implement the health check registry that powers that endpoint.
"""
from dataclasses import dataclass, field
from threading import Thread
from datetime import datetime, timezone


class HealthStatus:
    HEALTHY   = "healthy"
    DEGRADED  = "degraded"
    UNHEALTHY = "unhealthy"


class HealthCheck:
    def __init__(self, name, check_fn, timeout):
        self.name = name
        self.check_fn = check_fn
        self.timeout = timeout

    def run(self):
        result = [self.name, HealthStatus.UNHEALTHY, "timed out"]  # default

        def target():
            try:
                self.check_fn()
                result[1] = HealthStatus.HEALTHY
                result[2] = None
            except Exception as e:
                result[1] = HealthStatus.UNHEALTHY
                result[2] = str(e)

        t = Thread(target=target)
        t.start()
        t.join(timeout=self.timeout)   # wait up to timeout seconds
        # if thread still alive after join, it timed out — result stays as default
        return tuple(result)


class HealthRegistry:
    def __init__(self):
        self.checks = []

    def register(self, name, check_fn, timeout=5):
        self.checks.append(HealthCheck(name, check_fn, timeout))  # store, don't run yet

    def run_all(self):
        # run all checks concurrently
        threads = []
        results = [None] * len(self.checks)

        def run_check(i, check):
            results[i] = check.run()

        for i, check in enumerate(self.checks):
            t = Thread(target=run_check, args=(i, check))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        overall = HealthStatus.HEALTHY
        for name, status, error in results:
            if status == HealthStatus.UNHEALTHY:
                overall = HealthStatus.UNHEALTHY
            elif status == HealthStatus.DEGRADED and overall != HealthStatus.UNHEALTHY:
                overall = HealthStatus.DEGRADED

        return {
            "status": overall,
            "checks": results,
            "timestamp": datetime.now(timezone.utc).timestamp()  # unix float, utc
        }

    def as_http_response(self):
        result = self.run_all()
        codes = {
            HealthStatus.HEALTHY:   200,
            HealthStatus.DEGRADED:  207,
            HealthStatus.UNHEALTHY: 503
        }
        code = codes[result["status"]]
        return code, result
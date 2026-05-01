from dataclass import dataclass

@dataclass
class HealthStatus:
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"



class HealthCheck:
    def __init__(self, name, check_fn, timeout):
        self.name = name
        self.check_fn = check_fn
        self.timeout = timeout

    def run(self):
        try:
            check_fn()
            return name,HEALTHY,None
        except Exception as e:
            return (name, UNHEALTHY, "timed out")

        except Exception as e:
            return (name, UNHEALTHY, str(e))

class HealthRegistry:
    def __init__(self):
        self.checks = []
    def register(self, name, check_fn, timeout = 5):
        self.checks.append(HealthCheck(name, check_fn,timeout).run())

    def run_all(self):
        results = 

        overall = HEALTHY
        for name, status, error in results:
            if status == UNHEALTHY:
                overall = UNHEALTHY
            elif status == DEGRADED and overall != UNHEALTHY:
                overall = DEGRADED

        return {"status": overall, "checks": results, "timestamp": current_time}

    def as_http_response(self):
        result = self.run_all()
        code = 200 if healthy else 404
        return code, result
"""
Build an event bus.
A central object that lets different parts of a system communicate without knowing about each other. Any component can subscribe to an event by name, passing a function to call when that event fires. Any component can publish an event by name, optionally passing data. All subscribers to that event get called with the data."""


class EventBus:
    def __init__(self):
        self.events = {}

    def subscribe(self, event_name, func):
        self.events.setdefault(event_name, []).append(func)
    
    def publish(self, event_name, data = None):
        for func in self.events.get(event_name, []):
            func(data)

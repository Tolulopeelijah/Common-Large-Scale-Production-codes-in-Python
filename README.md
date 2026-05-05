# Production Python (Idea to Code Drills)

A self-imposed daily drill: given a production-grade problem description, implement it in Python without autocomplete or AI assistance, reviewed and hardened after each attempt. Builds speed converting thought to code, familiarity with production patterns before encountering them in real codebases, and muscle memory for Python idioms beyond algorithm solving.


## Notes
I will be jotting down a few techniques, hacks and standardized method I learn each day.

- Open/Closed Principle (Open to Extension, Closed to Modification): Add features by writing new code, not changing old code.
_*Other principles in the SOLID Principles:*_
*S - Single Responsibility:* One class, one job.
*O - Open/Closed:* Add new code, don't change old code.
*L - Liskov Substitution:* Child classes should work anywhere parent works.
*I - Interface Segregation:* Many small interfaces > one big interface.
*D - Dependency Inversion:* Depend on abstractions, not concrete details.

- When using .get() on a Queue, it does not throw an error when empty, it blocks until an item is available.
- Queue acquires a lock when accessing its elements, making it suitable for concurrent access across multiple threads.
- The validated attribute descriptor is essentially how Django model fields work under the hood.
- every agent tool call (web search, code exec, llm call,..) should be wrapped in resource lifecycle management [context manager](https://github.com/Tolulopeelijah/Common-Large-Scale-Production-codes-in-Python/blob/main/patterns/context_manager.py) in case the agent crashes mid run, it won't cause dangling conn, leaked file handles, or half written state. (guaranteeing cleanup regardless of what went wrong).
- there is no way in python to stop a running function after N seconds outside the thread running it, so a trick is to run in a Thread then join with timeout (the thread will still continue in background though until failure or sucess).
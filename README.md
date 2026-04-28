# Common Production Patterns & Large Scale Techniques in Python 
I asked claude to keep giving me production grade pseudo code to implement in python, just to strengthen my idea_to_code muscle and get more familiar with techniques in large scale code.

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
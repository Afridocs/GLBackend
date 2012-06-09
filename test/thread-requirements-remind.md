## Issues

### SQLAlchemy and Twisted don't fit well

Multithreading shall cause insane process duplication,
need to be clear which kind of classes are redounder between thread and which are singleton
ORM need to run in a separare singleton thread
therefore require an IPC able to collect requests and return answer.

this mean that the IPC need to collect request in SQL-like format,
and return object.

**ouch**

#!/usr/local/bin/python
try:
    while True:
        try:
            event = inbox.get(False)
        except QueueEmpty:
            continue
        if datetime.fromiso(event.occurrenceTime) < self.now:
            continue                  
        if self.isValidEvent(event):
            self.processEvent(event)

except (KeyboardInterrupt, StopIteration):
    # I'm not sure why I even bother with this,
    # because a keyboard interrupt is raised
    # no matter what, dunno why
    pass
finally:
    pass
    # postal.stop()

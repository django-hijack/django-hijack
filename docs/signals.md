# Signals

## Default Parameters

The following signals by default supply the following parameters::

    sender: Currently always None
    request: The standard request object all views receive.
    hijacker: The user object doing the hijacking.
    hijacked: The user object being hijacked and taken over.

## Available Signals

### hijack.signals.pre_hijack_started

Sent BEFORE the hijack occurs. Session data is still for the hijacker.

Data returned from this signal is passed onto `hijack_started`.

### hijack.signals.hijack_started

Sent AFTER the hijack occurs. Session data is now for the hijacked.

In addition to the default parameters mentioned above, this signal also 
supplies an additional parameter `pre_hijack_started_results`. 
This parameter contains a list of tuple pairs **[(receiver, response), ... ]**, 
representing the list of called receiver functions and their response values
of all other functions called using the `pre_hijack_started` signal.

This additional parameter is useful for when you need to manipulate session data BEFORE 
a hijack occurs and at the same time passing the results onto the `hijack_started` 
signal AFTER the hijack has happened.

### hijack.signals.pre_hijack_ended
    
Sent BEFORE the hijack ends. Session data is still for the hijacked user.

Data returned from this signal is passed onto `hijack_ended`.

### hijack.signals.hijack_ended

Sent AFTER the hijack ends. Session data is now for the hijacker.
 
This signal also supplies an additional parameter `pre_hijack_ended_results`. 
This parameter contains a list of tuple pairs **[(receiver, response), ... ]**, 
representing the list of called receiver functions and their response values
of all other functions called using the `pre_hijack_ended` signal.

This additional parameter is useful for when you need to manipulate session data BEFORE 
a hijack ends and at the same time passing the results onto the `hijack_ended` 
signal AFTER the hijack ends.

 
## Examples:

```python
from hijack.signals import hijack_started, hijack_ended, pre_hijack_started, pre_hijack_ended

def print_pre_hijack_started(sender, hijacker_id, hijacked_id, request, **kwargs):
    print('%d is about to hijack %d' % (hijacker_id, hijacked_id))
pre_hijack_started.connect(print_pre_hijack_started)

def print_hijack_started(sender, hijacker_id, hijacked_id, request, **kwargs):
    print('%d has hijacked %d' % (hijacker_id, hijacked_id))
hijack_started.connect(print_hijack_started)

def print_pre_hijack_ended(sender, hijacker_id, hijacked_id, request, **kwargs):
    print('%d is about to release %d' % (hijacker_id, hijacked_id))
pre_hijack_ended.connect(print_pre_hijack_ended)
    
def print_hijack_ended(sender, hijacker_id, hijacked_id, request, **kwargs):
    print('%d has released %d' % (hijacker_id, hijacked_id))
hijack_ended.connect(print_hijack_ended)
```

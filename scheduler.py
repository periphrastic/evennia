import events
from twisted.internet import task
"""
ADDING AN EVENT:
* Create an event function to call.
* Add an entry to the 'schedule' dictionary here.
* Profit.
"""

# Dictionary of events with a list in the form of:
#  [<function>, <interval>, <lastrantime>, <taskobject>, <description>]
schedule = {
   'check_sessions': [events.check_sessions, 5, None, None, "Session check."]
}

def start_events():
   """
   Start the event system, which is built on Twisted's framework.
   """
   for event in schedule:
      event_func = get_event_function(event)

      if callable(event_func):
         # Set the call-back function for the task to trigger_event, but pass
         # a reference to the event function.
         event_task = task.LoopingCall(trigger_event, event_func, event)
         # Start the task up with the specified interval.
         event_task.start(get_event_interval(event), now=False)
         # Set a reference to the event's task object in the dictionary so we
         # can re-schedule, start, and stop events from elsewhere.
         set_event_taskobj(event, event_task)

def get_event(event_name):
   """
   Return the relevant entry in the schedule dictionary for the named event.

   event_name: (string) The key of the event in the schedule dictionary.
   """
   return schedule.get(event_name, None)

def get_event_function(event_name):
   """
   Return a reference to the event's function.

   event_name: (string) The key of the event in the schedule dictionary.
   """
   return get_event(event_name)[0]

def get_event_interval(event_name):
   """
   Return the event's execution interval.

   event_name: (string) The key of the event in the schedule dictionary.
   """
   return get_event(event_name)[1]

def set_event_taskobj(event_name, taskobj):
   """
   Sets an event's task object.

   event_name: (string) The key of the event in the schedule dictionary.
   """
   get_event(event_name)[3] = taskobj

def trigger_event(event_func, event_name):
   """
   Update the last ran time and fire off the event.

   event_func: (func_reference) Reference to the event function to fire.
   eventname: (string) The name of the event (as per schedule dict).
   """
   event_func()
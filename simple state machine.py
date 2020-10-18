from FSM import *

"""
    Implements FSM at https://en.wikipedia.org/wiki/Finite-state_machine#Example:_coin-operated_turnstile and https://en.wikipedia.org/wiki/Finite-state_machine#Transducers
"""

turnstile_state_machine = FSM([["Locked", "push", "Locked"],
                               ["Locked", "coin", "Unlocked"],
                               ["Unlocked", "push", "Locked"],
                               ["Unlocked", "coin", "Locked"]])

turnstile_state_machine.set_initial_state("Locked")

print turnstile_state_machine.get_current_state()
turnstile_state_machine.transition_states("push")

print turnstile_state_machine.get_current_state()
turnstile_state_machine.transition_states("coin")

print turnstile_state_machine.get_current_state()


door_state_machine = FSM([["Opened", "close", "Closing"],
                          ["Closed", "open", "Opening"],
                          ["Opening", "close", "Closing"],
                          ["Opening", "sensor opened", "Open"],
                          ["Closing", "open", "Opening"],
                          ["Closing", "sensor closed", "Closed"]])

door_state_machine.set_initial_state("Opened")

print door_state_machine.get_current_state()
door_state_machine.transition_states("close")

print door_state_machine.get_current_state()
door_state_machine.transition_states("sensor closed")

print door_state_machine.get_current_state()



"""
    FSM Generator
"""

class STATE :

    def __init__(self, name, transition_condition, next_state, event_handler = None) :
        self.name = name
        self.condition = transition_condition
        self.next = next_state
        self.event_handler = event_handler

    def get_state_name(self) :
        return self.name

    def will_transition(self, condition) :
        return (self.condition == condition) or (self.condition == "Always")

    def get_next_state(self, condition) :
        if self.will_transition(condition) :
            return self.next
        return None
    
    def handle_state_event (self) :
        if self.event_handler is not None :
            self.event_handler()
    
    def __str__ (self) :
        return self.name


class FSM :

    def __init__(self, states = []) :
        # states is a list of lists, eg:
        # [["state one name", "conditional", "next state name", optional handler function],
        #  ["state two name", "conditional", "next state name", optional handler function]]
        self.current_state = None
        self.states = []
        
        for state in range(len(states)) :
            if len(states[state]) == 3 :
                new_state = STATE(states[state][0],
                                  states[state][1],
                                  states[state][2])
            else :
                new_state = STATE(states[state][0],
                                  states[state][1],
                                  states[state][2],
                                  states[state][3])
            self.states.append(new_state)

    def add_state(self, name, transition_condition, next_state, event_handler = None) :
        # Expected inputs:
        # "state name", "state transition condition", "next state name", optional handler function
        new_state = STATE(name, transition_condition, next_state, event_handler)
        self.states.append(new_state)


    def set_initial_state(self, state) :
        self.set_current_state(state)


    def get_current_state(self) :
        if self.current_state is not None :
            return self.current_state.get_state_name()


    def set_current_state(self, state_name) :
        for state in self.states :
            if state.get_state_name() == state_name :
                self.current_state = state


    def get_next_state(self, condition) :
        for state in self.states :
            if state.get_state_name() == self.get_current_state() :
                if state.get_next_state(condition) is not None :
                    return state.get_next_state(condition)
        return None

    def transition_states(self, condition) :
        if self.get_next_state(condition) is not None :
            self.set_current_state(self.get_next_state(condition))
            self.current_state.handle_state_event()

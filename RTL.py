from FSM import *

"""
    ISA description from https://en.wikipedia.org/wiki/Little_man_computer
    
    Implementation detail questions:
    - How do we deal with overflow of PC?
    - How do we deal with over/underflow on ADD/SUB?
        ->  Implemented -ve flag. Set on underflow. Cleared on positive result for
            SUB instruction only.
    - How do we deal with negative numbers in INPUT?
    - How does BRP (Branch If Positive) ever NOT take the branch if there are no negative numbers?
    http://www.peterhigginson.co.uk/LMC/help.html
    https://www.gwegogledd.cymru/wp-content/uploads/2018/04/RISC-Simulator-Design.pdf ???
"""

class LMC_RTL :

    def __init__(self, memory) :
        self.program_counter = 0
        self.instruction_register = 0
        self.accumulator = 0
        self.memory_address_register = 0
        self.memory_data_register = 0
        self.negative_flag = False
        self.input_register = 0
        self.output_register = 0
        
        self.RTL_model = FSM()
        # memory passed as a mutable list. We take advantage of this by copying a
        # reference to it, then modifying any value in the list directly
        self.memory = memory
        self.clock_cycles = 0
        self.instruction_cycles = 0


        self.init_processor_flow_control_states()
        self.init_fetch_states()
        self.init_decode_states()
        self.init_execute_states()
        self.init_retire_states()
        self.reset()



    def get_current_state(self) :
        return self.RTL_model.get_current_state()
 
    
    def get_memory_image(self) :
        return self.memory
    
    
    def get_elapsed_clock_cycles(self) :
        return self.clock_cycles
    
    
    def get_elapsed_instruction_cycles(self) :
        return self.instruction_cycles
    
    
    def get_program_counter(self) :
        return self.program_counter


    def get_instruction_register(self) :
        return self.instruction_register
    
    
    def get_accumulator(self) :
        return self.accumulator


    def get_memory_address_register(self) :
        return self.memory_address_register


    def get_memory_data_register(self) :
        return self.memory_data_register

    
    def get_formatted_memory_image(self) :
        # Better format than this? Deal with negative numbers?
        output_string = ""
        for i in range(10) :
            if self.memory[i * 10] < 100 :
                output_string += "0"
            if self.memory[i * 10] < 10 :
                output_string += "0"
            output_string += str(self.memory[i * 10])
            
            for j in range(1, 10) :
                output_string += " "
                if self.memory[i * 10 + j] < 100 :
                    output_string += "0"
                if self.memory[i * 10 + j] < 10 :
                    output_string += "0"
                output_string += str(self.memory[i * 10 + j])
            if i < 9 :
                output_string += "\n"
        return output_string
    
    
    def reset(self) :
        self.program_counter = 0
        self.instruction_register = 0
        self.accumulator = 0
        self.memory_address_register = 0
        self.memory_data_register = 0
        self.input_register = 0
        self.output_register = 0
        self.negative_flag = False
        self.RTL_model.set_current_state("Reset")
    
    
    def clock(self, single_step = False, single_cycle = False) :
        self.RTL_model.transition_states(self.decode_instruction())
        self.clock_cycles += 1
    
    
    def init_processor_flow_control_states(self) :
        def monitor_instruction_cycles() :
            self.instruction_cycles += 1
        
        self.RTL_model.add_state("Reset", "Always", "Fetch", monitor_instruction_cycles)
        self.RTL_model.add_state("Halt", "Always", "Halt", monitor_instruction_cycles)


    def init_fetch_states(self) :
        def fetch_instruction() :
            self.memory_address_register = self.program_counter
            self.memory_data_register = self.memory[self.memory_address_register]
            self.instruction_register = self.memory_data_register
            self.program_counter = self.program_counter + 1
            if self.program_counter > 99 :
                # Handle overflow of program counter. This doesn't seem to be defined?
                self.program_counter = 0

        self.RTL_model.add_state("Fetch", "Always", "Decode", fetch_instruction)
    
    
    def init_decode_states(self) :
        
        self.RTL_model.add_state("Decode", "Addition", "Execute Addition")
        self.RTL_model.add_state("Decode", "Subtraction", "Execute Subtraction")
        self.RTL_model.add_state("Decode", "Store", "Execute Store")
        self.RTL_model.add_state("Decode", "Load", "Execute Load")
        self.RTL_model.add_state("Decode", "Branch Unconditionally", "Execute Branch Unconditionally")
        self.RTL_model.add_state("Decode", "Branch If Zero", "Execute Branch If Zero")
        self.RTL_model.add_state("Decode", "Branch If Positive", "Execute Branch If Positive")
        self.RTL_model.add_state("Decode", "Input", "Execute Input")
        self.RTL_model.add_state("Decode", "Output", "Execute Output")
        self.RTL_model.add_state("Decode", "Halt", "Execute Halt")
        self.RTL_model.add_state("Decode", "No Operation", "Execute No Operation")


    def init_execute_states(self) :
        
        def execute_addition_instruction() :
            self.memory_address_register = self.get_address_from_instruction_register()
            self.memory_data_register = self.memory[self.memory_address_register]
            # Overflow behaviour doesn't seem to be defined, although BRP instruction implies
            # negative results are possible. Here, we just wrap to 0 > 999
            self.accumulator = (self.accumulator + self.memory_data_register) % 1000

        def execute_subtraction_instruction() :
            self.memory_address_register = self.get_address_from_instruction_register()
            self.memory_data_register = self.memory[self.memory_address_register]
            # Underflow isn't defined either
            self.accumulator = self.accumulator - self.memory_data_register
            if self.accumulator < 0 :
                self.negative_flag = True
            else :
                self.negative_flag = False
            self.accumulator = self.accumulator % 1000
        
        def execute_store_instruction() :
            self.memory_address_register = self.get_address_from_instruction_register()
            self.memory_data_register = self.accumulator
            self.memory[self.memory_address_register] = self.memory_data_register
        
        def execute_load_instruction() :
            self.memory_address_register = self.get_address_from_instruction_register()
            self.memory_data_register = self.memory[self.memory_address_register]
            self.accumulator = self.memory_data_register
        
        def execute_unconditional_branch_instruction() :
            self.program_counter = self.get_address_from_instruction_register()
        
        def execute_branch_if_zero_instruction() :
            if self.accumulator == 0 :
                self.program_counter = self.get_address_from_instruction_register()
        
        def execute_branch_if_positive_instruction() :
            if self.negative_flag is False :
                print "Taking branch!"
                self.program_counter = self.get_address_from_instruction_register()
        
        def execute_input_instruction() :
            # Better handling of inputs? Reject bad input?
            self.input_register = input("Input: ")
            self.accumulator = self.input_register
        
        def execute_output_instruction() :
            # Better display negative numbers?
            self.output_register = self.accumulator
            output_string = ""
            if self.output_register < 100 :
                output_string += "0"
            if self.output_register < 10 :
                output_string += "0"
            print "Output: " + output_string + str(self.output_register)

        self.RTL_model.add_state("Execute Addition", "Always", "Retire", execute_addition_instruction)
        self.RTL_model.add_state("Execute Subtraction", "Always", "Retire", execute_subtraction_instruction)
        self.RTL_model.add_state("Execute Store", "Always", "Retire", execute_store_instruction)
        self.RTL_model.add_state("Execute Load", "Always", "Retire", execute_load_instruction)
        self.RTL_model.add_state("Execute Branch Unconditionally", "Always", "Retire", execute_unconditional_branch_instruction)
        self.RTL_model.add_state("Execute Branch If Zero", "Always", "Retire", execute_branch_if_zero_instruction)
        self.RTL_model.add_state("Execute Branch If Positive", "Always", "Retire", execute_branch_if_positive_instruction)
        self.RTL_model.add_state("Execute Input", "Always", "Retire", execute_input_instruction)
        self.RTL_model.add_state("Execute Output", "Always", "Retire", execute_output_instruction)
        self.RTL_model.add_state("Execute Halt", "Always", "Halt")
        self.RTL_model.add_state("Execute No Operation", "Always", "Retire")


    def init_retire_states(self) :
        def monitor_instruction_cycles() :
            self.instruction_cycles += 1
        
        self.RTL_model.add_state("Retire", "Always", "Fetch", monitor_instruction_cycles)


    def decode_instruction(self) :
        if (self.instruction_register >= 100) and \
           (self.instruction_register <= 199) :
            return "Addition"
        if (self.instruction_register >= 200) and \
           (self.instruction_register <= 299) :
            return "Subtraction"
        if (self.instruction_register >= 300) and \
           (self.instruction_register <= 399) :
            return "Store"
        if (self.instruction_register >= 500) and \
           (self.instruction_register <= 599) :
            return "Load"
        if (self.instruction_register >= 600) and \
           (self.instruction_register <= 699) :
            return "Branch Unconditionally"
        if (self.instruction_register >= 700) and \
           (self.instruction_register <= 799) :
            return "Branch If Zero"
        if (self.instruction_register >= 800) and \
           (self.instruction_register <= 899) :
            return "Branch If Positive"
        if (self.instruction_register == 901) :
            return "Input"
        if (self.instruction_register == 902) :
            return "Output"
        if (self.instruction_register == 000) :
            return "Halt"
        return "No Operation"


    def get_address_from_instruction_register(self) :
        if self.decode_instruction() == "Addition" :
            return self.instruction_register - 100
        if self.decode_instruction() == "Subtraction" :
            return self.instruction_register - 200
        if self.decode_instruction() == "Store" :
            return self.instruction_register - 300
        if self.decode_instruction() == "Load" :
            return self.instruction_register - 500
        if self.decode_instruction() == "Branch Unconditionally" :
            return self.instruction_register - 600
        if self.decode_instruction() == "Branch If Zero" :
            return self.instruction_register - 700
        if self.decode_instruction() == "Branch If Positive" :
            return self.instruction_register - 800






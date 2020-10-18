from RTL import *

single_step = False
single_cycle = False
debug = False
timed = True

blank_memory_image         = [000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000]

IFN503_Tutorial_Four_A     = [901, 305, 901, 105, 902, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000]

IFN503_Tutorial_Four_B     = [901, 310, 901, 311, 210, 808, 510, 211, 902, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000]

IFN503_Tutorial_Four_C     = [901, 398, 901, 399, 598, 297, 398, 712, 901, 199,
                              399, 604, 599, 902, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 001, 000, 000]

# https://en.wikipedia.org/wiki/Little_man_computer#Example
squared_input_memory_image = [523, 319, 320, 901, 718, 322, 519, 122, 319, 520,
                              121, 320, 222, 715, 606, 519, 902, 600, 000, 000,
                              000, 001, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000]

# https://en.wikipedia.org/wiki/Little_man_computer#Example
quine_memory_image         = [500, 902, 208, 708, 500, 108, 300, 600, 001, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000]


test_memory_image          = [620, 570, 179, 390, 591, 179, 391, 570, 620, 599,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 001,
                              000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
                              599, 599, 000, 000, 000, 000, 000, 000, 000, 000]


simple_LMC = LMC_RTL(IFN503_Tutorial_Four_C)


while simple_LMC.get_current_state() is not "Halt" :
    if debug:
        print "State: " + str(simple_LMC.get_current_state())
        print "MAR: " + str(simple_LMC.get_memory_address_register())
        print "MDR: " + str(simple_LMC.get_memory_data_register())
        print "PC: " + str(simple_LMC.get_program_counter())
        print "IR: " + str(simple_LMC.get_instruction_register())
        print "ACC: " + str(simple_LMC.get_accumulator())
        print "FLAG: " + str(simple_LMC.negative_flag)
    simple_LMC.clock(single_step = False, single_cycle = False)

if timed:
    print "Clock Cycles: " + str(simple_LMC.get_elapsed_clock_cycles())
    print "Instructin Cycles: " + str(simple_LMC.get_elapsed_instruction_cycles())

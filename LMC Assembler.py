from FSM import *

file = "quine.lmc"

class TOKEN :

    def __init__(self, name_string = "", token_type = None) :
        self.name = name_string
        self.current_type = self.get_token_type()
        self.next_type = self.get_next()
        self.next = None
        
        self.one_argument_instructions  = ["ADD", "SUB", "STA", "LDA", \
                                          "BRA", "BRZ", "BRP", "DAT"]
        self.zero_argument_instructions = ["INP", "OUT", "HLT"]
        self.valid_instructions = self.one_argument_instructions + \
                                  self.zero_argument_instructions
        self.available_types = ["One Argument Instruction", "Zero Argument Instruction", \
                                "Label", "Literal", "Comment", "End of Line"]
    
    def __str__(self) :
        return self.name
    
    
    def get_type(self) :
        if self.name_string in self.one_argument_instructions :
            return "One Argument Instruction"

        if self.name_string in self.zero_argument_instructions :
            return "Zero Argument Instruction"

        if is_valid_literal(self.name_string) :
            return "Literal"

        if is_valid_comment(self.name_string) :
            return "Comment"
                
        if is_valid_label(self.name_string) :
            return "Label"
    
    
    def get_next(self) :
        if self.type == "Zero Argument Instruction" :
            return ["Comment", "End of Line"]
        
        if self.type == "One Argument Instruction" :
            return ["Label", "Literal"]

        if self.type == "Label" :
            return ["One Argument Instruction", "Zero Argument Instruction",
                    "Comment", "End of Line"]
        
        if self.type == "Literal" :
            return ["Comment", "End of Line"]

        if self.type == "Comment" :
            return ["End of Line"]

        if self.type == "End of Line" :
            return ["End of Line"]


    def is_valid_instruction(self, string) :
        return string in self.valid_opcodes


    def is_valid_literal(self, string) :
        if string.isdigit() :
            return True
        if string[0] == "-" and string[1 : ].isdigit() :
            return True
        return False


    def is_valid_comment(self, string) :
        if string[0] == "/" and string[1] == "/":
            return True
        return False


    def is_valid_label(self, string) :
        if self.is_valid_instruction(string) == True or \
           self.is_valid_literal(string) == True or \
           self.is_comment(string) == True:
            return False
        return True


class PARSER :

    def __init__(self):
        pass

    def parse_line(self, tokens)
        for token in tokens:
            


with open(file) as assembly_file:
    line_number = 0
    parser = PARSER()
    for line in assembly_file:
        tokens = line.split()
        parser.parse_line(tokens)




class PARSER :

    def __init__(self) :

        self.grammar_parser = FSM()
        self.tokens = []
        self.labels = {}
        self.line_number = 1
        self.one_argument_opcodes  = ["ADD", "SUB", "STA", "LDA", \
                                        "BRA", "BRZ", "BRP", "DAT"]
        self.zero_argument_opcodes = ["INP", "OUT", "HLT"]
        self.valid_opcodes = self.one_argument_opcodes + self.zero_argument_opcodes
    
        self.init_grammar_rules()
    
    def parse_line(self, tokens) :
        self.tokens = tokens
        self.grammar_parser.set_initial_state("Begin Parsing Line")
        while self.get_state() != "Finished Parsing Line" :
            self.grammar_parser.transition_states(self.get_token_type(self.tokens[0]))
        self.line_number += 1
    
    def is_valid_instruction(self, string) :
        return string in self.valid_opcodes
    
    
    def is_valid_literal(self, string) :
        if string.isdigit() :
            return True
        if string[0] == "-" and string[1 : ].isdigit() :
            return True
        return False


    def is_comment(self, string) :
        if string[0] == "/" and string[1] == "/":
            return True
        return False

    def is_label(self, string) :
        if self.is_valid_instruction(string) == True or \
           self.is_valid_literal(string) == True or \
           self.is_comment(string) == True:
            return False
        return True

    def is_label_catalogued(self, label_name) :
        if label_name in self.labels :
            return True
        else :
            return False

    def get_state(self) :
        return self.grammar_parser.get_current_state()

    def get_token_type(self, token) :
        if self.is_valid_instruction(token) :
            return "Instruction"
        elif self.is_valid_literal(token) :
            return "Literal"
        elif self.is_comment(token) :
            return "Comment"
        else:
            return "Label"

    def init_grammar_rules(self) :
        def unexpected_label_handler() :
            print "Error - Unexpected label: " + str(self.tokens[0]) + " on line " + str(self.line_number)
            self.grammar_parser.set_current_state("Finished Parsing Line")

        def unexpected_instruction_handler() :
            print "Error - Unexpected instruction: " + str(self.tokens[0]) + " on line " + str(self.line_number)
            self.grammar_parser.set_current_state("Finished Parsing Line")

        def unexpected_literal_handler() :
            print "Error - Unexepected literal: " + str(self.tokens[0]) + " on line " + str(self.line_number)
            self.grammar_parser.set_current_state("Finished Parsing Line")
        
        def trim_token_list() :
            if len(self.tokens) == 1 :
                self.grammar_parser.set_current_state("Finished Parsing Line")
            else :
                self.tokens = self.tokens[1 : ]
      
        def add_label_to_catalogue() :
            if self.is_label_catalogued(self.tokens[0]) :
                if self.labels[self.tokens[0]] != -1 :
                    print "Error - Duplicate Label: " + str(self.tokens[0]) + " on line " + str(self.line_number)
                    self.grammar_parser.set_current_state("Finished Parsing Line")
                else:
                    self.labels.update({self.tokens[0]: self.line_number})
            else :
                self.labels.update({self.tokens[0]: self.line_number})
        
        def check_catalogue_for_label() :
            if not self.is_label_catalogued(self.tokens[0]) :
                print "Warning - Label Referenced before Assignment: " + str(self.tokens[0]) + " on line " + str(self.line_number)
                self.labels.update({self.tokens[0]: -1})
 
        self.grammar_parser.add_state("Begin Parsing Line", "Always", "Catagorising First Token")
        
        self.grammar_parser.add_state("Catagorising First Token", "Label", "First token is a Label")
        self.grammar_parser.add_state("Catagorising First Token", "Instruction", "First token is an Instruction")
        self.grammar_parser.add_state("Catagorising First Token", "Literal", "First token is a Literal")
        self.grammar_parser.add_state("Catagorising First Token", "Comment", "First token is a Comment")

        self.grammar_parser.add_state("Catagorising Second Token", "Label", "Second token is a Label", trim_token_list)
        self.grammar_parser.add_state("Catagorising Second Token", "Instruction", "Second token is an Instruction", trim_token_list)
        self.grammar_parser.add_state("Catagorising Second Token", "Literal", "Second token is a Literal", trim_token_list)
        self.grammar_parser.add_state("Catagorising Second Token", "Comment", "Second token is a Comment", trim_token_list)

        self.grammar_parser.add_state("Catagorising Third Token", "Label", "Third token is a Label", trim_token_list)
        self.grammar_parser.add_state("Catagorising Third Token", "Instruction", "Third token is an Instruction", trim_token_list)
        self.grammar_parser.add_state("Catagorising Third Token", "Literal", "Third token is a Literal", trim_token_list)
        self.grammar_parser.add_state("Catagorising Third Token", "Comment", "Third token is a Comment", trim_token_list)

        self.grammar_parser.add_state("Catagorising Fourth Token", "Label", "Fourth token is a Label", trim_token_list)
        self.grammar_parser.add_state("Catagorising Fourth Token", "Instruction", "Fourth token is an Instruction", trim_token_list)
        self.grammar_parser.add_state("Catagorising Fourth Token", "Literal", "Fourth token is a Literal", trim_token_list)
        self.grammar_parser.add_state("Catagorising Fourth Token", "Comment", "Fourth token is a Comment", trim_token_list)

        self.grammar_parser.add_state("First token is a Label", "Always", "Catagorising Second Token", add_label_to_catalogue)
        self.grammar_parser.add_state("First token is an Instruction", "Always", "Catagorising Second Token")
        self.grammar_parser.add_state("First token is a Literal", "Always", "Unexpected Literal Error")
        self.grammar_parser.add_state("First token is a Comment", "Always", "Finished Parsing Line")

        self.grammar_parser.add_state("Second token is a Label", "Always", "Catagorising Third Token", check_catalogue_for_label)
        self.grammar_parser.add_state("Second token is an Instruction", "Always", "Catagorising Third Token")
        self.grammar_parser.add_state("Second token is a Literal", "Always", "Catagorising Third Token")
        self.grammar_parser.add_state("Second token is a Comment", "Always", "Finished Parsing Line")

        self.grammar_parser.add_state("Third token is a Label", "Always", "Catagorising Fourth Token", check_catalogue_for_label)
        self.grammar_parser.add_state("Third token is an Instruction", "Always", "Unexpected Instruction Error")
        self.grammar_parser.add_state("Third token is a Literal", "Always", "Catagorising Fourth Token")
        self.grammar_parser.add_state("Third token is a Comment", "Always", "Finished Parsing Line")

        self.grammar_parser.add_state("Fourth token is a Label", "Always", "Unexpected Label Error")
        self.grammar_parser.add_state("Fourth token is an Instruction", "Always", "Unexpected Instruction Error")
        self.grammar_parser.add_state("Fourth token is a Literal", "Always", "Unexpected Literal Error")
        self.grammar_parser.add_state("Fourth token is a Comment", "Always", "Finished Parsing Line")

        self.grammar_parser.add_state("Finished Parsing Line", "Always", "Finished Parsing Line")

        self.grammar_parser.add_state("Unexpected Label Error", "Always", "Finished Parsing Line", unexpected_label_handler)
        self.grammar_parser.add_state("Unexpected Literal Error", "Always", "Finished Parsing Line", unexpected_literal_handler)
        self.grammar_parser.add_state("Unexpected Instruction Error", "Always", "Finished Parsing Line", unexpected_instruction_handler)
    

        self.grammar_parser.set_initial_state("Begin Parsing Line")




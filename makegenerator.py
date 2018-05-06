'''
Created by Martin Vaško
'''
import os

class MakeGenenerator:
    '''
    Create Makefile generator
    '''
    def __init__(self, name):
        if os.path.dirname(name):
            self.filename = os.path.dirname(name) + "/Makefile"
        else:
            self.filename = "Makefile"
        self.target_name = os.path.basename(name)
        self.addition = ""
        self.message = ""


    def add_rule(self, content, rule=None):
        '''
        add makefile rule with its content
        '''
        if rule:
            self.addition += rule + ":\n\t"
        self.addition = self.addition + content + "\n"

    def generate(self, print_to_file=None):
        '''
        Generate Makefile contents
        '''
        self.message = (
            "all:\n\tpdflatex {}\n"
            "clean:\n\trm {} {}\n"
            "{}\n\n"
            ).format(self.target_name + ".tex", self.target_name + ".aux",
                     self.target_name + ".log", self.addition)
        if print_to_file:
            with open(self.filename, "w") as file:
                file.write(self.message)
        else:
            print(self.message)

    def __str__(self):
        return self.message

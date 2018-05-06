'''
Created by Martin Vaško
'''

import os


class ScriptGenerator:
    '''
    This class is supposed to generate bash script to given files.
    Class is responsible of creating nice names for graphs, executing make file
    clearing resources.
    '''
    def __init__(self, path, name):
        if os.path.dirname(path):
            self.name = os.path.dirname(path) + "/generator.sh"
        else:
            self.name = "generator.sh"
        self.message = ""
        self.graph_name = name
        self. additional_commands = ""

    def add_commands(self, commands):
        '''
        add bash commands.
        '''
        self.additional_commands += commands + "\n"


    def generate(self, print_to_file=None):
        '''
        generate script with filled message
        '''
        self.message = (
            "#!/usr/bin/bash\n"
            "# Created by Martin Vaško supporting GPL license\n"
            "# GNU GENERAL PUBLIC LICENSE\n"
            "# Version 3, 29 June 2007\n"
            "# Copyright (C) 2007 Free Software Foundation, Inc. <http://fsf.org/>\n"
            "# Everyone is permitted to copy and distribute verbatim copies\n"
            "# of this license document, but changing it is not allowed.\n\n\n"
            "make\n"
            "mv auto.pdf {}.pdf\n"
            "make clean\n"
            "{}\n"
            ).format(self.graph_name, self.additional_commands)
        if print_to_file:
            with open(self.name, "w+") as file:
                file.write(self.message)
            os.chmod(self.name, 0o775)
        else:
            print(self.message)

    def __str__(self):
        return self.message

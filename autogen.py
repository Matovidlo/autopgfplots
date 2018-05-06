#!/usr/bin/env python3
'''
Created by Martin Vaško
'''

import glob
import re
from makegenerator import MakeGenenerator
from texgenerator import TexGenerator
from scriptgenerator import ScriptGenerator
from getcoord import GetCoordinates


class GenerateOutput:
    '''
    This class is supposed to output by given options
    '''
    def __init__(self, options, output_file=None):
        self.options = options
        self.texgen = options.texgen
        self.makegen = options.makegen
        self.scriptgen = options.scriptgen
        self.output = output_file
        self.__generate__()


    def set_output(self, print_to_file):
        '''
        set output wether should be outputed to file or stdin.
        '''
        self.output = print_to_file


    def __get_steps__(self):
        '''
        TODO customize start point of steps
        '''
        if isinstance(self.options.step, (int, float)):
            tmp_dict = {}
            for i in range(0, len(self.options.values),
                           self.options.step):
                tmp_dict[list(self.options.values.values())[i]] = i
            result = ""
            for key, value in tmp_dict.items():
                result += "\t\t(" + str(value) + ", "\
                          + str(key).rstrip() + ")\n"
            self.options.values = result


    def __generate__(self):
        if self.makegen:
            self.makegen.generate(self.output)
        self.__get_steps__()
        self.scriptgen.generate(self.output)
        self.texgen.generate(self.options.values, self.output)


    def generate(self, print_to_file=None):
        '''
        generate output with given output file or intialized output within
        class.
        '''
        if print_to_file is None:
            if self.makegen:
                self.makegen.generate(self.output)
            self.scriptgen(self.output)
            self.texgen.generate(self.options.values, self.output)
        else:
            if self.makegen:
                self.makegen.generate(print_to_file)
            self.scriptgen(print_to_file)
            self.texgen.generate(self.options.values, print_to_file)

    def __str__(self):
        return str(self.options.values + "\n" + self.options.step)


class GeneratorOptions:
    '''
    Generator of options for pgfplot labels and name of files
    '''
    def __init__(self, name, xlabel, ylabel, graph_name):
        self.texgen = TexGenerator(name, xlabel, ylabel)
        self.scriptgen = ScriptGenerator(name, graph_name)
        self.makegen = MakeGenenerator(name)
        self.coordination = None
        self.filter_result = {}
        self.values = {}
        self.step = 1


    def clear_makefile(self):
        '''
        Add makefile to generator
        '''
        self.makegen = None


    def file_coordination(self, filename, position):
        '''
        parse one file
        '''
        # possibility of wildcard
        try:
            self.coordination.get_input()
        except FileNotFoundError:
            print("Could not open file with name: '{}'".format(filename))
            return False
        self.filter_result[filename] = self.coordination.filter_input(position)


    def list_coordination(self, filename, position):
        '''
        list of files which should give coordination
        '''
        for file in filename:
            try:
                self.coordination.get_input(file)
            except FileNotFoundError:
                print("Could not open file with name: '{}'".format(filename))
                return False
            self.filter_result[file] = self.coordination.filter_input(position)


    def define_coordination(self, filename, expression, position=0):
        '''
        Define how to get coordination from input file
        '''
        self.coordination = GetCoordinates(filename, expression)
        self.filter_result = {}

        if isinstance(filename, str):
            # when wildcard call list_coordination
            if len(glob.glob(filename)) > 1:
                self.list_coordination(glob.glob(filename), position)
            else:
                self.file_coordination(filename, position)

        # input is list of files
        elif isinstance(filename, (list, tuple)):
            self.list_coordination(filename, position)

        # use values instead of filter
        self.values = self.filter_result
        return self.filter_result


    def filter_coord(self, expression, position=0):
        '''
        filter coordinates with given expression.
        This variant is when define coordination expression filter is
        not enough to get values for pgfplots
        '''
        if self.filter_result is None:
            print("No coordination defined")
            return
        self.filter_result = re.search(expression, self.filter_result)
        self.filter_result = self.filter_result.group(position)

        # Return when wants to more processing of filtered string
        self.values = self.filter_result
        return self.filter_result


    def define_step(self, step=None, expression=None):
        '''
        When step defined use this int/float step, when defined as regular
        expression need to call function with extraction step from filename.
        '''
        if isinstance(step, (int, float)):
            self.step = step
        if isinstance(step, str) and expression:
            self.values = self.filter_result
            self.step = self.define_coordination(step, expression)

    def define_value(self, value):
        '''
        Define value when own processing is done. There are strict restrictions
        to define value. Better do not use this function when you are not forced
        to
        '''
        self.values = value

    def __str__(self):
        return self.filter_result


# Example main program
if __name__ == '__main__':
    GEN = GeneratorOptions("./here/auto", "Pocet", "Dlzka", "nice_graph")
    # clear makefile when not needed
    # GEN.clear_makefile()

    # add coordination and its parsing to get values
    VAL = GEN.define_coordination("input.txt", r"\d+")
    VAL = GEN.define_coordination("input.txt", r"\d+\n")

    VAL = GEN.define_coordination(("input.txt", "./here/log1.txt"), r"\d+\n")
    # Wildcard match
    VAL = GEN.define_coordination("./here/log*.txt", r"\d+\n")

    # TODO
    OUTPUT = GenerateOutput(GEN, True)
    # print(OUTPUT)

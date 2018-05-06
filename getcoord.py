'''
Created by Martin Vaško
'''

import re

class GetCoordinates:
    '''
    Class which creates coordinates by user given input
    '''
    def __init__(self, name, coord_filter):
        self.message = ""
        self.filename = name
        self.filter = coord_filter


    # def get_path(self):


    def get_input(self, input_file=None):
        '''
        read input to message
        '''
        # get path
        # set input file as given param
        if input_file:
            self.filename = input_file
        try:
            with open(self.filename, "r") as file:
                self.message = file.read()
        except FileNotFoundError:
            raise

    def filter_input(self, position):
        '''
        filter input by given coordination filter
        '''
        result = re.search(self.filter, self.message)
        # return first match
        return result.group(position)

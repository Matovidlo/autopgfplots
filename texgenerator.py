'''
Created by Martin Vaško
'''
class TexGenerator:
    '''
    Create tex files for pgfplots
    '''
    def __init__(self, name, xlabel, ylabel):
        self.filename = name + ".tex"
        self.docclass = "standalone"
        self.package = "\\usepackage{siunitx}\n"
        self.package += "\\usepackage{pgfplots}\n"
        self.package += "\\usepackage{pgfplotstable}\n"
        self.package += "\\usepackage[utf8]{inputenc}\n"
        self.scale = 1
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.message = ""

    def add_package(self, package):
        '''
        add tex package
        '''
        self.package += package + "\n"

    def change_scale(self, scale):
        '''
        change scale when necessary
        '''
        if not isinstance(scale, str):
            self.scale = scale

    def generate(self, coordinates, print_to_file=None):
        '''
        Generate Tex file which should be maked
        '''
        self.message = (
            "\\documentclass{{{}}}\n"
            "{}\n"
            "\\begin{{document}}\n"
            "\\begin{{tikzpicture}}\n"
            "\t\\begin{{axis}}[\n"
            "\t\tscale={},\n"
            "\t\txlabel={{ {} }},\n"
            "\t\tylabel={{ {} }}\n"
            "\t]\n\t\\addplot coordinates{{\n"
            "{}\t}};\n"
            "\t\\end{{axis}}\n"
            "\\end{{tikzpicture}}\n"
            "\\end{{document}}\n\n"
            ).format(self.docclass, self.package, self.scale, self.xlabel,
                     self.ylabel, coordinates)
        if print_to_file:
            with open(self.filename, "w") as file:
                file.write(self.message)
        else:
            print(self.message)


    def __str__(self):
        return self.message

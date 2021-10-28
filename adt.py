import fileinput

# Constants
SPACE = " "
INDENT = "   "
NL = "\n"
BLANK = ""
CLASS = "class "
COMMA = ", " 
ROOT = "self.root = True"
CHILD = "self.root = False"
DATA = "data"

# Code generatos

def gen_init(args = []):
    """
        Generates:
        def __init__(self, <args>): 
    """
    result = "def __init__(self"

    for arg in args:
        result += COMMA + arg
    
    result += "):"

    return result


def gen_type(name):
    """
        Generates:
        class <Name>:
            self.root = true
    """
    result = CLASS + name + ":" + NL
    result += INDENT + gen_init() + NL
    result += (2 * INDENT) + ROOT + NL
    return result


def gen_selfs(indent, *args):
    """
        Generates:
        self.<args[0]> = <args[0]>
        self.<args[1]> = <args[1]>
        ...
        self.<args[m]> = <args[m]>
    """
    result = BLANK
    
    for arg in args:
        arg = arg.replace(SPACE, BLANK)
        result += indent + "self." + arg + " = " + arg + NL
    
    return result


def gen_constructor(name, type_name, args):
    """
        Generates:
        class <name>(<type_name>):
            def __init__(self, <args>):
                self.root = False
                self.<args[0]> = <args[0]>
                ...
                self.<args[m]> = <args[m]>
                
    """
    result = CLASS + name + "(" + type_name +")" + ":" + NL
    result += INDENT + gen_init(args) + NL
    result += (2 * INDENT) + CHILD + NL
    result += gen_selfs(2 * INDENT, *args) + NL

    return result


# Parser.

def valid_name(name):
    """
        Validates number of constructor and data type. 
    """
    cond1 = name[0].isupper()
    return cond1


def preprocessor(source):
    """
        Generates a python script from source.
    """
    code = BLANK

    adt = False
    adt_name = None
    line_number = 1

    for line in source:
        tokens = line.replace(NL, BLANK).split(SPACE)
        
        if tokens[0] == DATA:
            if ":" not in line:
                raise SyntaxError("Line %d: No ':' in data declaration" 
                        % line_number)
           
            if len(tokens) < 2:
                raise SyntaxError("Line %d: No name in data declaration" 
                        % line_number)

            adt = True
            adt_name = tokens[1].replace(":", BLANK)
            
            if not valid_name(adt_name):
                raise SyntaxError("Line %d: name declaration must start with uppercase" 
                        % line_number)

            code += gen_type(adt_name) + NL

    
        
        if tokens[0] not in [BLANK, DATA]:
            adt = False

        if adt and len(tokens) > len(INDENT):
            if line.count("(")  + line.count(")") != 2:
                raise SyntaxError("Line %d: unbalanced parenthesis" 
                        % line_number) 

            constructor = line.replace(NL, BLANK).split("(")
            name = constructor[0].replace(SPACE,BLANK)
            
            if not valid_name(name):
                raise SyntaxError("Line %d: constructor declaration must start with uppercase" 
                        % line_number) 

            parameters = []

            if len(constructor) > 1:
                parameters = constructor[1].replace(")",BLANK).split(",")
                parameters = list(filter(lambda s: s != BLANK, parameters))

                if line.count(",") not in [0, len(parameters) - 1]:
                    raise SyntaxError("Line %d: bad constructor parameconstructor parameters " 
                            % line_number)
 
            code += gen_constructor(name, adt_name, parameters)

        if not adt:
            code += line

        line_number += 1


    return code


if __name__ == "__main__":
    source = fileinput.input()
    code = preprocessor(source) 
    print(code)

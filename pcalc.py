import sys
import math as m
import re

# TODO add strict standards for how errors are handled, for example sysexit or return or raise
numbers = []
restricted = ["N", "kg", "s", "m", "m/s", "m/s^2",
              "s^2", "kgm/s^2", "cos", "sin", "tan", "sqrt", "J"]
prep_vars = ["g", "pi", "e"]  # TODO Integrate prep vars into program


# TODO standard for equation input that is easy to specifically match space between num-unit, trig-num,
#  and every operator


class PhysicsValue:
    """Class to store the value and unit of a number, with the option to add a descriptor
    \n   num: value of the number
    \n   unit: unit of the number
    \n   name: descriptor of the number, auto generated typically by the unit
    \n   returns: PhysicsValue object
    """

    def __init__(self, num, unit, name=None):
        self.val = num
        if type(unit) == str:
            self.unit = Unit(unit)
        elif type(unit) == Unit:
            self.unit = unit
        elif unit is None:
            self.unit = Unit(None)
        else:
            print("Error: Unit must be a string or a Unit object")
            sys.exit(1)
        if unit is None:
            self.name = "unk: " + str(hash)

        self.name = name
        if self.name is None:
            self.name = self.unit.determine() + ": " + str(hash)

    # Fix operators to work with units

    def __repr__(self):
        if self.unit.combined is None:
            return str(self.val)
        return str(self.val) + " " + self.unit.combined

    def __add__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return PhysicsValue(self.val + other.val, self.unit + other.unit)

    def __sub__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return PhysicsValue(self.val - other.val, self.unit + other.unit)

    def __mul__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return PhysicsValue(self.val * other.val, self.unit * other.unit)

    def __truediv__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return PhysicsValue(self.val / other.val, self.unit / other.unit)

    def __pow__(self, other):
        return PhysicsValue(self.val ** other.val, self.unit ** other.val)

    def __eq__(self, other):
        # TODO add code to find missing variable and solve for it
        pass

    def cos(self):
        return PhysicsValue((m.cos(m.radians(self.val))), self.unit)

    def sin(self):
        return PhysicsValue((m.sin(m.radians(self.val))), self.unit)

    def tan(self):
        return PhysicsValue((m.tan(m.radians(self.val))), self.unit)

    def sqrt(self):
        return PhysicsValue((m.sqrt(self.val)), self.unit)  # TODO Add square root function on unit

    def get_num(self):
        return float(self.val)

    def get_unit(self):
        return str(self.unit)

    def get_component(self):
        return str(self.unit.component)


# Function to interpret a string as an equation using regex
# TODO add error handling in case of invalid input in the equation function
# TODO Add error handling for invalid units / unit combinations / variables - evaluate rest of equation if possible


class PhysicsVar(PhysicsValue):
    """Class that inherits from physicsval, and provides a way to store variables.
        \nIn the future, this class will be able to store results of functions
        \nand replace as values in an equation"""

    def __init__(self, num, unit, name):
        if name is None:
            print("Error: Variable must have a name")
            sys.exit(1)
        elif type(name) != str:
            print("Error: Variable name must be a string")
            sys.exit(1)
        elif name in numbers or name in restricted:
            print("Error: Variable name already exists")
            sys.exit(1)
        super().__init__(num, unit, name)
        numbers.append(self)

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if type(other) == str:
            return self.name == other
        elif self.name == other.name:
            return True
        else:
            return False

    def substitute(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        self.val = other.val
        self.unit = other.unit
        self.name = other.name
        return self  # Integrate this with equation function


def calc(eq, prefix=None):
    ''' Function to calculate the value of an equation \n   eq: string of equation to be calculated \n   returns:
    float of the value of the equation \n   variables must be in the form of a string with no spaces, and listed in
    the nums list - look at physicsvar class for more info
    '''

    priority = re.compile(
        r'(?P<prefix>cos|sin|tan|v|sqrt|d+(?:\.\d+)?)?(?P<parent>\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\))')
    # TODO detect square roots and other functions before parenthesis with non capturing group
    # TODO add support to multiply numbers prior to a parenthesis or variable
    # TODO add support for equal sign assignment of variables and calculations of variables
    for x in priority.findall(eq):
        if x[0] is None:
            eq = eq.replace(''.join(x), str(calc(x[1][1:-1])))
        else:  # TODO why are there false flags for the prefix
            eq = eq.replace(''.join(x), str(calc(x[1][1:-1], x[0])))
    for x in numbers:  # TODO add support for variables
        if x in eq:
            eq = eq.replace(x, str(x))
    print(eq)
    # fix to not need the space in between the operator and stuff
    # TODO Possibly re-engineer the process of extracting data
    # Don't know yet

    pattern = r"(?P<numbers>\d+(?:\.\d+)?)\s*(?P<units>(?:N|kg|m|s|J|\^2)*/?(?:N|kg|m|s|J|\^2)+)?\s*(?P<arithmetic>[" \
              r"-+*/][*]*)?\s*"
    # Pattern requires exponents to be written as **, not ^
    extracted_data = []
    matches = re.findall(pattern, eq)
    for group in matches:
        # find the named group that matched
        for x in group:
            if x == group[0]:
                if group[1] == "":
                    extracted_data.append(PhysicsValue(float(group[0]), None))
                else:
                    extracted_data.append(
                        PhysicsValue(float(group[0]), group[1]))
            elif x == group[2]:
                if group[2] == "":
                    pass
                elif group[2] == "^":
                    extracted_data.append("**")
                else:
                    extracted_data.append(group[2])
    print(extracted_data)
    # combines all operations in extracted_data into one final result
    operator = ["**", "*", "/", "+", "-"]
    result = None
    for y in operator:
        while extracted_data.count(y) > 0:
            x = extracted_data[extracted_data.index(y)]
            pos = extracted_data.index(x)
            if x == y:
                if x == "**":
                    x = "__pow__"
                elif x == "*":
                    x = "__mul__"
                elif x == "/":
                    x = "__truediv__"
                elif x == "+":
                    x = "__add__"
                elif x == "-":
                    x = "__sub__"
                else:
                    break
                value1 = extracted_data[pos - 1]
                value2 = extracted_data[pos + 1]
                result = value1.__getattribute__(x)(value2)
                extracted_data[extracted_data.index(value1)] = result
                extracted_data.remove(extracted_data[pos])
                extracted_data.remove(value2)
    if result is None:
        result = extracted_data[0]
    if prefix is not None and prefix != "":
        prefix = prefix.lower()
        if prefix == "v":
            prefix = "sqrt"
        result = result.__getattribute__(prefix)()
    return result


# Class to store the unit of a number, with the option to add a descriptor


def parse_unit(unit):
    # print(unit)
    units = re.compile(r'(?!None)(N|kg|m|s|J|\^2)')
    if unit == None:
        return None, None
    if "/" in unit:
        unit = unit.split("/")
        numerator = units.findall(unit[0])
        denominator = units.findall(unit[1])
    else:
        numerator = units.findall(unit)
        denominator = []
    # print(numerator, denominator)
    numerator.sort()
    denominator.sort()
    for x in numerator:
        match x:
            case "^2":
                numerator[numerator.index(
                    x)] = numerator[numerator.index(x) - 1]
            case "N":
                numerator.remove(x)
                numerator += ("m", "kg")
                denominator += ("s", "s")
            case "J":
                numerator.remove(x)
                numerator += ("kg", "m", "m")
                denominator += ("s", "s")
            case _:
                pass
    for x in denominator:
        match x:
            case "^2":
                denominator[denominator.index(
                    x)] = denominator[denominator.index(x) - 1]
            case "N":
                denominator.remove(x)
                denominator += ("m", "kg")
                numerator += ("s", "s")
            case "J":
                denominator.remove(x)
                denominator += ("m", "m", "kg")
                numerator += ("s", "s")
            case _:
                pass
    if denominator == '' or denominator is None or denominator == []:
        denominator = None
    elif numerator == denominator:
        numerator = None
        denominator = None
    return numerator, denominator


class Unit:
    """class to store the unit of a number, evaluate for validity, and combine units\n
    unit: string of the unit to be stored, using the following format:\n
    N, kg, m, s, J, or ^2\n
    Can be combined with / to represent a fraction\n
    Example: N/kg, m/s^2, J/N, etc.\n
    combined = string of the combined unit\n
    component = suspected component of the equation\n
    """

    def __init__(self, unit):
        self.numerator, self.denominator = parse_unit(unit)
        self.combined = self.combine_units()
        self.component = self.determine()

    def __str__(self):
        # TODO find and squash bug that causes repeated units
        return self.combined

    def combine_units(self):
        if self.denominator is None:
            if self.numerator is None:
                return ""
            return ''.join(self.numerator)
        self.numerator.sort()
        self.denominator.sort()
        # Remove common elements
        for i in self.numerator:
            if i in self.denominator:
                self.numerator.remove(i)
                self.denominator.remove(i)
        for i in self.denominator:
            if i in self.numerator:
                self.denominator.remove(i)
                self.numerator.remove(i)

        # print(self.numerator, self.denominator)
        # Check if list is empty
        if self.denominator is None or self.denominator == '' or self.denominator == []:
            if self.numerator is None or self.numerator == '' or self.numerator == []:
                return ""
            return ''.join(self.numerator)
        elif (self.numerator == ["kg", "m", "m"]) & (self.denominator == ["s", "s"]):
            return "J"
        elif (self.numerator == ["kg", "m"]) & (self.denominator == ["s", "s"]):
            return "N"
        else:
            return ''.join(self.numerator) + "/" + ''.join(self.denominator)

    # Determine the type of unit

    # TODO Fix comparison / arithmetic to work with "" instead of none
    def determine(self):
        if self.combined == "N":
            return ("force")
        elif self.combined == "kgm":
            return ("position")
        elif self.combined == "kgm/s":
            return ("momentum")
        elif self.combined == "kgm/s^2":
            return ("acceleration")
        elif self.combined == "m/s":
            return ("velocity")
        elif self.combined == "J":
            return ("energy")
        elif self.combined == "kg":
            return ("mass")
        elif self.combined == "m":
            return ("displacement")
        elif self.combined == "s":
            return ("time")
        else:
            return ("unknown")

    def get_nume(self):
        if self.numerator is None:
            return ""
        elif type(self.numerator) == list:
            return ''.join(self.numerator)
        elif type(self.numerator) == str:
            return self.numerator

    def get_deno(self):
        if self.denominator is None:
            return ""
        elif type(self.denominator) == list:
            return ''.join(self.denominator)
        elif type(self.denominator) == str:
            return self.denominator

    def __mul__(self, other):
        if other is None:
            return self
        nums = self.get_nume() + other.get_nume()
        dens = self.get_deno() + other.get_deno()
        return Unit(nums + "/" + dens)

    def __truediv__(self, other):
        if other is None:
            return self
        nums = self.get_nume() + other.get_deno()
        dens = self.get_deno() + other.get_nume()
        return Unit(nums + "/" + dens)

    def __add__(self, other):
        if other is None:
            return self
        elif self.combine_units() == "":
            return other
        elif other is not None:
            if self.combine_units() == other.combine_units():
                return self
            else:
                raise ValueError("Units do not match")

    def __pow__(self, other):
        if other == 0:
            return Unit(" ")
        elif other == 1:
            return self
        elif other == 2:
            return Unit((self * self))  # TODO fix this


# TODO engineer the scope of this class, including possibility of evaluating the equation to a possible equation
#  template


class KinematicsEquation:  # TODO brainstorm how we will do this lol
    def __init__(self):
        self.variables = []
        self.parse()

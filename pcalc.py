import sys
import math as m
import re

# Class to store the value and unit of a number, with the option to add a descriptor

nums = []


class PhysicsValue:
    def __init__(self, num, unit, name=None):
        self.val = num
        if type(unit) == str:
            self.unit = Unit(unit)
        elif type(unit) == Unit:
            self.unit = unit
        elif unit == None:
            self.unit = Unit(None)
        else:
            print("Error: Unit must be a string or a Unit object")
            sys.exit(1)
        if unit == None:
            self.name = "unk: " + str(hash)

        self.name = name
        if self.name == None:
            self.name = self.unit.determine() + ": " + str(hash)
    # Fix operators to work with units

    def __repr__(self):
        if self.unit.combined == None:
            return (str(self.val))
        return (str(self.val) + " " + self.unit.combined)

    def __add__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return (PhysicsValue(self.val + other.val, self.unit + other.unit))

    def __sub__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return (PhysicsValue(self.val - other.val, self.unit + other.unit))

    def __mul__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return (PhysicsValue(self.val * other.val, self.unit * other.unit))

    def __truediv__(self, other):
        if type(other) == int | float:
            other = PhysicsValue(other, None)
        return (PhysicsValue(self.val / other.val, self.unit / other.unit))

    def __pow__(self, other):
        return (PhysicsValue(self.val ** other.val, self.unit ** other.val))

    def __eq__(self, other):
        # TODO add code to find missing variable and solve for it
        pass

    def cos(self):
        return (m.cos(m.radians(self.val)))

    def sin(self):
        return (m.sin(m.radians(self.val)))

    def tan(self):
        return (m.tan(m.radians(self.val)))

    def sqrt(self):
        return (m.sqrt(self.val))

    def get_num(self):
        return (float(self.val))

    def get_unit(self):
        return (str(self.unit))

    def get_component(self):
        return (str(self.unit.component))

# Function to interpret a string as an equation using regex


def calc(eq):

    priority = re.compile(r'\((?:[^()]+|\((?:[^()]+|\([^()]*\))*\))*\)') # TODO add support for nested parenthesis
    # TODO add better support for variables, and add support to multiply numbers prior to a parenthesis or variable
    for x in priority.findall(eq):
        eq = eq.replace(x, str(calc(x[1:-1])))
    for x in nums:
        if x in eq:
            eq = eq.replace(x, str(x))
    print(eq)
    pattern = r"(?P<numbers>\d+(?:\.\d+)?)\s*(?P<units>(?<!cos|sin|tan)(?:N|kg|m|s|J|\^2)*/?(?:N|kg|m|s|J|\^2)+)?\s*(?P<trig>cos|sin|tan)?\s*(?P<trig_num>\d+(?:\.\d+)?)?\s*(?P<arithmetic>[-+*/][*]*)?\s*" #fix to not need the space in between the operator and stuff
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
                if group[3] == "":
                    pass
                elif group[3] != "":
                    temp = PhysicsValue(float(group[3]), None)
                    print(temp)
                    if group[0] == "":
                        extracted_data.append(PhysicsValue(1, None))
                    extracted_data.append("*")
                    extracted_data.append(PhysicsValue(getattr(temp, group[2])(), None))
                else:
                    pass
            elif x == group[4]:
                if group[4] == "":
                    pass
                elif group[4] == "^":
                    extracted_data.append("**")
                else:
                    extracted_data.append(group[4])
    # print(extracted_data)
    # combine all operations in extracted_data into one final result
    operator = ["**", "*", "/", "+", "-"]
    # Fix to operate one operation at a time

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
                value1 = extracted_data[pos-1]
                value2 = extracted_data[pos+1]
                result = value1.__getattribute__(x)(value2)
                extracted_data[extracted_data.index(value1)] = result
                extracted_data.remove(extracted_data[pos])
                extracted_data.remove(value2)

        # if extracted_data
        # operation = extracted_data[]
        # value = extracted_data[i+1]
        # result = result.__getattribute__(operation)(value)
    return (result)
# Class to store the unit of a number, with the option to add a descriptor


class Unit:
    def __init__(self, unit):
        self.numerator, self.denominator = self.parse_unit(unit)
        self.combined = self.combine_units()
        self.component = self.determine()

    def __str__(self):
        return(self.combined) # TODO find and squash bug that causes repeated units
    
    def parse_unit(self, unit):
        #print(unit)
        units = re.compile(r'(?!None)(N|kg|m|s|J|\^2)')
        if unit == None:
            return (None, None)
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
        if denominator == '' or denominator == None or denominator == []:
            denominator = None
        elif numerator == denominator:
            numerator = None
            denominator = None
        return (numerator, denominator)
    # Combine the numerator and denominator lists into a single string

    def combine_units(self):
        if self.denominator == None:
            if self.numerator == None:
                return ("")
            return (''.join(self.numerator))
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
        if self.denominator == None or self.denominator == '' or self.denominator == []:
            if self.numerator == None or self.numerator == '' or self.numerator == []:
                return ("")
            return (''.join(self.numerator))
        elif (self.numerator == ["kg", "m", "m"]) & (self.denominator == ["s", "s"]):
            return ("J")
        elif (self.numerator == ["kg", "m"]) & (self.denominator == ["s", "s"]):
            return ("N")
        else:
            return (''.join(self.numerator) + "/" + ''.join(self.denominator))
    # Determine the type of unit

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
        if self.numerator == None:
            return ("")
        elif type(self.numerator) == list:
            return (''.join(self.numerator))
        elif type(self.numerator) == str:
            return (self.numerator)
    
    def get_deno(self):
        if self.denominator == None:
            return ("")
        elif type(self.denominator) == list:
            return (''.join(self.denominator))
        elif type(self.denominator) == str:
            return (self.denominator)

    def __mul__(self, other):
        if other == None:
            return (self)
        nums = self.get_nume() + other.get_nume()
        dens = self.get_deno() + other.get_deno()
        return Unit(nums + "/" + dens)

    def __truediv__(self, other):
        if other == None:
            return (self)
        nums = self.get_nume() + other.get_deno()
        dens = self.get_deno() + other.get_nume()
        return Unit(nums + "/" + dens)
    
    def __add__(self, other):
        if other == None:
            return (self)
        elif other != None:
            if self.combine_units() == other.combine_units():
                return (self)
            else:
                raise ValueError("Units do not match")

    def __pow__(self, other):
        if other == 0:
            return (Unit(" "))
        elif other == 1:
            return (self)
        elif other == 2:
            return (Unit((self * self))) # TODO fix this


class KinematicsEquation: # TODO brainstorm how we will do this lol
    def __init__(self):
        self.variables = []
        self.parse()

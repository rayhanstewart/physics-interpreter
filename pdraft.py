# Physics Interpreter 1.1
# Much better in every way, though simple for now and not very customizable (yet)

import sys
import math as m
import re
from dataclasses import dataclass


# Starting with creating data classes to generate units
@dataclass
class Unit:
    core: str  # Radians or meters
    dist: int
    sec: int
    kg: int

    # Every int means the amount of times of that unit in the total unit
    # For example, 1 m/s would be Unit("m", 1, 1, 0)

    def __repr__(self):
        return f"{self.core}^{self.dist} s^{self.sec} kg^{self.kg}"

    def get_unit(self):
        for x in units:
            if units[x] == self:
                return x
        return self.__repr__()

# TODO Research radians to meters conversion, and how to handle radians in general
units = {  # All the units that can be used
    "none": Unit("m", 0, 0, 0),
    "m": Unit("m", 1, 0, 0),
    "s": Unit("m", 0, 1, 0),
    "kg": Unit("m", 0, 0, 1),
    "rad": Unit("rad", 1, 0, 0),
    "m/s": Unit("m", 1, -1, 0),
    "m/s^2": Unit("m", 1, -2, 0),
    "kg*m": Unit("m", 1, 0, 1),
    "kg/m": Unit("m", -1, 0, 1),
    "kg*m/s": Unit("m", 1, -1, 1),
    "Newton": Unit("m", 1, -2, 1),
    "Joule": Unit("m", 2, -2, 1),
    "Watt": Unit("m", 2, -3, 1),
    "rad/s": Unit("rad", 1, -1, 0),
    "rad/s^2": Unit("rad", 1, -2, 0),
    "kg*m^2": Unit("m", 2, 0, 1),
    "kg*m^2/s": Unit("m", 2, -1, 1),
    "kg*m^2/s^2": Unit("rad", 2, -2, 1),
    "Hz": Unit("rad", 0, -1, 0),
}

arithmetic = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: x / y,
    "^": lambda x, y: x ** y,
    "sqrt": lambda x: x ** 0.5,
    "sin": lambda x: m.sin(x),
    "cos": lambda x: m.cos(x),
    "tan": lambda x: m.tan(x),
    "=": "equals",
}


class Physics_Num:
    def __init__(self, value, unit: Unit):
        self.value = value
        self.unit = unit

    def __repr__(self):
        return f"{self.value} {self.unit.get_unit()}"

    def get_unit(self):
        return self.unit.get_unit()

    def __add__(self, other):
        if self.unit == other.unit:
            return Physics_Num(self.value + other.value, self.unit)
        else:
            raise Exception("Units do not match")

    def __sub__(self, other):
        if self.unit == other.unit:
            return Physics_Num(self.value - other.value, self.unit)
        else:
            raise Exception("Units do not match")

    def __mul__(self, other):
        if self.unit.core == other.unit.core:
            return Physics_Num(self.value * other.value, Unit(self.unit.core, self.unit.dist + other.unit.dist,
                                                             self.unit.sec + other.unit.sec,
                                                             self.unit.kg + other.unit.kg))
        else:
            pass # TODO Handle this

    def __truediv__(self, other):
        if self.unit.core == other.unit.core:
            return Physics_Num(self.value / other.value, Unit(self.unit.core, self.unit.dist - other.unit.dist,
                                                             self.unit.sec - other.unit.sec,
                                                             self.unit.kg - other.unit.kg))
        else:
            pass

    def __pow__(self, other):
        if self.unit.core == other.unit.core:
            return Physics_Num(self.value ** other.value, Unit(self.unit.core, self.unit.dist * other.value,
                                                             self.unit.sec * other.value,
                                                             self.unit.kg * other.value))
        else:
            pass



class Physics_Var(Physics_Num):
    def __init__(self, name: str, value, unit: Unit):
        self.name = name
        self.placeholder = False
        if value == None:
            self.placeholder = True
        if self.placeholder:
            self.unit = unit
        else:
            super().__init__(value, unit)

    def __repr__(self):
        if self.placeholder:
            return f"{self.name}: {self.unit.get_unit()}"
        return f"{self.name}: {self.value} {self.unit.get_unit()}"


# Placeholder numbers with units
def globe(precision=3):
    all = {
        'pi': [m.pi, units["none"]],
        'g': [9.81, units["m/s^2"]],
        'c': [299792458, units["m/s"]],
        'e': [m.e, units["none"]],
        'h': [6.62607015e-34, units["kg*m^2/s"]],
        'k': [1.380649e-23, units["kg*m^2/s^2"]],
        'G': [6.67430e-11, units["none"]],
        'cycle': [2 * m.pi, units["rad"]],
    }
    for x in all:
        all[x][0] = round(all[x][0], precision)
        all[x] = Physics_Num(all[x][0], all[x][1])

    def summon(x):
        if x in all:
            return all[x]
        else:
            raise Exception(f"Unknown constant {x}")

    return summon


summon = globe()


class equation():
    # TODO Decide on list or dictionary for components, want to be able to set an expected unit for solving
    def __init__(self, components: dict):
        self.components = components

    def __repr__(self):
        # Return all components and their units
        return f"{self.components}"

    def solve(self, **kwargs):
        # Validate the right units before solving
        for x in self.components.keys():
            if x in arithmetic:
                self.components[x] = x
            elif x in kwargs:
                self.components[x] = kwargs[x]
            else:
                try:
                    self.components[x] = summon(x)
                except:
                    pass
        return self.components
        # Balance both sides and highlight the unknown variable or judge equality
        # Integrate calc function here


def init_workspace(name):
    # Workspace variable is a list of physics variables in a workspaces dictionary
    workspace = []
    workspaces.update({name: workspace})

    def store(pvar: Physics_Var):
        workspace.append(pvar)

    def get(name: str):
        for x in workspace:
            if x.name == name:
                return x
        raise Exception(f"Variable {name} not found")

    def get_all():
        return workspace

    return [store, get, get_all]


workspaces = {}


def set_space(name):
    global workspaces
    if name in workspaces:
        pass
    else:
        workspaces[name] = init_workspace(name)
    return workspaces[name][0], workspaces[name][1], workspaces[name][2]

def calc(equation: list):
    # Add error handling later
    # evaluate equation based on order of operations
    # First split at every arithmetic operator
    if "=" in equation: # Add unknown variable support later
        ind = equation.index("=")
        lhs = equation[:ind]
        rhs = equation[ind+1:]
        lhs = calc(lhs)
        rhs = calc(rhs)
        if lhs == rhs:
            return True
        else:
            return False
    equation = equation
    oops = ["(", "sqrt", "sin", "cos", "tan", "^", "*", "/", "+", "-"]
    for x in oops:
        if (x == "(") & ("(" in equation):
            start = equation.index("(")
            end = equation.index(")") # doesn't work for layered parenthesis
        if x in equation:
            ind = equation.index(x)
            if x in ["sqrt", "sin", "cos", "tan"]:
                temp = arithmetic[x](equation[ind+1])
                equation.pop(ind)
                equation[ind] = temp
            else:
                temp = arithmetic[x](equation[ind-1],equation[ind+1])
                equation.pop(ind)
                equation.pop(ind-1)
                equation[ind-1] = temp
    return equation[0]

store, get_var, all_vars = set_space("default")

# Some debugging driver stuff
store(Physics_Var("x", 5, units["m"]))
store(Physics_Var("y", 10, units["m"]))
print(all_vars())
print(summon('pi'))
print(summon('g').get_unit())
print(equation(
    {'F': get_var('x'), '=': None, 'm': get_var('y'), 'a': summon('g')}).solve())
print(calc([1, "+", 2, "*", 3, "^", 2]))

import sys
import pcalc as p
import math as m
import random as r
print(f' Answer: {p.calc("1m + 3m + 4m")}')
print(f' Answer: {p.calc("1m * 4m")}')
print(f' Answer: {p.calc("1m / 2m")}')
print(f' Answer: {p.calc("2m * 3m")}')
print(f' Answer: {p.calc ("(1m + 2m + 3m) / 10s")}')
#print(f' Answer: {p.calc("10m/s ** 2")} ') # ERROR FIX LATER
print(f' Answer: {p.calc("10m/s^2 * 2s")}')
print(f' Answer: {p.calc("10m/s^2 / 2m/s * 3m")}')
print(f' Answer: {p.calc("10kgm/s^2 + 2N")}')
# Generate test cases
print("Generating test cases")
'''testcases = []
units = ["m", "s", "kg", "m/s", "m/s2", "s2", "kgm/s2"]
operators = ["*", "/"]
for x in range(0, 10):
    testcases.append(p.calc(str(m.floor(r.random()*100)) + r.choice(units) + r.choice(operators) + str(m.floor(r.random()*100)) + r.choice(units)))

for x in testcases:
    print(x)'''
equations = []
print(p.calc("10 cos 30"))
print(p.calc("25kg * (0.5 * (10m/s^2 * 2s))")) #TODO ERROR FIX LATER
print( p.calc("20 * 20 * 20 + 2"))
while True:
    try:
        num = p.calc(input("\nEnter your calculation: \n"))
        print(str(num), "  ", num.get_component(), "\n")
    except KeyboardInterrupt:
        print(" Goodbye!")
        sys.exit(0)
    except:
        print("Error: Invalid input")
        continue
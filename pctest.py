import sys
import os
import pcalc as p

print(f' Answer: {p.calc("1m + 3m + 4m")}')
print(f' Answer: {p.calc("1m * 4m")}')
print(f' Answer: {p.calc("1m / 2m")}')
print(f' Answer: {p.calc("2m * 3m")}')
print(f' Answer: {p.calc("(1m + 2m + 3m) / 10s")}')
# print(f' Answer: {p.calc("10m/s ** 2")} ') # ERROR FIX LATER
print(f' Answer: {p.calc("10m/s^2 * 2s")}')
print(f' Answer: {p.calc("10m/s^2 / 2m/s * 3m")}')
print(f' Answer: {p.calc("10kgm/s^2 + 2N")}')
# Generate test cases

equations = []
print(p.calc("10 cos 30"))
print(p.calc("25kg * (0.5 * (10m/s^2 * 2s))"))  # TODO ERROR FIX LATER
print(p.calc("20 * 20 * 20 + 2"))
print(p.calc("10 + 10s"))
os.system("cls")
while True:
    try:
        num = p.calc(input("\nEnter your calculation: "))
        print(str(num), "  ", num.get_component(), "\n")
    except KeyboardInterrupt:
        print(" Goodbye!")
        sys.exit(0)
    finally:
        continue

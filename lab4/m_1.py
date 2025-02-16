import math
def degree_to_radian(degrees):
    return degrees * (math.pi / 180)

degrees = float(input("Input degree: "))
radians = degree_to_radian(degrees)
print("Output radian:", round(radians, 6))

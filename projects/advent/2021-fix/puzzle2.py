# input
data = []
with open("advent/input2.txt", "r") as file:
    for line in file:
        data.append(line.strip("\n"))

# process
commands = []
for i in data:
    temp = i.split()
    commands.append([temp[0], int(temp[1])])

# part one
position = 0
depth = 0
for i in commands:
    if i[0] == "down":
        depth += i[1]
    elif i[0] == "up":
        depth -= i[1]
    elif i[0] == "forward":
        position += i[1]
print(position*depth) # 2147104

# part two
position = 0
depth = 0
aim = 0
for i in commands:
    if i[0] == "down":
        aim += i[1]
    elif i[0] == "up":
        aim -= i[1]
    elif i[0] == "forward":
        position += i[1]
        depth += i[1] * aim
print(position*depth) # 2044620088
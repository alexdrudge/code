from operator import xor


input = []
with open("projects/advent/2020/day2/input.txt", "r") as file:
    for line in file:
        input.append(line.strip("\n").split(" "))

for i, data in enumerate(input):
    input[i][0] = data[0].split("-")
    input[i][0][0] = int(data[0][0])
    input[i][0][1] = int(data[0][1])
    input[i][1] = data[1][0]

total = 0
for i, data in enumerate(input):
    if (data[2][data[0][0]-1] == data[1]) ^ (data[2][data[0][1]-1] == data[1]):
        total += 1

print(total)

## 335
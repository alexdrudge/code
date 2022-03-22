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
    count = 0
    for j, letter in enumerate(data[2]):
        if data[1] == letter:
            count += 1
    if data[0][0] <= count <= data[0][1]:
        total += 1

print(total)

## 591
data = []
with open("projects/advent/2020/day1/input.txt", "r") as file:
    for line in file:
        data.append(int(line.strip("\n")))

difference = set()
for i in range(len(data)):
    diff = 2020 - data[i]
    if diff in difference:
        print(diff * data[i])
    difference.add(data[i])

## 197451
data = []
with open("projects/advent/2020/day1/input.txt", "r") as file:
    for line in file:
        data.append(int(line.strip("\n")))

pairs = {}
for i in range(len(data)-1):
    for j in range(i+1,len(data)):
        pairs[data[i]+data[j]] = [data[i], data[j]]

for i in range(len(data)):
    diff = 2020 - data[i]
    if diff in pairs:
        print(data[i] * pairs[diff][0] * pairs[diff][1])
        print(data[i] , pairs[diff][0] , pairs[diff][1])

## 138233720
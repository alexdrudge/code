# input
data = []
with open("advent/input1.txt", "r") as file:
    for line in file:
        data.append(int(line.strip("\n")))

# part one
count = 0
for i in range(1,len(data)):
    if data[i] > data[i-1]:
        count += 1
print(count) # 1342

# part two
count = 0
for i in range(3,len(data)):
    if data[i] > data[i-3]:
        count += 1
print(count) # 1378
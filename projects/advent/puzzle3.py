# input
def get_data():
    data = []
    with open("advent/input3.txt") as file:
        for line in file:
            data.append(line.strip("\n"))
    return data

# process
def count_digits(data):
    counts = []
    if len(data) == 0:
        return 0
    length = len(data[0])
    for i in range(length):
        counts.append([0, 0])
    for i in data:
        for j, bit in enumerate(i):
            if bit == "0":
                counts[j][0] += 1
            elif bit == "1":
                counts[j][1] += 1
    return counts

# part one
def calc_power_consumption(data):
    counts = count_digits(data)
    gamma = ""
    epsilon = ""
    length = len(data[0])
    for i in range(length):
        if counts[i][0] >= counts[i][1]:
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"
    print(int(gamma, 2) * int(epsilon, 2)) # 4001724

# part two
def calc_life_support(data):
    oxygen = ""
    ratings1 = data
    co2 = ""
    ratings2 = data
    length = len(data[0])
    for i in range(length):
        temp = []
        counts = count_digits(ratings1)
        for byte in ratings1:
            if counts[i][0] > counts[i][1]:
                if byte[i] == "0":
                    temp.append(byte)
            elif counts[i][0] <= counts[i][1]:
                if byte[i] == "1":
                    temp.append(byte)
        ratings1 = temp[:]
        temp = []
        counts = count_digits(ratings2)
        for byte in ratings2:
            if counts[i][0] > counts[i][1]:
                if byte[i] == "1":
                    temp.append(byte)
            elif counts[i][0] <= counts[i][1]:
                if byte[i] == "0":
                    temp.append(byte)
        ratings2 = temp[:]
        if len(ratings1) == 1:
            oxygen = ratings1[0]
        if len(ratings2) == 1:
            co2 = ratings2[0]
    print(int(oxygen, 2) * int(co2, 2)) # 587895

if __name__ == "__main__":
    data = get_data()
    calc_power_consumption(data)
    calc_life_support(data)
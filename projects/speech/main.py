import os

def main():
    # retrieve list of all text files that need to be processed
    file_names = os.listdir("project/full_transcript")
    file_results = []
    for path in file_names:
        file_data = file_import(path)
        time_total, utterance_total, utterance_mean, pause_total, pause_mean, utterance_percentage, pause_percentage = calc_mean(file_data)
        word_total, word_different, word_average, words = calc_words(file_data)
        words_export(path, words)
        file_results.append([path, time_total, utterance_total, utterance_mean, pause_total, pause_mean, utterance_percentage, pause_percentage, word_total, word_different, word_average])
    file_export(file_results)

def file_import(path):
    # import the data from the file
    path = "project/full_transcript/" + path
    file_content = open(path, "r")
    file_temp = file_content.readlines()
    file_content.close()
    # split the data up into a nested list and remove any modifiers
    file_data = []
    for line in file_temp:
        file_data.append(line.strip("\n").split("\t"))
    # change the data types to floats and the string into a list
    for i in range(len(file_data)):
        file_data[i][0] = float(file_data[i][0])
        file_data[i][1] = float(file_data[i][1])
        file_data[i][2] = file_data[i][2].split(" ")
    return file_data

def file_export(file_results):
    file_content = open("project/results.txt", "w")
    for line in file_results:
        for i in line:
            file_content.write(str(i) + "\t")
        file_content.write("\n")
    file_content.close()

def words_export(path, words):
    path = "project/word_counts/" + path
    file_content = open(path, "w")
    for line in words:
        for i in line:
            file_content.write(str(i) + "\t")
        file_content.write("\n")
    file_content.close()

def calc_mean(file_data):
    utterance = 0
    total = 0
    utterance_total = 0
    for line in file_data:
        for i in line[2]:
            spoken = False
            if i[0] != "[":
                spoken = True
            elif i == "[speech]" or i == "[foreign]" or i == "[filler]":
                spoken = True
        if spoken:
            utterance = line[1] - line[0]
            utterance_total += utterance
            total += 1
    utterance_mean = utterance_total / total
    time_total = file_data[len(file_data) - 1][1] - file_data[0][0]
    pause_total = time_total - utterance_total
    pause_mean = pause_total / (total - 1)
    utterance_percentage = utterance_total / time_total
    pause_percentage = pause_total / time_total
    return round(time_total, 2), round(utterance_total, 2), round(utterance_mean, 2), round(pause_total, 2), round(pause_mean, 2), round(utterance_percentage, 2), round(pause_percentage, 2)

def calc_words(file_data):
    word_total = 0
    word_different = 0
    total = 0
    words = []
    counted = False
    for line in file_data:
        total += 1
        for i in line[2]:
            counted = False
            if i != "":
                if (i[0] != "[") and ("@" not in i):
                    word_total += 1
                    for j in words:
                        if i == j[0]:
                            counted = True
                            j[1] = j[1] + 1
                    if not counted:
                        words.append([i, 1])
                        word_different += 1
    word_average = word_total / total
    return word_total, word_different, round(word_average, 2), words

if __name__ == "__main__":
    main()
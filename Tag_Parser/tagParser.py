# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json as js

def tag_analysis():
    ret = []
    with open('tags.txt', mode = 'r') as file:
        json = file.read()
        ind = 0
        while ind < len(json):
            str = ""
            while json[ind] != "}":
                str += json[ind]
                ind += 1
            ind += 2
            str += '}'
            dict1 = js.loads(str)
            ret.append([dict1['name'], dict1['usageCount']])
    return ret
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import csv

    arr = tag_analysis()
    arr.sort(key = lambda x: x[0].lower())
    with open('tags.csv', mode = 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Tag Name", "Number of Related Assets"])
        writer.writerows(arr)
        print(len(arr))


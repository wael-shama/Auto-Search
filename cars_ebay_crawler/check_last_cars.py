import csv

def lastAdded(filename):
    import csv
    with open('./cars/' + filename + '.csv', newline='') as f:
        reader = csv.reader(f)
        line = 0
        first=[]
        for row in reader:
            if line:
                first = row
                break
            line +=1
        if first:
            first = first[2]
    return first


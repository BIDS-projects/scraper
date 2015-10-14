import csv

with open("data-science-websites.csv", 'rb') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)
    for row in reader:
        print("{}, {}").format(row[0],row[1])

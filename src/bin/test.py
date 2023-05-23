import csv

file = r'sequence.csv'
with open(file) as fh:
    reader = csv.reader(fh)
    angles = list(reader)[0]
    angles = [int(ang.strip()) for ang in angles]



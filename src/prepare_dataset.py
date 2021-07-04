
import numpy as np
import csv
import pprint


num_rows = 12
drop_rows = [10, 11]
num_columns = 8
drop_columns = [5, 6, 7]

with open('../data/example/data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    #dataset = list(reader)
    dataset_str = []
    for row in reader:
        dataset_str.append(row[:])

pp = pprint.PrettyPrinter(width=100, compact=True)

pp.pprint(dataset_str)
print('\n')

dataset = [[float(col) for col in row] for row in dataset_str]
pp.pprint(dataset)



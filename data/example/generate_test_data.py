
# Prepare example data

import numpy as np
import csv
import pandas as pd

num_rows = 12
drop_rows = [10, 11]
num_columns = 8
drop_columns = [5, 6, 7]

rows = []
rng = np.random.default_rng()

print('\nExample data, as generated...')

with open('./data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    for i in range(0, num_rows):
        row = []
        row.append(np.float32(rng.random()))
        row.append(np.float32(rng.random()))
        row.append(np.float32(rng.random()))

        row.append(np.float32(2.0 * row[1]))
        row.append(np.float32(3.0 * row[2] + 2.0))

        row.append(np.float32(0.0))
        row.append(np.float32(1.0))
        row.append(np.float32(2.0))

        rows.append(row)
        writer.writerow(row)

print(*rows, sep = "\n")

print('\nExample data, CSV readback, dropped rows and columns...')

with open('./data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    data_df = pd.DataFrame(list(reader)).drop(drop_rows).drop(columns=drop_columns)

print(data_df)


# Unaccelerated version of feature reduction 

drop_rows = [10, 11]
drop_columns = [5, 6, 7]

with open('../data/example/data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    data_df = pd.DataFrame(list(reader)).drop(drop_rows).drop(columns=drop_columns)

print(data_df)


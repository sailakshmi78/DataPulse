from data_engine.reader import read_dataset


file_path = "datasets/sample/test.csv"

data = read_dataset(file_path)

print("Dataset loaded successfully!")
print("Rows:", len(data))
print("Columns:", len(data.columns))
print("Column names:", list(data.columns))
print(data)
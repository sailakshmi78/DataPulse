from data_engine.reader import read_dataset
from data_engine.profiler import profile_dataset


file_path = "datasets/sample/test.csv"

data = read_dataset(file_path)

profile = profile_dataset(data)

print("Dataset profiling completed!")
print("Rows:", profile["row_count"])
print("Columns:", profile["column_count"])

for column, details in profile["columns"].items():
    print()
    print("Column:", column)
    print("Data Type:", details["data_type"])
    print("Missing:", details["missing_count"])
    print("Unique:", details["unique_count"])
    print("Duplicates:", details["duplicate_count"])
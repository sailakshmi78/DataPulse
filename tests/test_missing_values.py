from data_engine.reader import read_dataset
from algorithms.missing_value_detector import find_missing_values


file_path = "datasets/sample/missing_values.csv"

data = read_dataset(file_path)

missing_values = find_missing_values(data)

print("Missing-value detection completed!")
print("Missing columns:", len(missing_values))

for issue in missing_values:
    print()
    print("Column:", issue["column_name"])
    print("Missing count:", issue["missing_count"])
    print("Rows:", issue["rows"])
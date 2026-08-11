from data_engine.reader import read_dataset
from algorithms.range_detector import find_out_of_range


file_path = "datasets/sample/range_test.csv"

data = read_dataset(file_path)

issues = find_out_of_range(
    data,
    column="age",
    minimum=0,
    maximum=120
)

print("Range validation completed!")
print("Out-of-range values:", len(issues))

for issue in issues:
    print()
    print("Row:", issue["row_number"])
    print("Column:", issue["column_name"])
    print("Value:", issue["value"])
    print("Allowed range:", issue["minimum"], "-", issue["maximum"])

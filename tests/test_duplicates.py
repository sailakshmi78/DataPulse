from data_engine.reader import read_dataset
from algorithms.duplicate_detector import find_duplicates


file_path = "datasets/sample/duplicates.csv"

data = read_dataset(file_path)

duplicates = find_duplicates(data)

print("Duplicate detection completed!")
print("Duplicates found:", len(duplicates))

for duplicate in duplicates:
    print()
    print("Duplicate row:", duplicate["row_number"])
    print("Values:", duplicate["values"])
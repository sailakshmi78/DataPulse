from data_engine.reader import read_dataset
from services.validation_engine import run_validation


file_path = "datasets/sample/validation_test.csv"

data = read_dataset(file_path)

results = run_validation(data)

print("Validation engine completed!")

print()
print("Duplicate issues:", len(results["duplicates"]))
print("Missing-value issues:", len(results["missing_values"]))
print("Range issues:", len(results["range_issues"]))

for issue in results["duplicates"]:
    print()
    print("DUPLICATE:")
    print(issue)

for issue in results["missing_values"]:
    print()
    print("MISSING:")
    print(issue)

for issue in results["range_issues"]:
    print()
    print("RANGE:")
    print(issue)
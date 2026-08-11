from data_engine.processor import process_in_chunks


file_path = "datasets/sample/test.csv"

total_rows = 0
chunk_number = 0

for chunk in process_in_chunks(file_path, chunk_size=2):
    chunk_number += 1

    print()
    print("Chunk:", chunk_number)
    print(chunk)

    total_rows += len(chunk)

print()
print("Processing completed!")
print("Total rows processed:", total_rows)
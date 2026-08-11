import pandas as pd


def process_in_chunks(file_path, chunk_size=10000):
    """
    Read a large CSV file in chunks to avoid loading
    the entire dataset into memory at once.
    """

    chunks = pd.read_csv(
        file_path,
        chunksize=chunk_size
    )

    for chunk in chunks:
        yield chunk
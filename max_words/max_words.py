import os
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor


# Check for filepaths
def filepaths_check(paths):
    existing_paths = []
    for path in paths:
        existing_paths.extend(traverse_directory(path))
    return set(existing_paths)


# Check if path exists / check if there is a directory
def traverse_directory(path):
    found_filepaths = []
    if os.path.exists(path):
        if not os.path.isfile(path):
            print("Found a directory! Let's look for files in it")
            for root, dirs, files in os.walk(path):
                for file in files:
                    if file.split(".")[1] == "txt":
                        print(f"Found one more file for reading: {file}")
                        file_path = os.path.join(root, file)
                        found_filepaths.append(file_path)
            return found_filepaths
        else:
            return [path]


# Processing files in parallel
def files_processing(paths):
    overall_counter = Counter()

    with ThreadPoolExecutor() as executor:
        individual_counters = list(executor.map(word_counter, paths))

    for individual_counter in individual_counters:
        overall_counter.update(individual_counter)

    return overall_counter

# Counting words
def word_counter(path):
    with open(path, 'r') as file:
        words = file.read().lower().split()
    return Counter(words)

def main():
    if len(sys.argv) < 2:
        print("There's not enough arguments to run this script")
        sys.exit(1)

    try:
        N = int(sys.argv[1])
    except:
        print('N must be an integer')
        sys.exit(1)

    paths = sys.argv[2:]

    if not paths:
        print("No paths provided")
        sys.exit(1)

    existing_paths = filepaths_check(paths)

    words_amount = files_processing(existing_paths)
    for word, amount in words_amount.most_common(N):
        print(f"Word '{word}' occured '{amount}' times")


if __name__ == "__main__":
    main()

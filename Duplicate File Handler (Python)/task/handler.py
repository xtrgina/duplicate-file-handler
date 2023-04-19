import sys
import os
import hashlib
from collections import defaultdict
from os.path import join, getsize, splitext


class DuplicateFileHandler:
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.file_format = None
        self.files = defaultdict(set)
        self.hash_tables_by_size = defaultdict(dict)

    def scan_files(self):
        for root, dirs, files in os.walk(self.root_directory):
            for name in files:
                filepath = join(root, name)
                size = getsize(filepath)

                if self.file_format:
                    extension = splitext(name)[1]
                    if extension != "." + self.file_format:
                        continue
                self.files[size].add(filepath)

        return self.files

    def compute_hashes(self):
        for size, filepaths in self.files.items():
            hash_table = defaultdict(set)
            if len(filepaths) > 1:
                for filepath in filepaths:
                    with open(filepath, "rb") as f:
                        digest = hashlib.file_digest(f, "md5")
                    file_hash = digest.hexdigest()
                    hash_table[file_hash].add(filepath)
                self.hash_tables_by_size[size] = hash_table
        return self.hash_tables_by_size

    def delete_files(self, files):
        total_size = 0
        for file in files:
            total_size += getsize(file)
            os.remove(file)
        print(f"Total freed up space: {total_size} bytes")


class DuplicateFileHandlerApplication:
    def __init__(self, root_directory):
        self.handler = DuplicateFileHandler(root_directory)
        self.sorting_option = None
        self.duplicate_files = []

    def execute(self):
        self.handler.file_format = input("Enter file format: ")
        print("Size sorting options:\n1. Descending\n2. Ascending\n")
        while (sorting_option := int(input("Enter a sorting option: "))) not in [1, 2]:
            print("Wrong option")
        self.sorting_option = sorting_option
        self.print_equal_sizes()

        while (
            check_for_duplicates := input("\nCheck for duplicates? [yes/no]: ")
        ) not in ["yes", "no"]:
            print("Wrong option")
        if check_for_duplicates == "yes":
            self.print_equal_hashes()

        self.select_files_to_delete()

    def select_files_to_delete(self):
        prompt = "\nDelete files? [yes/no]: "
        while (delete_files := input(prompt)) not in ["yes", "no"]:
            print("Wrong option")

        if delete_files == "yes":
            files_to_delete = []
            file_numbers = self.read_file_numbers()
            for index, file in enumerate(self.duplicate_files):
                if index + 1 in file_numbers:
                    files_to_delete.append(file)
            self.handler.delete_files(files_to_delete)

    def read_file_numbers(self):
        file_numbers = []
        prompt = "\nEnter file numbers to delete: "
        while True:
            try:
                file_numbers = [int(x) for x in input(prompt).split()]
            except ValueError:
                print("\nWrong format")
                continue
            if not file_numbers:
                print("\nWrong format")
                continue
            for number in file_numbers:
                if not 1 <= number <= len(self.duplicate_files):
                    print("\nWrong format")
                    break
            else:
                break
        return file_numbers

    def print_equal_sizes(self):
        is_descending = True if self.sorting_option == 1 else False
        files = self.handler.scan_files()
        for size, filepaths in sorted(files.items(), reverse=is_descending):
            if len(filepaths) > 1:
                print(f"\n{size} bytes")
                for filepath in filepaths:
                    print(filepath)

    def print_equal_hashes(self):
        is_descending = True if self.sorting_option == 1 else False
        hash_tables_by_size = self.handler.compute_hashes()
        counter = 1
        for size, hash_table in sorted(
            hash_tables_by_size.items(), reverse=is_descending
        ):
            print(f"\n{size} bytes")
            for hash_, filepaths in hash_table.items():
                if len(filepaths) > 1:
                    print(f"Hash: {hash_}")
                    for filepath in filepaths:
                        print(f"{counter}. {filepath}")
                        self.duplicate_files.append(filepath)
                        counter += 1


def main():
    if len(sys.argv) != 2:
        print("Directory is not specified")
        sys.exit()
    app = DuplicateFileHandlerApplication(root_directory=sys.argv[1])
    app.execute()


if __name__ == "__main__":
    main()

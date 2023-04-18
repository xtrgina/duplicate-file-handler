import sys
import os
from os.path import join, getsize, splitext


class DuplicateFileHandler:
    @classmethod
    def validate_input_args(cls):
        if len(sys.argv) != 2:
            print("Directory is not specified")
            sys.exit()

    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.file_format = None
        self.sorting_option = None
        self.files = dict()

    def scan_files(self):
        for root, dirs, files in os.walk(self.root_directory):
            for name in files:
                filepath = join(root, name)
                size = getsize(filepath)

                if self.file_format:
                    extension = splitext(name)[1]
                    if extension != "." + self.file_format:
                        continue

                if size in self.files:
                    self.files[size].append(filepath)
                else:
                    self.files[size] = []
                    self.files[size].append(filepath)

    def print_duplicates(self):
        is_descending = True if self.sorting_option == 1 else False
        for size, filepaths in sorted(self.files.items(), reverse=is_descending):
            if len(filepaths) > 1:
                print(f"\n{size} bytes")
                for filepath in filepaths:
                    print(filepath)

    def display_UI(self):
        self.file_format = input("Enter file format: ")
        print("Size sorting options:\n1. Descending\n2. Ascending\n")
        while (sorting_option := int(input("Enter a sorting option: "))) not in [1, 2]:
            print("Wrong option")
        self.sorting_option = sorting_option


def main():
    DuplicateFileHandler.validate_input_args()
    handler = DuplicateFileHandler(root_directory=sys.argv[1])
    handler.display_UI()
    handler.scan_files()
    handler.print_duplicates()


if __name__ == "__main__":
    main()

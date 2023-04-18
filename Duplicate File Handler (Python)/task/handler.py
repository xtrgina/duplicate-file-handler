import sys
import os


def validate_input():
    if len(sys.argv) != 2:
        print("Directory is not specified")
        sys.exit()


def main():
    validate_input()
    scan_for_files(sys.argv[1])


def scan_for_files(root):
    for root, dirs, files in os.walk(root):
        for name in files:
            print(os.path.join(root, name))


if __name__ == "__main__":
    main()

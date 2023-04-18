import sys


def validate_input():
    if len(sys.argv) != 2:
        print("Directory is not specified")


def main():
    validate_input()


if __name__ == "__main__":
    main()

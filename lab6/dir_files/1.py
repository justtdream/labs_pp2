import os

def list_contents(path):
    try:
        all_items = os.listdir(path)
        only_dirs = [item for item in all_items if os.path.isdir(os.path.join(path, item))]
        only_files = [item for item in all_items if os.path.isfile(os.path.join(path, item))]

        print("Only dir:")
        print(only_dirs)

        print("\n Only files:")
        print(only_files)

        print("\n All elements:")
        print(all_items)
    except FileNotFoundError:
        print("Given path does not exist")
    except PermissionError:
        print("Don't allow")

# Example
path = input("Enter path: ")
list_contents(path)

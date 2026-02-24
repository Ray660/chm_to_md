from ui import select_folder
from extract import extract_all
from convert import convert_folder

def main():
    selected_folder = select_folder()
    if not selected_folder:
        print("Cancelled")
        return

    print(f"Selected folder: {selected_folder}")

    has_chm = extract_all(selected_folder)
    
    print("\nConverting HTML to MD...")
    convert_folder(selected_folder)
    
    print("\nDone!")

if __name__ == '__main__':
    main()

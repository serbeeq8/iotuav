import os

def rename_images(folder_path, base_name="name"):
    # Get a list of files in the folder
    files = os.listdir(folder_path)
    
    # Sort the files to ensure sequential numbering
    files.sort()
    
    # Initialize a counter
    count = 1
    
    for file in files:
        # Get the file extension
        file_extension = os.path.splitext(file)[1]
        
        # Define the new name
        new_name = f"{base_name}{count}{file_extension}"
        
        # Get the full file paths
        old_file = os.path.join(folder_path, file)
        new_file = os.path.join(folder_path, new_name)
        
        # Rename the file
        os.rename(old_file, new_file)
        
        # Increment the counter
        count += 1
    
    print(f"Renamed {count-1} files in {folder_path}")

# Example usage
folder_path = r'D:\IORT\output_folder'  # Replace with your folder path
rename_images(folder_path)

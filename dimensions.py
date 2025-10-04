from PIL import Image, ImageOps
import os

# Set your base directory (Archive folder)
# base_directory = r'C:\Users\Administrator\Desktop\IKMC 2025 Amina\KangarooQatar Sheets for results ikmc\Archive'
base_directory = r'C:\BBSheet\sources'

# Set output text file path
output_file = r"C:\Users\Administrator\Desktop\script\image_dimensions_report.txt"

# Initialize a dictionary to store dimensions and associated filenames
dimensions_dict = {}
processed_folders = set()

# Walk through all subdirectories in the base directory
for subdir, _, files in os.walk(base_directory):
    # Skip __MACOSX directories
    if '__MACOSX' in subdir:
        continue

    folder_name = os.path.basename(subdir)
    processed_folders.add(folder_name)

    # Check each .jpg file in the current subdirectory
    for filename in files:
        if filename.lower().endswith('.jpg') and not filename.startswith('._'):
            filepath = os.path.join(subdir, filename)
            try:
                with Image.open(filepath) as img:
                    # Apply EXIF-based auto-orientation
                    img = ImageOps.exif_transpose(img)
                    width, height = img.size
                    dimension = (width, height)

                    # Add the image to the corresponding dimension, including subfolder
                    if dimension not in dimensions_dict:
                        dimensions_dict[dimension] = []
                    dimensions_dict[dimension].append((filename, folder_name))

            except Exception as e:
                print(f"{filename}: Failed to read image ({e})")

# Save results to text file using utf-8 encoding
with open(output_file, 'w', encoding='utf-8') as f:
    f.write("\n\n\n\n\n")  # Add vertical space
    for dimension, filenames_folders in dimensions_dict.items():
        f.write(f"Dimension {dimension[0]}x{dimension[1]}:\n")
        for filename, folder in filenames_folders:
            f.write(f"  {filename} in folder '{folder}'\n")
        f.write("\n")

    f.write("Finished processing images.\n\n")

    # Folder summary
    f.write(f"Total number of unique folders: {len(processed_folders)}\n")
    f.write("Folder names:\n")
    for folder in sorted(processed_folders):
        f.write(f"  - {folder}\n")

print(f"✅ Results saved to: {output_file}")

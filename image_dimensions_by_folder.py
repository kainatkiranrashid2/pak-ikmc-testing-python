from PIL import Image, ImageOps
import os

# Set your base directory
# base_directory = r'C:\Users\Administrator\Desktop\IKMC 2025 Amina\KangarooQatar Sheets for results ikmc\Archive'
base_directory = r'C:\BBSheet\sources'

# Set the output file path
output_file = r'C:\Users\Administrator\Desktop\test-out\new-ikmc-testing-2025\new_image_dimensions_by_folder.txt'

# Dictionary to group images by folder
folder_dict = {}

print("📂 Starting to group images by folder...")

# Walk through all subdirectories
for subdir, _, files in os.walk(base_directory):
    if '__MACOSX' in subdir:
        continue

    folder_name = os.path.basename(subdir)
    for filename in files:
        if filename.lower().endswith('.jpg') and not filename.startswith('._'):
            filepath = os.path.join(subdir, filename)
            try:
                with Image.open(filepath) as img:
                    img = ImageOps.exif_transpose(img)
                    width, height = img.size

                    dpi = img.info.get('dpi', (None, None))
                    dpi_str = f"{dpi[0]}x{dpi[1]}" if dpi[0] else "Unknown DPI"

                    dimension_str = f"{filename} - {width}x{height} @ {dpi_str}"

                    if folder_name not in folder_dict:
                        folder_dict[folder_name] = []
                    folder_dict[folder_name].append(dimension_str)

                    print(f"✅ Processed: {filename} in '{folder_name}'")
            except Exception as e:
                print(f"⚠️ Failed: {filename} ({e})")

# Write the results to a text file
with open(output_file, 'w', encoding='utf-8') as f:
    for folder, files in folder_dict.items():
        f.write(f"📁 Folder: {folder}\n")
        for file_line in files:
            f.write(f"  {file_line}\n")
        f.write("\n")
    f.write("✅ Image dimension listing by folder completed.\n")

print(f"\n📄 Results saved to: {output_file}")

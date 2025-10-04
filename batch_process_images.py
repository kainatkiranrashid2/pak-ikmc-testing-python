import os
import requests
from PIL import Image

# Set the FastAPI endpoint
API_URL = "http://localhost:8000/process-file/"

# Default folder paths
default_folder_path_1 = r"C:\Users\Administrator\Desktop\Aminah\200dpi\864.2.XSM"
# default_folder_path_2 = r"C:\Users\Administrator\Desktop\25-new-folders\138"
default_folder_path_2 = r"C:\Users\Administrator\Desktop\test-out\01\97"
# default_folder_path_2 = r"C:\Users\Administrator\Desktop\test-out\01\102"

# Output logs
success_log = "successful_images.txt"
error_log = "failed_images.txt"

# Initialize counters and lists
total_count = 0
success_count = 0
error_count = 0
successful_images_by_folder = {}
failed_images_by_folder = {}

# === User Input Flow ===
use_default = input(
    f"Do you want to use a default folder path?\n1: {default_folder_path_1}\n2: {default_folder_path_2}\n(y/n): "
).strip().lower()

if use_default == 'y':
    folder_choice = input(f"Choose default path:\n1: {default_folder_path_1}\n2: {default_folder_path_2}\nEnter 1 or 2: ").strip()

    if folder_choice == '1':
        folder_path = default_folder_path_1
    elif folder_choice == '2':
        folder_path = default_folder_path_2
    else:
        print("Invalid choice. Using default path 1.")
        folder_path = default_folder_path_1

    # Ask if user wants to process all or one image
    mode = input("What do you want to do?\n1: Process all images\n2: Pick one image\nEnter 1 or 2: ").strip()

    if mode == '2':
        # List available images
        jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg") and not f.startswith("._")]

        if not jpg_files:
            print("No JPG files found in the selected folder.")
            exit()

        print("\nAvailable image files:")
        for idx, file in enumerate(jpg_files, start=1):
            print(f"{idx}. {file}")

        image_index = input("Enter the number of the image to process: ").strip()

        try:
            selected_file = jpg_files[int(image_index) - 1]
            file_path = os.path.join(folder_path, selected_file)
            folder_name = os.path.basename(folder_path)

            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    print(f"\n📤 Sending: {selected_file} ({width}x{height})")
            except Exception as e:
                print(f"\n📤 Sending: {selected_file} (⚠️ Could not read dimensions: {e})")

            total_count += 1

            try:
                response = requests.post(API_URL, params={"file_path": file_path})
                if response.status_code == 200:
                    success_count += 1
                    successful_images_by_folder.setdefault(folder_name, []).append(selected_file)
                    print(f"✅ Success: {selected_file}")
                else:
                    error_count += 1
                    failed_images_by_folder.setdefault(folder_name, []).append(
                        f"{selected_file} - Error: {response.status_code} - {response.text}"
                    )
                    print(f"❌ Error: {selected_file} - {response.status_code}")
            except Exception as e:
                error_count += 1
                failed_images_by_folder.setdefault(folder_name, []).append(
                    f"{selected_file} - Exception: {str(e)}"
                )
                print(f"⚠️ Exception: {selected_file} - {str(e)}")

        except (IndexError, ValueError):
            print("❌ Invalid image selection.")
            exit()

    elif mode == '1':
        print(f"\n📂 Starting to process all images from: {folder_path}")
        for root, _, files in os.walk(folder_path):
            folder_name = os.path.basename(root)
            for file in files:
                if file.lower().endswith(".jpg") and not file.startswith("._"):
                    file_path = os.path.join(root, file)
                    try:
                        with Image.open(file_path) as img:
                            width, height = img.size
                            print(f"📤 Sending: {file} ({width}x{height})")
                    except Exception as e:
                        print(f"📤 Sending: {file} (⚠️ Could not read dimensions: {e})")

                    total_count += 1
                    try:
                        response = requests.post(API_URL, params={"file_path": file_path})
                        if response.status_code == 200:
                            success_count += 1
                            successful_images_by_folder.setdefault(folder_name, []).append(file)
                            print(f"✅ Success: {file}")
                        else:
                            error_count += 1
                            failed_images_by_folder.setdefault(folder_name, []).append(
                                f"{file} - Error: {response.status_code} - {response.text}"
                            )
                            print(f"❌ Error: {file} - {response.status_code}")
                    except Exception as e:
                        error_count += 1
                        failed_images_by_folder.setdefault(folder_name, []).append(
                            f"{file} - Exception: {str(e)}"
                        )
                        print(f"⚠️ Exception: {file} - {str(e)}")

    else:
        print("❌ Invalid input. Please enter 1 or 2.")
        exit()

else:
    # Manual path
    folder_path = input("Please enter the folder path (e.g., C:\\Users\\...): ").strip()

    print(f"\n📂 Starting to process all images from: {folder_path}")
    for root, _, files in os.walk(folder_path):
        folder_name = os.path.basename(root)
        for file in files:
            if file.lower().endswith(".jpg") and not file.startswith("._"):
                file_path = os.path.join(root, file)
                try:
                    with Image.open(file_path) as img:
                        width, height = img.size
                        print(f"📤 Sending: {file} ({width}x{height})")
                except Exception as e:
                    print(f"📤 Sending: {file} (⚠️ Could not read dimensions: {e})")

                total_count += 1
                try:
                    response = requests.post(API_URL, params={"file_path": file_path})
                    if response.status_code == 200:
                        success_count += 1
                        successful_images_by_folder.setdefault(folder_name, []).append(file)
                        print(f"✅ Success: {file}")
                    else:
                        error_count += 1
                        failed_images_by_folder.setdefault(folder_name, []).append(
                            f"{file} - Error: {response.status_code} - {response.text}"
                        )
                        print(f"❌ Error: {file} - {response.status_code}")
                except Exception as e:
                    error_count += 1
                    failed_images_by_folder.setdefault(folder_name, []).append(
                        f"{file} - Exception: {str(e)}"
                    )
                    print(f"⚠️ Exception: {file} - {str(e)}")

# === Save Logs ===
with open(success_log, 'w', encoding='utf-8') as f:
    f.write(f"✅ Total successful: {success_count}\n\n")
    for folder, files in successful_images_by_folder.items():
        f.write(f"📁 Folder: {folder}\n")
        for file in files:
            f.write(f"  {file}\n")
        f.write("\n")

with open(error_log, 'w', encoding='utf-8') as f:
    f.write(f"❌ Total failed: {error_count}\n\n")
    for folder, files in failed_images_by_folder.items():
        f.write(f"📁 Folder: {folder}\n")
        for file in files:
            f.write(f"  {file}\n")
        f.write("\n")

# === Summary ===
print("\n📊 Summary:")
print(f"📸 Total files processed: {total_count}")
print(f"✅ Successful: {success_count}", f"❌ Failed: {error_count}")
print(f"📄 Logs saved to '{success_log}' and '{error_log}'")

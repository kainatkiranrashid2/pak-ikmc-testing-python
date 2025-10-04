import os
import requests
from PIL import Image
from datetime import datetime  # <-- Added for timestamps

API_URL = "http://localhost:3001/process-file/"
# ROOT_FOLDER = r"C:\Users\Administrator\Desktop\25-new-folders"  # <== Change this path as needed
# ROOT_FOLDER = r"C:\Users\Administrator\Desktop\IKMC 2025 Amina\KangarooQatar Sheets for results ikmc\Archive"
ROOT_FOLDER = r"C:\Users\Administrator\Desktop\test-out\01"

# Data containers
total_images = 0
success_count = 0
fail_count = 0
results_by_folder = {}

# Record start time
start_time = datetime.now()
print(f"🕒 Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Walk through all subfolders and process images
for root, _, files in os.walk(ROOT_FOLDER):
    jpg_files = [f for f in files if f.lower().endswith(".jpg") and not f.startswith("._")]
    if not jpg_files:
        continue

    folder_name = os.path.relpath(root, ROOT_FOLDER)
    results_by_folder[folder_name] = {"success": [], "fail": []}

    for file in jpg_files:
        total_images += 1
        file_path = os.path.join(root, file)

        try:
            with Image.open(file_path) as img:
                width, height = img.size
                dimension_str = f"{width}x{height}"
        except Exception as e:
            dimension_str = "Unknown"
            print(f"⚠️ Failed to read dimensions for {file}: {e}")

        print(f"📤 Processing: {file_path} [{dimension_str}]")

        try:
            response = requests.post(API_URL, params={"file_path": file_path})
            if response.status_code == 200:
                success_count += 1
                results_by_folder[folder_name]["success"].append(f"{file} [{dimension_str}]")
                print(f"✅ Success: {file}")
            else:
                fail_count += 1
                results_by_folder[folder_name]["fail"].append(f"{file} [{dimension_str}] - {response.status_code} ")
                print(f"❌ Error: {file} - {response.status_code}")
        except Exception as e:
            fail_count += 1
            results_by_folder[folder_name]["fail"].append(f"{file} - Exception: {str(e)}")
            print(f"⚠️ Exception: {file} - {str(e)}")

# Record end time
end_time = datetime.now()
print(f"🕒 End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Save report to file
report_file = "api_results_summary.txt"
with open(report_file, "w", encoding="utf-8") as f:
    f.write(f"📊 API PROCESSING SUMMARY\n")
    f.write(f"=========================\n")
    f.write(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Duration: {str(end_time - start_time)}\n\n")
    f.write(f"Total images processed: {total_images}\n")
    f.write(f"✅ Successes: {success_count}\n")
    f.write(f"❌ Failures: {fail_count}\n\n")

    for folder, data in results_by_folder.items():
        f.write(f"📁 Folder: {folder}\n")
        f.write(f"  ✅ Successful images ({len(data['success'])}):\n")
        for img in data['success']:
            f.write(f"    - {img}\n")

        f.write(f"  ❌ Failed images ({len(data['fail'])}):\n")
        for img in data['fail']:
            f.write(f"    - {img}\n")
        f.write("\n")

print("\n📄 Done! Summary written to:", report_file)
print(f"📸 Total: {total_images} | ✅ {success_count} | ❌ {fail_count}")
print(f"🕒 Duration: {str(end_time - start_time)}")

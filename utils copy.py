import cv2
import numpy as np
import os
from constants import *
import re
import easyocr
from pathlib import Path
from PIL import Image
from rapidfuzz import fuzz

def draw_rois(image_path, rois, output_path):
    """
    Draw rectangles around ROIs on the image and save the result.
    
    Parameters:
        image_path (str): Path to the input image.
        rois (list): List of ROIs, each with x, y, width, height.
        output_path (str): Path to save the output image with drawn ROIs.
    
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        img = cv2.imread(path_image)
         
        # Draw rectangles for each ROI
        for roi in rois:
            x, y, w, h = roi["x"], roi["y"], roi["width"], roi["height"]
            # Draw green rectangle (BGR: 0, 255, 0) with thickness 2
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Save the image
        cv2.imwrite(output_path, img)

        print(f"Saved image with ROIs drawn: {output_path}")
        return True
    except Exception as e:
        print(f"Error drawing ROIs: {str(e)}")
        return False

def get_rois(image_path, image, image_height, image_width, roi_index):
    # Determine the ROI list based on image dimensions
    # DONT REMOVE ( NEW IMAGE dIMENSION PROPOSED)
    if image_height in (4676, 4677) and image_width in (3306, 3307):
        rois = rois_3306_4676
    elif image_height == 4704 and image_width == 3310:
        rois = rois_4704_3310
    elif image_height == 7040 and image_width == 4965:
        rois = rois_7040_4965
    elif image_height == 6624 and image_width == 5100:
        rois = rois_6624_5100
    elif image_height == 2368 and image_width == 1655:
        rois = rois_2368_1655
    elif image_height == 1600 and image_width == 1129:
        rois = roi_1129_1600
    elif image_height == 4680 and image_width == 3307:
        rois = roi_3307_4680
    elif image_height == 4671 and image_width == 3303:
        rois = roi_3303_4671
    elif image_height == 4677 and image_width == 3400:
        rois = roi_3400_4677
    elif image_height == 3488 and image_width == 2268:
        rois = roi_2268_3488
    elif image_height in [1755, 1754] and image_width in [1238, 1239, 1241]:
        rois = roi_1241_1755
    elif image_height == 3520 and image_width == 2268:
        rois = roi_2268_3520
    elif image_height == 3520 and image_width == 2496:
        rois = roi_2496_3520
    elif image_height == 4665 and image_width == 3292:
        rois = roi_3292_4665
    elif image_height == 7014 and image_width == 4960:
        rois = roi_4960_7014
    elif image_height == 1755 and image_width == 1238:
        rois = roi_1238_1755
    elif image_height in [2340, 2339, 2338] and image_width in [1664, 1654, 1653, 1656]:
        rois = roi_1653_2339
    elif image_height == 2560 and image_width == 1806:
        rois = roi_1806_2560
    elif image_height == 4680 and image_width in [3299, 3300, 3302, 3304, 3307]:
        rois = roi_3300_4680
    elif image_height == 2944 and image_width == 2176:
        rois = roi_2176_2944
    elif image_height == 2944 and image_width == 2112:
        rois = roi_2112_2944
    elif image_height == 2704 and image_width in [1904, 1872]:
        rois = roi_1904_2704
    elif image_height in [2960, 2976] and image_width == 2080:
        rois = roi_2080_2960
    elif image_height == 2848 and image_width == 1984:
        rois = roi_1984_2848
    elif image_height == 3280 and image_width == 2288:
        rois = roi_2288_3280
    elif image_height == 3056 and image_width == 2016:
        rois = roi_2016_3056
    elif image_height == 3200 and image_width == 2224:
        rois = roi_2224_3200
    elif image_height == 3072 and image_width == 2208:
        rois = roi_2208_3072
    elif image_height == 2896 and image_width == 2128:
        rois = roi_2128_2896
    elif image_height == 3452 and image_width == 2374:
        rois = roi_2374_3452
    elif image_height == 3376 and image_width == 2276:
        rois = roi_2276_3376
    elif image_height == 3428 and image_width == 2396:
        rois = roi_2396_3428
    elif image_height == 3480 and image_width == 2250:
        rois = roi_2250_3480
    elif image_height == 3488 and image_width == 2268:
        rois = roi_2268_3488
    elif image_height == 3024 and image_width == 2064:
        rois = roi_2064_3024
    # new
    elif image_height == 1277 and image_width in [906, 942]:
        rois = roi_942_1277
    elif image_height == 4672 and image_width == 3248:
        rois = roi_3248_4672
    elif image_height == 4672 and image_width == 3328:
        rois = roi_3328_4672
    elif image_height in [1313, 1275] and image_width == 950:
        rois = roi_950_1313
    elif image_height == 1477 and image_width == 1050:
        rois = roi_1050_1477
    elif image_height == 1290 and image_width == 939:
        rois = roi_939_1290
    elif image_height == 1494 and image_width == 1072:
        rois = roi_1072_1494
    elif image_height == 1408 and image_width == 1010:
        rois = roi_1010_1408
    elif image_height == 1364 and image_width == 1013:
        rois = roi_1013_1364
    elif image_height == 1281 and image_width == 920:
        rois = roi_920_1281
    elif image_height == 1376 and image_width == 998:
        rois = roi_998_1376
    elif image_height == 1262 and image_width == 929:
        rois = roi_929_1262
    elif image_height == 1289 and image_width == 947:
        rois = roi_947_1289
    elif image_height == 1325 and image_width == 935:
        rois = roi_935_1325
    elif image_height == 1245 and image_width == 917:
        rois = roi_917_1245
    elif image_height == 1335 and image_width == 999:
        rois = roi_999_1335
    elif image_height == 1251 and image_width == 926:
        rois = roi_926_1251
    elif image_height == 1317 and image_width == 958:
        rois = roi_958_1317
    elif image_height == 1304 and image_width == 975:
        rois = roi_975_1304
    elif image_height == 4678 and image_width == 3308:
        rois = roi_3308_4678
    else:
        raise ValueError("Image dimensions do not match any predefined ROI lists.")

    # Check if roi_index is valid
    if roi_index >= len(rois) or roi_index < 0:
        return []  # Invalid index, return empty list
    
    # Open a file in append mode ('a'), so it adds to the file instead of overwriting it
    with open('log.txt', 'a') as f:
        f.write(f"Using ROI list {roi_index} for {image_height}x{image_width} image {image_path}.\n")
    # Get selected ROIs
    selected_rois = rois[roi_index]
    if not selected_rois:
        return []  # Selected roi_index points to an empty roi

    # if roi_index == 1: 
    #     import pdb; pdb.set_trace()
    
    # Extract and return the regions of interest
    extracted_rois = []

    # for roi in rois:
    for roi in selected_rois :
        x, y, w, h = roi["x"], roi["y"], roi["width"], roi["height"]
        extracted_rois.append(image[y:y+h, x:x+w])
        if not extracted_rois:
            raise ValueError("No valid ROIs extracted from the image.")
    return extracted_rois

def preprocess_image(image, width, height):
    """
    Resize and preprocess the image.

    Parameters:
        image (numpy.ndarray): The input image.
        width (int): Desired width for resizing.
        height (int): Desired height for resizing.

    Returns:
        tuple: Preprocessed grayscale, blurred, and edge-detected images.
    """
    t_lower = 10 # Lower Threshold 
    t_upper = 70 # Upper threshold 
    # aperture_size = 1 # Aperture size 
    L2Gradient = True # Boolean 
    resized_image = cv2.resize(image, (width, height))
    gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 1)
    canny_image = cv2.Canny(blurred_image, 10, 70)
        # Applying the Canny Edge filter  
    # with Aperture Size and L2Gradient 
    canny_image = cv2.Canny(blurred_image,
     t_lower,
     t_upper, 
    # apertureSize = aperture_size,  
    L2gradient = L2Gradient )
    return resized_image, gray_image, canny_image

def find_circles(contours):
    """
    Find circle-like contours based on area and circularity.

    Parameters:
        contours (list): List of contours.

    Returns:
        list: List of circle contours.
    """
    circle_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 4000 < area < 5500:  # Adjusted area threshold
            perimeter = cv2.arcLength(cnt, True)
            circularity = 4 * np.pi * area / (perimeter * perimeter + 1e-5)
            if 0.65 <= circularity <= 0.82:
                circle_contours.append(cnt)
    return circle_contours

def group_circles_by_row(circle_centers):
    """
    Group circles into rows based on y-coordinate proximity.

    Parameters:
        circle_centers (list): List of circle centers (x, y, radius).

    Returns:
        list: List of grouped circles.
    """
    circle_centers.sort(key=lambda c: c[1])  # Sort by y-coordinate
    grouped_circles = []
    current_group = [circle_centers[0]]

    for i in range(1, len(circle_centers)):
        if abs(circle_centers[i][1] - current_group[-1][1]) <= 4:
            current_group.append(circle_centers[i])
        else:
            grouped_circles.append(current_group)
            current_group = [circle_centers[i]]

    if current_group:
        grouped_circles.append(current_group)
    return grouped_circles

def fill_missing_coordinates(groups, complete_group):
    # Identify groups that need filling
    completed_groups = []

    for group in groups:
        # Check if the group has less than 5 tuples
        if len(group) < 5:
            missing_indices = []
            filled_group = list(group)  # Make a copy of the group

            # Identify missing indices by comparing x values
            for i in range(len(complete_group)):
                if i >= len(group) or abs(group[i][0] - complete_group[i][0]) > 10:
                    missing_indices.append(i)

            # Fill missing tuples
            for missing_idx in missing_indices:
                x = complete_group[missing_idx][0]  # Use x from the complete group
                if missing_idx > 0:
                    y = filled_group[missing_idx - 1][1]  # Use y from the previous tuple
                else:
                    y = filled_group[missing_idx + 1][1]  # Use y from the next tuple
                r = complete_group[missing_idx][2]  # Use r from the complete group
                filled_group.insert(missing_idx, (x, y, r))

            completed_groups.append(filled_group[:5])  # Slice to keep only the first 5 tuples
        else:
            completed_groups.append(group[:5])  # Slice to keep only the first 5 tuples

    return completed_groups

def analyze_groups(grouped_circles, gray_image, question_number):
    """
    Analyze each group of circles to determine the filled circle(s).
    Detects multiple filled bubbles and returns comma-separated answers when applicable.

    Parameters:
        grouped_circles (list): List of grouped circles.
        gray_image (numpy.ndarray): The grayscale image.
        question_number (int): Starting question number.

    Returns:
        dict: Results mapping question numbers to answers.
    """
    results = {}
    position_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
    
    print(f"Initial grouped_circles count: {len(grouped_circles)}")
    validGroups = [group for group in grouped_circles if len(group) == 5]
    print(f"Valid groups with exactly 5 circles: {len(validGroups)}")

    # Early exit if no valid groups
    if not validGroups:
        print("No valid groups found. Returning empty results.")
        return {}, grouped_circles

    for group in grouped_circles:
        group.sort(key=lambda c: c[0])  # Sort by x-coordinate
    print("Sorted all groups by x-coordinate.")

    for i, group in enumerate(grouped_circles):
        if len(group) == 1:
            lone_tuple = group[0]
            print(f"Found lone tuple at group index {i}: {lone_tuple}")

            y_diff_prev = abs(lone_tuple[1] - grouped_circles[i - 1][0][1]) if i > 0 else float('inf')
            y_diff_next = abs(lone_tuple[1] - grouped_circles[i + 1][0][1]) if i < len(grouped_circles) - 1 else float('inf')
            print(f"y_diff_prev: {y_diff_prev}, y_diff_next: {y_diff_next}")

            # Determine whether to append to the previous or next group
            if y_diff_prev <= y_diff_next and i > 0:
                grouped_circles[i - 1].append(lone_tuple)
                grouped_circles[i - 1].sort(key=lambda c: c[0])  # Sort by x-coordinate
                print(f"Appended lone tuple to previous group {i - 1}")
            elif y_diff_next < y_diff_prev and i < len(grouped_circles) - 1:
                grouped_circles[i + 1].append(lone_tuple)
                grouped_circles[i + 1].sort(key=lambda c: c[0])  # Sort by x-coordinate
                print(f"Appended lone tuple to next group {i + 1}")

    # Remove groups that contained only one tuple, as they are now merged
    grouped_circles = [group for group in grouped_circles if len(group) > 1]
    print(f"Grouped circles after merging lone tuples: {len(grouped_circles)} groups")

    grouped_circles = fill_missing_coordinates(grouped_circles, validGroups[0])
    print("Filled missing coordinates.")

    for group_index, group in enumerate(grouped_circles):
        circle_intensities = []
        print(f"Analyzing group {group_index} with {len(group)} circles")

        for (x, y, radius) in group:
            mask = np.zeros(gray_image.shape, dtype=np.uint8)
            cv2.circle(mask, (x, y), int(radius * 0.8), 255, -1)
            mean_val = cv2.mean(gray_image, mask=mask)[0]
            circle_intensities.append(mean_val)
            print(f"Circle at ({x}, {y}) with radius {radius}: mean intensity = {mean_val}")

        # Find the average intensity of all circles to use as a reference
        avg_intensity = sum(circle_intensities) / len(circle_intensities)
        
        # Find the max intensity which likely represents unfilled bubbles
        max_intensity = max(circle_intensities)
        
        # Calculate threshold to determine filled vs unfilled
        THRESHOLD = 20  # Adjustable (recommended range: 15–30)
        print(f"Using threshold: {THRESHOLD}, Average intensity: {avg_intensity}")

        # Find all filled circles (significantly lower intensity than max)
        filled_positions = []
        for idx, intensity in enumerate(circle_intensities):
            intensity_diff = max_intensity - intensity
            if intensity_diff > THRESHOLD:
                filled_positions.append(idx + 1)
                print(f"Circle {idx+1} is filled (intensity: {intensity}, diff: {intensity_diff})")
        
        # Convert positions to letters
        if not filled_positions:
            print(f"Group {group_index}: No circle is meaningfully filled.")
            answer = 'Blank'
        else:
            answers = [position_to_letter[pos] for pos in filled_positions]
            answer = ','.join(answers) if len(answers) > 1 else answers[0]
            print(f"Group {group_index}: Filled circle(s): {filled_positions}, answer: {answer}")

        results[f"Q{question_number}"] = answer
        question_number += 1

    print(f"Final results: {results}")
    return results, grouped_circles
# 
reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU for simplicity

def extract_roll_number(image_path):
    
    # Read the image in grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Reduce the image quality by resizing to 60% of the original resolution
    height, width = image.shape
    resized_image = cv2.resize(image, (int(width * 0.25), int(height * 0.25)), interpolation=cv2.INTER_AREA)
    
    # Crop the top 20% of the resized image
    cropped_image = resized_image[:int(0.2 * resized_image.shape[0]), :]
    
    # Resize the cropped image for better OCR and apply thresholding
    cropped_image = cv2.resize(cropped_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(cropped_image, 128, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Step 2: Use EasyOCR to extract text
    results = reader.readtext(thresh,detail=0, batch_size=32)

    # Step 3: Look for "ROLL NO" and extract the next text
    for i, text in enumerate(results):
        if "ROLL NO" in text.upper():  # Case-insensitive search
            if i + 1 < len(results):  # Ensure there's a next item
                return results[i + 1]  # Return the text after "ROLL NO"
    
    return "No roll number found."


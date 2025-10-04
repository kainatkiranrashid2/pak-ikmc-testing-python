import threading
import math
import cv2
import numpy as np
from utils import *
from pathlib import Path
from PIL import Image

class TimeoutException(Exception):
    pass

def process_image_wt(path_image, timeout=15):
    result = {"status": "success", "data": None}

    def target():
        try:
            result["data"] = process_image(path_image)
        except Exception as e:
            result["status"] = "error"
            result["data"] = str(e)

    thread = threading.Thread(target=target)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise TimeoutException(f"Manual check required: {path_image}")
    
    if result["status"] == "error":
        raise Exception(result["data"])
    
    return result["data"]

def process_image(path_image):
    height_img, width_img = 850, 700
    current_question_number = 1
    final_results = {}
    valid_results_lengths = {24, 30}

    # Load image with OpenCV or fallback to PIL
    img = cv2.imread(path_image)
    if img is None:
        print(f"OpenCV failed to load image at {path_image}. Attempting to load with PIL...")
        try:
            pil_image = Image.open(path_image).convert('RGB')
            img = np.array(pil_image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            print(f"Successfully loaded image with PIL at {path_image}")
        except Exception as e:
            raise ValueError(f"Failed to load image with both OpenCV and PIL at {path_image}. Error: {str(e)}")

    if img is None:
        raise ValueError(f"Image at {path_image} is corrupt or unreadable. Please verify the file.")

    print(f"Image Height: {img.shape[0]}, Width: {img.shape[1]}")
    imgHeight, imgWidth = img.shape[0], img.shape[1]

    roi_list = get_roi_list(imgHeight, imgWidth)
    print(f"roi_list: {roi_list}")  # DEBUG
    max_roi_attempts = len(roi_list)
    
    roi_index = 0
    while roi_index < max_roi_attempts:
        # Get ROIs with the current roi_index
        try:
            print(f"Getting ROIs for roi_index {roi_index}.")
            rois = get_rois(path_image, img, imgHeight, imgWidth, roi_index)
            if not rois:
                print(f"No ROIs found for roi_index {roi_index}. Incrementing roi_index.")
                roi_index += 1
                current_question_number = 1
                continue
        except IndexError as e:
            print(f"IndexError in get_rois for roi_index {roi_index}: {e}. Incrementing roi_index.")
            roi_index += 1
            current_question_number = 1
            continue
        except Exception as e:
            raise ValueError(f"Error in get_rois for {path_image}: {str(e)}")

        final_results = {}  # Reset results for each iteration
        print(f"Processing {len(rois)} ROIs for roi_index {roi_index}")

        for i, roi in enumerate(rois, 1):
            try:
                # Preprocess the ROI
                resized_image, gray_image, canny_image = preprocess_image(roi, width_img, height_img)
                cv2.imwrite(f"resized_image_{i}.jpg", resized_image)
                cv2.imwrite(f"gray_image_{i}.jpg", gray_image)
                cv2.imwrite(f"canny_image_{i}.jpg", canny_image)
                
                # Find contours
                contours, _ = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                print(f"Number of contours in ROI {i}: {len(contours)}")
                
                # Find circles
                circle_contours = find_circles(contours)
                if not circle_contours:
                    print(f"No circle contours found in ROI {i}. Skipping.")
                    continue
                
                circle_centers = [(int(x), int(y), int(radius)) for cnt in circle_contours for (x, y), radius in [cv2.minEnclosingCircle(cnt)]]
                print(f"Number of circle centers in ROI {i}: {len(circle_centers)}")
                
                # Group circles by row
                grouped_circles = group_circles_by_row(circle_centers)
                print(f"Number of grouped circles in ROI {i}: {len(grouped_circles)}")
                
                # Analyze groups
                analysis_results, grouped_circles = analyze_groups(grouped_circles, gray_image, current_question_number)
                print(f"Analysis results for ROI {i}: {analysis_results}")
                
                if not analysis_results:
                    print(f"No valid groups found in ROI {i}. Incrementing roi_index.")
                    current_question_number = 1
                    break
                
                final_results.update(analysis_results)
                current_question_number += len(grouped_circles)
            
            except IndexError as e:
                print(f"IndexError in ROI {i} processing: {e}. Skipping ROI.")
                continue
            except Exception as e:
                print(f"Error processing ROI {i}: {str(e)}. Skipping ROI.")
                continue

        # Check if the results are valid
        if len(final_results) in valid_results_lengths:
            break
        else:
            print(f"Invalid result length {len(final_results)}. Incrementing roi_index.")
            roi_index += 1
            current_question_number = 1

    # Check if we exhausted ROI attempts
    if roi_index >= max_roi_attempts:
        raise ValueError(f"Manual check required for {path_image}: No valid results after {max_roi_attempts} ROI attempts")

    # Count NaN values in final_results
    nan_count = sum(1 for value in final_results.values() if value is None or (isinstance(value, float) and math.isnan(value)))
    print(f"Final results: {final_results}")
    print(f"Number of NaN values: {nan_count}")

    if nan_count > 7:
        raise ValueError(f"Manual check required for {path_image}: Too many NaN values ({nan_count})")

    if not final_results or len(final_results) not in valid_results_lengths:
        raise ValueError(f"Manual check required for {path_image}: Invalid final results")

    formatted_results = ", ".join([f"({key}:{value})" for key, value in final_results.items()])
    return f"{{{formatted_results}}}"
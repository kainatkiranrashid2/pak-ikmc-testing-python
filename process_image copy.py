
import threading
import math
import cv2
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
    import time  # For simulating delays in testing

    height_img, width_img = 850, 700
    current_question_number = 1
    final_results = {}
    roi_index = 0
    valid_results_lengths = {24, 30}  # Define valid lengths for final_results

    # img = cv2.imread(path_image)
    # if img is None:
    #     raise FileNotFoundError(f"Image not found at {path_image}")

    # new code 
    # Try loading image with OpenCV
    img = cv2.imread(path_image)

    if img is None:
        print(f"OpenCV failed to load image at {path_image}. Attempting to load with PIL...")
        try:
            # Fallback to PIL
            pil_image = Image.open(path_image).convert('RGB')
            # Convert PIL image to OpenCV format (BGR)
            img = np.array(pil_image)
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            print(f"Successfully loaded image with PIL at {path_image}")
        except Exception as e:
            raise ValueError(f"Failed to load image with both OpenCV and PIL at {path_image}. Error: {str(e)}")

    if img is None:
        raise ValueError(f"Image at {path_image} is corrupt or unreadable. Please verify the file.")

    print("Image Height: ", img.shape[0], "Width: ", img.shape[1])
    imgHeight = img.shape[0]
    imgWidth = img.shape[1]

    while True:

        # Get ROIs with the current roi_index
        rois = get_rois(path_image, img, imgHeight, imgWidth, roi_index)
        print(roi_index, "rois in process image")
        final_results = {}  # Reset results for each iteration

        # # DONT REMOVE ( NEW CODE GRAPHICAL)
        # path = Path(path_image)
        # print("Processing file: ", path)
        # if not path.exists():
        #     raise HTTPException(status_code=404, detail="File does not exist")
        # elif not path.is_file():
        #     raise HTTPException(status_code=400, detail="The path is not a file")

        # # DONT REMOVE ( NEW CODE GRAPHICAL)
        # # Define output path for visualized image
        # output_dir = path.parent
        # output_filename = f"{path.stem}_roi_visualized{path.suffix}"
        # output_path = str(output_dir / output_filename)
        # rois_for_visualization = roi_2112_2944[0]

        # # Draw and save image with ROIs
        # if not draw_rois(path_image, rois_for_visualization, output_path):
        #     print("Warning: Failed to save visualized image, proceeding with processing")

        # print(rois, "rois in process image")
        for i, roi in enumerate(rois, 1):
            resized_image, gray_image, canny_image = preprocess_image(roi, width_img, height_img)
            cv2.imwrite(f"resized_image_{i}.jpg", resized_image)
            cv2.imwrite(f"gray_image_{i}.jpg", gray_image)
            cv2.imwrite(f"canny_image_{i}.jpg", canny_image)
            
            contours, _ = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            print("Number of contours: ", len(contours))
            circle_contours = find_circles(contours)
            print("Number of circle contours: ", circle_contours)
            circle_centers = [(int(x), int(y), int(radius)) for cnt in circle_contours for (x, y), radius in [cv2.minEnclosingCircle(cnt)]]
            print("Number of grouped circles: ", len(circle_centers))
            grouped_circles = group_circles_by_row(circle_centers)
            print("Number of grouped circles: ", len(grouped_circles))
            analysis_results, grouped_circles = analyze_groups(grouped_circles, gray_image, current_question_number)
            print("Analysis results: ", analysis_results)

            if not analysis_results:  # If empty results are returned
                roi_index += 1  # Increment roi_index
                current_question_number = 1  # Reset question number
                break  # Exit the inner loop and restart with updated ROI            
                       
            final_results.update(analysis_results)
            current_question_number += len(grouped_circles)

        # Check if the results are valid
        if len(final_results) in valid_results_lengths:
            break  # Exit the loop if valid results are obtained
        else:
            roi_index += 1  # Increment roi_index and retry
            current_question_number = 1

    # Count NaN values in final_results 
    nan_count = sum(1 for value in final_results.values() if value is None or (isinstance(value, float) and math.isnan(value)))

    print("Final results: ", final_results)
    print("Number of NaN values: ", nan_count)

    if nan_count > 7:
        raise Exception(f"Manual check required for {path_image}")
    
    # Final exception check before returning
    if not final_results or len(final_results) not in valid_results_lengths:
        raise ValueError(f"Manual check required for {path_image}")
    

    formatted_results = ", ".join([f"({key}:{value})" for key, value in final_results.items()])

    return f"{{{formatted_results}}}"



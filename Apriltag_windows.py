import cv2
import numpy as np
import pupil_apriltags as pl
import os
import csv
from datetime import datetime

# Create a folder to save images
images_folder = "detected_tags_images"
if not os.path.exists(images_folder):
    os.makedirs(images_folder)

# Initialize CSV file and write the header row
csv_filename = "detection_results.csv"
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Tag ID", "Tag Position"])

# Camera intrinsic parameters (these values should be obtained by calibrating your camera)
camera_matrix = np.array([[930.79652155, 0, 661.20967027],
                          [0, 932.27891919, 408.65175784],
                          [0, 0, 1]], dtype=np.float64)
dist_coeffs = np.array([[0.0481284473, -0.0886667343, 0.000604081268, -0.0000677186841, 0.0281485370]])

# The actual size of the AprilTag (in meters)
tag_size = 0.16  # Modify this to the actual size of your tag

cap = cv2.VideoCapture(0)  # Capture from camera
options = pl.Detector(families='tag36h11')

while True:
    ret, image1 = cap.read()
    if not ret:
        break  # Exit loop if unable to get an image

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time

    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    results = options.detect(gray)
    for r in results:
        # Get the ID
        id = r.tag_id
        print(f"Detected AprilTag ID: {id}, Time: {current_time}")

        # Get the coordinates of the four corners
        corners = r.corners.astype(int)
        # Draw lines between each corner point
        for i in range(4):
            cv2.line(image1, tuple(corners[i - 1]), tuple(corners[i]), (255, 0, 255), 2, cv2.LINE_AA)

        # Calculate 3D coordinates
        object_points = np.array([[-tag_size / 2, -tag_size / 2, 0],
                                  [tag_size / 2, -tag_size / 2, 0],
                                  [tag_size / 2, tag_size / 2, 0],
                                  [-tag_size / 2, tag_size / 2, 0]])
        retval, rvec, tvec = cv2.solvePnP(object_points, corners.astype(np.float64), camera_matrix, dist_coeffs)

        tag_position = tvec.flatten()
        print("Tag position: ", tag_position)
        # Uncomment to print the distance: print('distance:', tag_position[2])

        # Draw the center coordinate of the AprilTag
        center = np.mean(corners, axis=0).astype(int)
        cv2.circle(image1, tuple(center), 5, (0, 0, 255), -1)

        # Overlay text information on the image
        cv2.putText(image1, f"ID: {id}", (center[0], center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the current detection information to the CSV file
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, id, tag_position])

        # Save the image with the detected tag
        image_filename = os.path.join(images_folder, f"tag_{id}_{current_time.replace(':', '-')}.jpg")
        cv2.imwrite(image_filename, image1)

    # Display the processed image
    cv2.imshow("Apriltags", image1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close any open windows
cap.release()
cv2.destroyAllWindows()




import cv2
import numpy as np
import apriltag
import os
import csv
import time
import glob

# Existing setup code...

# Initialize an empty list to store all the center points
all_centers = []

# New directory for processed images
processed_image_folder_path = '/media/zinc/F86FD79DA96C4494/mmtag_record_data/mmwave_tag_data/20240216_154233/processed_video/'
os.makedirs(processed_image_folder_path, exist_ok=True)

# Existing image processing loop...
for image_filename in sorted_filenames:
    # Existing code to process each image...
    
    # Initialize an empty image1 for drawing. You need to clone the original image to avoid altering it.
    image1 = image.copy()
    
    if results:
        for r in results:
            # Existing code to process each detected tag...
            
            # Draw the center coordinate of the AprilTag
            center = np.mean(r.corners, axis=0).astype(int)
            cv2.circle(image1, tuple(center), 5, (0, 0, 255), -1)
            
            # Overlay text information on the image
            cv2.putText(image1, f"ID: {r.tag_id}", (center[0], center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            
            # Append the center point to all_centers
            all_centers.append(center)
            
    # Draw the trajectory
    for i in range(1, len(all_centers)):
        cv2.line(image1, tuple(all_centers[i-1]), tuple(all_centers[i]), (255, 0, 0), 2)
    
    # Save the processed image to the new directory
    processed_image_filename = os.path.join(processed_image_folder_path, os.path.basename(image_filename))
    cv2.imwrite(processed_image_filename, image1)

print("Processing and drawing completed.")



import cv2
import numpy as np
import apriltag
import os
import csv
import glob

# 初始化用于追踪每个ID中心点的字典
all_centers = {}

# 新目录用于存储处理后的图片
processed_image_folder_path = '/path/to/processed_images/'
os.makedirs(processed_image_folder_path, exist_ok=True)

# 遍历每张图片的代码...
for image_filename in sorted_filenames:
    image = cv2.imread(image_filename)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    results = options.detect(gray)
    
    image1 = image.copy()

    if results:
        for r in results:
            id = r.tag_id
            corners = r.corners
            center = np.mean(corners, axis=0).astype(int)

            # 如果ID不在字典中，则添加一个新的空列表
            if id not in all_centers:
                all_centers[id] = []
            all_centers[id].append(center)

            # 为当前标签绘制中心点
            cv2.circle(image1, tuple(center), 5, (0, 0, 255), -1)
            cv2.putText(image1, f"ID: {id}", (center[0], center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 为每个ID绘制轨迹
    for id, centers in all_centers.items():
        for i in range(1, len(centers)):
            cv2.line(image1, tuple(centers[i-1]), tuple(centers[i]), (255, 0, 0), 2)

    # 保存处理后的图片
    processed_image_filename = os.path.join(processed_image_folder_path, os.path.basename(image_filename))
    cv2.imwrite(processed_image_filename, image1)

print("Processing and drawing for all IDs completed.")

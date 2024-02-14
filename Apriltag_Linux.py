import cv2
import numpy as np
import apriltag
import os
import csv
import time

# # 创建用于保存图像的文件夹
# images_folder = "detected_tags_images"
# if not os.path.exists(images_folder):
#     os.makedirs(images_folder)
#
# # 初始化CSV文件并写入标题行
# csv_filename = "detection_results.csv"
# with open(csv_filename, 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Time", "Tag ID", "Tag Position"])
def create_folder_for_test():
    """创建新文件夹以保存当前测试的图片和CSV文件，文件夹名基于当前时间戳。"""
    folder_name = time.strftime("test_%Y%m%d_%H%M%S")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    return folder_name


# 每次测试时创建新的文件夹
test_folder = create_folder_for_test()

# 初始化CSV文件并写入标题行
csv_filename = os.path.join(test_folder, "detection_results.csv")
with open(csv_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Time", "Tag ID", "Tag Position"])

# 相机内参（这些值应该通过标定你的相机获得）
camera_matrix = np.array([[930.79652155, 0, 661.20967027],
                          [0, 932.27891919, 408.65175784],
                          [0, 0, 1]], dtype=np.float64)
dist_coeffs = np.array([[4.81284473e-02, -8.86667343e-02, 6.04081268e-04, -6.77186841e-05, 2.81485370e-02]])

# AprilTag的实际尺寸（米）
tag_size = 0.16  # 修改为您的标签实际大小

cap = cv2.VideoCapture(0)  # 获取摄像头
options = apriltag.Detector(apriltag.DetectorOptions(families='tag36h11'))

while True:
    ret, image1 = cap.read()
    if not ret:
        break  # 如果无法获取图像，退出循环

    current_time = time.time()  # 获取当前时间

    gray = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    results = options.detect(gray)
    for r in results:
        # 获取id
        id = r.tag_id
        print(f"Detected AprilTag ID: {id}, Time: {current_time}")

        # 获取四个角点的坐标
        corners = r.corners.astype(int)
        # 对于每个角点绘制线
        for i in range(4):
            cv2.line(image1, tuple(corners[i - 1]), tuple(corners[i]), (255, 0, 255), 2, cv2.LINE_AA)

        # 计算3D坐标
        object_points = np.array([[-tag_size / 2, -tag_size / 2, 0],
                                  [tag_size / 2, -tag_size / 2, 0],
                                  [tag_size / 2, tag_size / 2, 0],
                                  [-tag_size / 2, tag_size / 2, 0]])
        retval, rvec, tvec = cv2.solvePnP(object_points, corners.astype(np.float64), camera_matrix, dist_coeffs)

        tag_position = tvec.flatten()
        print("Tag position: ", tag_position)
        # print('distance:', tag_position[2])

        # 绘制AprilTag的中心坐标
        center = np.mean(corners, axis=0).astype(int)
        cv2.circle(image1, tuple(center), 5, (0, 0, 255), -1)

        # 在图像上绘制文本信息
        cv2.putText(image1, f"ID: {id}", (center[0], center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # # 保存当前检测到的信息到CSV文件
        # with open(csv_filename, 'a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([current_time, id, tag_position])
        # 保存检测到的信息到CSV文件
        with open(csv_filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, id, tag_position])

        # 保存检测到标签的图像
        image_filename = os.path.join(test_folder, f"tag_{id}_str{current_time}.jpg")
        cv2.imwrite(image_filename, image1)

    # 显示处理后的图像
    cv2.imshow("Apriltags", image1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

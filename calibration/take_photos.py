import cv2
import os
import time

def capture_images(folder_path, interval=1, duration=40):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Create a video capture object
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open the camera")
        return

    print("Press the space bar to start capturing...")

    # Display the camera image in real-time until the space bar is pressed
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot read the camera image")
            break
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord(' '):  # ASCII code for the space bar
            break

    start_time = time.time()
    count = 0

    # Capture images at the specified interval and duration
    while True:
        ret, frame = cap.read()

        if not ret:
            print("Cannot read the camera image")
            break

        # Get the current time
        current_time = time.time()

        # Save images at the given interval
        if current_time - start_time >= interval * count:
            # Save the image
            img_name = f"{folder_path}/img_{count:03d}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"Captured {img_name}")
            count += 1

        # Stop capturing after the specified duration
        if current_time - start_time > duration:
            break

        # Continue displaying the image in real-time
        cv2.imshow("Frame", frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources and close the window
    cap.release()
    cv2.destroyAllWindows()

# Example usage, make sure to update it to your actual path
capture_images("/home/yao/Documents/mmwave/pic")

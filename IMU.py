import pyrealsense2 as rs
import cv2
import numpy as np
from ultralytics import YOLO
import math
import time



# Initialize YOLOv8 model
model = YOLO("best.pt")  # Replace with your YOLOv8 weights

# Configure RealSense camera
pipeline = rs.pipeline()
config = rs.config()

# Enable the color and depth streams
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 60)
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

# Start the camera pipeline
pipeline.start(config)

# Get depth scale to convert depth units to meters
profile = pipeline.get_active_profile()
color_stream = profile.get_stream(rs.stream.color).as_video_stream_profile()
intrinsics = color_stream.get_intrinsics()  # Camera intrinsics

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

# Align depth to the color stream
align = rs.align(rs.stream.color)




#time
last_time = time.time()


# Display the image
times = []
circle_pos = []
try:
    while True:
        # Wait for frames and align them
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        # Get color and depth frames
        color_frame = aligned_frames.get_color_frame()
        depth_frame = aligned_frames.get_depth_frame()

        current_time = time.time()



        if not color_frame or not depth_frame:
            continue

        # Convert frames to NumPy arrays
        color_image = np.asanyarray(color_frame.get_data())
        depth_image = np.asanyarray(depth_frame.get_data())


        color_image = cv2.flip(color_image, -1)
        depth_image = cv2.flip(depth_image, -1)
        # Run YOLOv8 inference on the color image
        results = model(color_image)

        # Annotate the color image with YOLO results

        # Process YOLO results and calculate depth

        average_x = 0
        average_y = 0
        average_z = 0
        x = 0
        for detection in results[0].boxes:

            x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Bounding box coordinates
            conf = detection.conf[0]  # Confidence score
            label = detection.cls[0]  # Class label

            # Get the depth at the center of the bounding box
            center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
            depth_value = depth_image[center_y, center_x] * depth_scale  # Convert to meters
            average_x += center_x
            average_y += center_y
            average_z += depth_value
            x += 1

            dx = (center_x - intrinsics.ppx) / intrinsics.fx  # Horizontal offset in normalized coordinates
            dy = (center_y - intrinsics.ppy) / intrinsics.fy  # Vertical offset in normalized coordinates

            angle_x = math.degrees(math.atan(dx))  # Angle in degrees along the X-axis
            angle_y = math.degrees(math.atan(dy))  # Angle in degrees along the Y-axis

            relative_x = depth_value * math.sin(math.radians(angle_x))
            relative_y = depth_value * math.cos(math.radians(angle_x))

        if x > 0:
            average_x /= x
            average_y /= x
            average_z /= x
        else:
            average_x = 0
            average_y = 0
            average_z = 0

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Stop the pipeline and release resources
    pipeline.stop()
    cv2.destroyAllWindows()

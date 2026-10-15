import cv2
import numpy as np

# Input and output paths
input_video = "C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\demo_raw.mp4"
output_video = "C:\\Users\\lsz\\Desktop\\KeyShield\\Video_Assets\\demo_cleaned.mp4"

# Crop region (x, y, width, height)
crop_x, crop_y, crop_w, crop_h = 50, 30, 1820, 1020

# Blur regions (relative to the ORIGINAL frame)
# After cropping, adjust coordinates:
# New x = original_x - crop_x
# New y = original_y - crop_y
blur_regions_original = [
    {"x": 120, "y": 60, "w": 320, "h": 32},  # Username in PowerShell path
]

# Calculate blur regions relative to the CROPPED frame
blur_regions = []
for region in blur_regions_original:
    new_x = region["x"] - crop_x
    new_y = region["y"] - crop_y
    if new_x + region["w"] <= crop_w and new_y + region["h"] <= crop_h:
        blur_regions.append({"x": new_x, "y": new_y, "w": region["w"], "h": region["h"]})

# Open the video
cap = cv2.VideoCapture(input_video)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Get video properties
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video, fourcc, fps, (crop_w, crop_h))

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Crop the frame
    frame = frame[crop_y:crop_y + crop_h, crop_x:crop_x + crop_w]

    # Blur sensitive regions
    for region in blur_regions:
        x, y, w, h = region["x"], region["y"], region["w"], region["h"]
        if x + w <= frame.shape[1] and y + h <= frame.shape[0]:
            frame[y:y + h, x:x + w] = cv2.GaussianBlur(frame[y:y + h, x:x + w], (25, 25), 0)

    # Write the frame
    out.write(frame)
    frame_count += 1
    if frame_count % 100 == 0:
        print(f"Processed {frame_count} frames...")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()

print(f"Video processed and saved to {output_video}")
print(f"Total frames processed: {frame_count}")
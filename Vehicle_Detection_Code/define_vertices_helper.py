"""
Helper script to interactively define quadrilateral vertices for lane detection.
This script allows you to click on points in a video frame to get their coordinates.
"""

import cv2
import numpy as np

# List to store clicked points
clicked_points = []

def mouse_callback(event, x, y, flags, param):
    """
    Mouse callback function that captures click coordinates.
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y))
        print(f"Point {len(clicked_points)}: ({x}, {y})")
        # Draw a circle at the clicked point
        cv2.circle(frame_copy, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Click to define vertices (Press ESC when done)', frame_copy)

# Path to your video file
video_path = r'C:\Object_Detection_Projects\vehicle_detection\Dataset\Vehicle_Detection_Image_Dataset\sample_video.mp4'

# Open the video
cap = cv2.VideoCapture(video_path)

# Read the first frame (or any frame you want to use as reference)
ret, frame = cap.read()

if not ret:
    print("Error: Could not read video frame")
    cap.release()
    exit()

# Create a copy for drawing
frame_copy = frame.copy()

# Display instructions
print("=" * 60)
print("VERTEX DEFINITION HELPER")
print("=" * 60)
print("\nInstructions:")
print("1. Click on the 4 corners of your LEFT lane quadrilateral")
print("2. Click in order: top-left, top-right, bottom-right, bottom-left")
print("3. Press ESC when done with left lane")
print("4. Repeat for right lane")
print("\nClick on the frame to define vertices...")
print("=" * 60)

# Set up mouse callback
cv2.namedWindow('Click to define vertices (Press ESC when done)')
cv2.setMouseCallback('Click to define vertices (Press ESC when done)', mouse_callback)

# Display the frame
cv2.imshow('Click to define vertices (Press ESC when done)', frame_copy)

# Wait for ESC key (27) to be pressed
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        break

cv2.destroyAllWindows()
cap.release()

# Process the clicked points
if len(clicked_points) >= 4:
    # First 4 points are for left lane
    left_lane_vertices = clicked_points[:4]
    
    # If more than 4 points, use next 4 for right lane
    if len(clicked_points) >= 8:
        right_lane_vertices = clicked_points[4:8]
    else:
        right_lane_vertices = None
    
    # Print the vertices in the format needed for your code
    print("\n" + "=" * 60)
    print("GENERATED VERTEX CODE:")
    print("=" * 60)
    print("\n# Left lane vertices:")
    print(f"vertices1 = np.array([{left_lane_vertices[0]}, {left_lane_vertices[1]}, "
          f"{left_lane_vertices[2]}, {left_lane_vertices[3]}], dtype=np.int32)")
    
    if right_lane_vertices:
        print("\n# Right lane vertices:")
        print(f"vertices2 = np.array([{right_lane_vertices[0]}, {right_lane_vertices[1]}, "
              f"{right_lane_vertices[2]}, {right_lane_vertices[3]}], dtype=np.int32)")
    
    print("\n" + "=" * 60)
else:
    print(f"\nError: Only {len(clicked_points)} points clicked. Need at least 4 points.")


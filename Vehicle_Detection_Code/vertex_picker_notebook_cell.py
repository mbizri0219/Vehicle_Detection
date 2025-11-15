"""
Copy this code into a Jupyter notebook cell to interactively define vertices.
This version uses matplotlib's ginput which works well in Jupyter notebooks.
"""

# ============================================================================
# STEP 1: Load and display a frame from your video
# ============================================================================
import cv2
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Path to your video
video_path = r'C:\Object_Detection_Projects\vehicle_detection\Dataset\Vehicle_Detection_Image_Dataset\sample_video.mp4'

# Open video and read a representative frame (you can change frame number)
cap = cv2.VideoCapture(video_path)
frame_number = 0  # Change this to use a different frame
cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
ret, frame = cap.read()
cap.release()

if not ret:
    print("Error: Could not read frame")
else:
    # Convert BGR to RGB for matplotlib
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Display the frame
    plt.figure(figsize=(15, 10))
    plt.imshow(frame_rgb)
    plt.title('Frame for vertex selection')
    plt.axis('on')
    plt.grid(True, alpha=0.3)
    plt.show()
    
    print(f"Frame dimensions: {frame.shape[1]} x {frame.shape[0]} (width x height)")
    print("\n" + "="*60)

# ============================================================================
# STEP 2: Click to define LEFT lane vertices
# ============================================================================
print("\nLEFT LANE: Click 4 points in this order:")
print("  1. Top-left corner")
print("  2. Top-right corner") 
print("  3. Bottom-right corner")
print("  4. Bottom-left corner")
print("\nClick on the image above, then run the next cell...")

# Display frame again and get clicks
plt.figure(figsize=(15, 10))
plt.imshow(frame_rgb)
plt.title('LEFT LANE: Click 4 points (top-left, top-right, bottom-right, bottom-left)')
plt.axis('on')
plt.grid(True, alpha=0.3)

# Get 4 clicks (this will pause and wait for mouse clicks)
left_points = plt.ginput(4, timeout=0, show_clicks=True)
plt.close()

# Convert to integer coordinates
left_vertices = np.array([(int(p[0]), int(p[1])) for p in left_points], dtype=np.int32)

print("\nLeft lane vertices captured:")
for i, v in enumerate(left_vertices):
    print(f"  Point {i+1}: ({v[0]}, {v[1]})")

# ============================================================================
# STEP 3: Click to define RIGHT lane vertices
# ============================================================================
print("\n" + "="*60)
print("\nRIGHT LANE: Click 4 points in this order:")
print("  1. Top-left corner")
print("  2. Top-right corner")
print("  3. Bottom-right corner")
print("  4. Bottom-left corner")

# Display frame again and get clicks
plt.figure(figsize=(15, 10))
plt.imshow(frame_rgb)
plt.title('RIGHT LANE: Click 4 points (top-left, top-right, bottom-right, bottom-left)')
plt.axis('on')
plt.grid(True, alpha=0.3)

# Get 4 clicks
right_points = plt.ginput(4, timeout=0, show_clicks=True)
plt.close()

# Convert to integer coordinates
right_vertices = np.array([(int(p[0]), int(p[1])) for p in right_points], dtype=np.int32)

print("\nRight lane vertices captured:")
for i, v in enumerate(right_vertices):
    print(f"  Point {i+1}: ({v[0]}, {v[1]})")

# ============================================================================
# STEP 4: Visualize the vertices on the frame
# ============================================================================
# Draw the quadrilaterals on the frame
frame_with_vertices = frame.copy()
cv2.polylines(frame_with_vertices, [left_vertices], isClosed=True, color=(0, 255, 0), thickness=3)
cv2.polylines(frame_with_vertices, [right_vertices], isClosed=True, color=(255, 0, 0), thickness=3)

# Add labels
for i, v in enumerate(left_vertices):
    cv2.circle(frame_with_vertices, tuple(v), 8, (0, 255, 0), -1)
    cv2.putText(frame_with_vertices, f'L{i+1}', (v[0]+10, v[1]), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

for i, v in enumerate(right_vertices):
    cv2.circle(frame_with_vertices, tuple(v), 8, (255, 0, 0), -1)
    cv2.putText(frame_with_vertices, f'R{i+1}', (v[0]+10, v[1]), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

# Display
frame_rgb_vertices = cv2.cvtColor(frame_with_vertices, cv2.COLOR_BGR2RGB)
plt.figure(figsize=(15, 10))
plt.imshow(frame_rgb_vertices)
plt.title('Verification: Check if vertices align correctly with lanes')
plt.axis('on')
plt.show()

# ============================================================================
# STEP 5: Generate the code to copy into your main script
# ============================================================================
print("\n" + "="*60)
print("COPY THIS CODE INTO YOUR MAIN SCRIPT:")
print("="*60)
print("\n# Define the vertices for the quadrilaterals")
print(f"vertices1 = np.array([{tuple(left_vertices[0])}, {tuple(left_vertices[1])}, "
      f"{tuple(left_vertices[2])}, {tuple(left_vertices[3])}], dtype=np.int32)")
print(f"vertices2 = np.array([{tuple(right_vertices[0])}, {tuple(right_vertices[1])}, "
      f"{tuple(right_vertices[2])}, {tuple(right_vertices[3])}], dtype=np.int32)")
print("\n" + "="*60)


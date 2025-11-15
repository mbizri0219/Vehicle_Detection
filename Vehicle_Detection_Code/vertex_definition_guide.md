# Guide: How to Define Quadrilateral Vertices for Lane Detection

## Overview

This guide shows you how to accurately determine the pixel coordinates for drawing quadrilaterals (4-sided polygons) on video frames to mark detection zones.

---

## Method 1: Interactive Click-to-Select (Easiest)

### Step 1: Load and Display a Frame

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load your video
video_path = r'C:\Object_Detection_Projects\vehicle_detection\Dataset\Vehicle_Detection_Image_Dataset\sample_video.mp4'
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

# Display the frame
plt.figure(figsize=(15, 10))
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title('Click on this image to get coordinates (use plt.ginput)')
plt.axis('on')
plt.show()
```

### Step 2: Use Matplotlib's Interactive Point Picker

```python
# Click 4 points on the image (in order: top-left, top-right, bottom-right, bottom-left)
# This will pause and wait for you to click
points = plt.ginput(4, timeout=0)  # Click 4 points, no timeout
print("Clicked points:", points)

# Convert to integer coordinates
vertices = np.array([(int(p[0]), int(p[1])) for p in points], dtype=np.int32)
print("\nVertices array:")
print(f"vertices = np.array({list(vertices)}, dtype=np.int32)")
```

---

## Method 2: Manual Coordinate Inspection

### Step 1: Display Frame with Grid

```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load frame
cap = cv2.VideoCapture(video_path)
ret, frame = cap.release()

# Create a copy with grid overlay
frame_with_grid = frame.copy()
h, w = frame.shape[:2]

# Draw grid lines every 50 pixels
for x in range(0, w, 50):
    cv2.line(frame_with_grid, (x, 0), (x, h), (128, 128, 128), 1)
for y in range(0, h, 50):
    cv2.line(frame_with_grid, (y, 0), (y, w), (128, 128, 128), 1)

# Add coordinate labels at corners
cv2.putText(frame_with_grid, f'(0, 0)', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
cv2.putText(frame_with_grid, f'({w}, {h})', (w-100, h-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

# Display
plt.figure(figsize=(15, 10))
plt.imshow(cv2.cvtColor(frame_with_grid, cv2.COLOR_BGR2RGB))
plt.title('Frame with coordinate grid - Use this to estimate vertex positions')
plt.show()
```

### Step 2: Use Image Editing Software

1. Take a screenshot of a frame from your video
2. Open it in an image editor (Paint, GIMP, Photoshop)
3. Hover over corners - most editors show coordinates in the status bar
4. Note down the (x, y) coordinates for each corner

---

## Method 3: Test and Refine (Recommended Workflow)

### Step 1: Make Initial Estimate

Start with approximate coordinates based on visual inspection:

```python
# Initial guess for left lane
vertices1_guess = np.array([(400, 300), (600, 300), (500, 600), (0, 600)], dtype=np.int32)
```

### Step 2: Visualize on Frame

```python
# Load frame
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()
cap.release()

# Draw the quadrilateral
frame_test = frame.copy()
cv2.polylines(frame_test, [vertices1_guess], isClosed=True, color=(0, 255, 0), thickness=3)

# Display
plt.figure(figsize=(15, 10))
plt.imshow(cv2.cvtColor(frame_test, cv2.COLOR_BGR2RGB))
plt.title('Test your vertices - adjust if needed')
plt.show()
```

### Step 3: Adjust Coordinates

If the quadrilateral doesn't align correctly:

- **Too far left?** Increase x-coordinates
- **Too far right?** Decrease x-coordinates
- **Too high?** Decrease y-coordinates
- **Too low?** Increase y-coordinates

### Step 4: Fine-tune with Small Adjustments

```python
# Adjust individual points
vertices1_adjusted = vertices1_guess.copy()
vertices1_adjusted[0] = (vertices1_guess[0][0] + 10, vertices1_guess[0][1] - 5)  # Move top-left
# Test again...
```

---

## Method 4: Use Video Frame Analyzer (Most Accurate)

Create a comprehensive tool that shows coordinates as you move the mouse:

```python
import cv2
import numpy as np

class VertexSelector:
    def __init__(self, video_path):
        self.video_path = video_path
        self.points = []
        self.current_frame = None
        self.frame_copy = None

    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.points.append((x, y))
            print(f"Point {len(self.points)}: ({x}, {y})")
            cv2.circle(self.frame_copy, (x, y), 8, (0, 255, 0), -1)
            if len(self.points) >= 2:
                # Draw line between consecutive points
                cv2.line(self.frame_copy, self.points[-2], self.points[-1], (0, 255, 0), 2)
            cv2.imshow('Vertex Selector', self.frame_copy)
        elif event == cv2.EVENT_MOUSEMOVE:
            # Show current mouse position
            temp_frame = self.frame_copy.copy()
            cv2.putText(temp_frame, f'({x}, {y})', (x+10, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
            cv2.circle(temp_frame, (x, y), 5, (255, 255, 0), 1)
            cv2.imshow('Vertex Selector', temp_frame)

    def select_vertices(self, frame_number=0):
        cap = cv2.VideoCapture(self.video_path)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, self.current_frame = cap.read()
        cap.release()

        if not ret:
            print("Error reading frame")
            return None

        self.frame_copy = self.current_frame.copy()
        cv2.namedWindow('Vertex Selector')
        cv2.setMouseCallback('Vertex Selector', self.mouse_callback)

        print("Click 4 points to define quadrilateral. Press 'r' to reset, 'q' to quit")
        cv2.imshow('Vertex Selector', self.frame_copy)

        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                self.points = []
                self.frame_copy = self.current_frame.copy()
                cv2.imshow('Vertex Selector', self.frame_copy)

        cv2.destroyAllWindows()
        return np.array(self.points, dtype=np.int32) if len(self.points) == 4 else None

# Usage:
selector = VertexSelector(video_path)
vertices = selector.select_vertices(frame_number=0)  # Use first frame
print(f"\nvertices = np.array({list(vertices)}, dtype=np.int32)")
```

---

## Best Practices

### 1. **Order Matters**

Always define vertices in a consistent order:

- **Clockwise or Counter-clockwise**: Choose one and stick with it
- **Typical order**: Top-left → Top-right → Bottom-right → Bottom-left

### 2. **Use Representative Frames**

- Don't use the first frame if vehicles aren't visible yet
- Use a frame where lanes are clearly visible
- Consider using multiple frames to verify consistency

### 3. **Account for Perspective**

- Lanes may appear wider at the bottom (closer to camera)
- Lanes may appear narrower at the top (farther from camera)
- Your quadrilateral should follow this perspective

### 4. **Test on Multiple Frames**

```python
# Test vertices on different frames
test_frames = [0, 100, 200, 300]  # Frame numbers to test
for frame_num in test_frames:
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    ret, frame = cap.read()
    # Draw vertices and check alignment
```

### 5. **Consider Video Resolution**

- Coordinates are in pixels, so they're resolution-dependent
- If you change video resolution, you'll need to recalculate vertices
- Use relative coordinates (percentages) if you need resolution independence

---

## Quick Reference: Coordinate System

```
(0, 0) ────────────────────────→ X (width)
  │
  │
  │
  │
  ↓
  Y (height)
```

- **X increases** from left to right
- **Y increases** from top to bottom
- **Origin (0, 0)** is at top-left corner

---

## Example: Your Current Vertices Explained

```python
vertices1 = np.array([(465, 350), (609, 350), (510, 630), (2, 630)], dtype=np.int32)
```

Breaking this down:

- `(465, 350)`: Top-left corner of left lane zone
- `(609, 350)`: Top-right corner of left lane zone
- `(510, 630)`: Bottom-right corner of left lane zone
- `(2, 630)`: Bottom-left corner of left lane zone

This creates a trapezoid (not a rectangle) because:

- Top width: 609 - 465 = 144 pixels
- Bottom width: 510 - 2 = 508 pixels
- This accounts for perspective (wider at bottom, closer to camera)

import os
from PIL import Image

# Attempt to import tkinter, but provide a fallback if it fails
try:
    import tkinter as tk
    from tkinter import filedialog
    HAS_GUI = True
except ImportError:
    HAS_GUI = False

class ImageRecognitionSystem:
    def __init__(self, target_size=(28, 28), threshold=128):
        self.target_size = target_size
        self.threshold = threshold
        self.database = {}

    def get_image_path(self):
        """Step 1: Image Acquisition (GUI or Manual fallback)"""
        if HAS_GUI:
            try:
                root = tk.Tk()
                root.withdraw()
                path = filedialog.askopenfilename(title="Select Image")
                root.destroy()
                if path: return path
            except Exception:
                pass # If GUI fails, move to manual input
        
        return input("Enter the full path to your image file: ").strip()

    def process(self, path):
        """Steps 2-5: Grayscale, Normalize, Binarize, Matrix"""
        try:
            img = Image.open(path).convert('L').resize(self.target_size)
            
            pixels = list(img.getdata())
            width = self.target_size[0]
            matrix = [[(1 if pixels[y * width + x] > self.threshold else 0) 
                       for x in range(width)] for y in range(self.target_size[1])]
            return matrix
        except Exception as e:
            print(f"Error: {e}")
            return None

    def compare(self, input_m, label):
        """Step 7: Comparison"""
        ref_m = self.database.get(label)
        if not ref_m: return 0
        
        matches = sum(1 for r in range(len(input_m)) 
                     for c in range(len(input_m[0])) 
                     if input_m[r][c] == ref_m[r][c])
        
        return (matches / (self.target_size[0] * self.target_size[1])) * 100

# --- RUN ---
recognizer = ImageRecognitionSystem()

# Step 6: Build Database
print("Select a REFERENCE image:")
ref_path = recognizer.get_image_path()
if ref_path:
    recognizer.database["Target"] = recognizer.process(ref_path)

# Step 7 & 8: Compare and Output
print("\nSelect an image to ANALYZE:")
test_path = recognizer.get_image_path()
if test_path:
    test_matrix = recognizer.process(test_path)
    score = recognizer.compare(test_matrix, "Target")
    print(f"\nResult: {score:.2f}% Match")
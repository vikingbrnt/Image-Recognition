import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

class ImageDigitMatcher:
    def __init__(self, ref_folder="Image", target_size=(20, 20), threshold=128):
        self.ref_folder = ref_folder
        self.target_size = target_size
        self.threshold = threshold
        self.database = {}  # Stores { "1": matrix, "2": matrix ... }

    def select_file(self, title):
        """Step 1: Graphical Image Acquisition"""
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(title=title)
        root.destroy()
        return file_path

    def to_matrix(self, path):
        """Steps 2-5: Grayscale, Normalize, Binarize, Matrix"""
        try:
            # Load and convert to Grayscale ('L') then Resize (Normalization)
            img = Image.open(path).convert('L').resize(self.target_size)
            pixels = list(img.getdata())
            w, h = self.target_size
            
            # Binarization based on threshold (1 for light, 0 for dark)
            return [[(1 if pixels[y * w + x] > self.threshold else 0) 
                     for x in range(w)] for y in range(h)]
        except Exception as e:
            print(f"Error processing {path}: {e}")
            return None

    def load_references(self):
        """Step 6: Build Database from 'Image' folder (1.png to 9.png)"""
        print(f"Building database from folder: '{self.ref_folder}'...")
        for i in range(1, 10):
            file_name = f"{i}.png"
            path = os.path.join(self.ref_folder, file_name)
            
            if os.path.exists(path):
                self.database[str(i)] = self.to_matrix(path)
                print(f"  [✓] Reference {i} loaded.")
            else:
                print(f"  [!] Missing: {file_name} in '{self.ref_folder}'")

    def run_identification(self):
        """Steps 7 & 8: Comparison and Result Display"""
        while True:
            print("\nOpening file selector for identification...")
            test_path = self.select_file("Select a number to identify")
            
            if not test_path:
                print("No file selected. Program ending.")
                break

            test_matrix = self.to_matrix(test_path)
            if not test_matrix: continue

            scores = {}
            for num, ref_matrix in self.database.items():
                # Compare pixel by pixel (both 0s and 1s)
                matches = sum(1 for r in range(self.target_size[1]) 
                             for c in range(self.target_size[0]) 
                             if test_matrix[r][c] == ref_matrix[r][c])
                
                score = (matches / (self.target_size[0] * self.target_size[1])) * 100
                scores[num] = score

            # Determine best match
            best_num = max(scores, key=scores.get)
            best_score = scores[best_num]

            self.visualize(test_matrix, self.database[best_num], best_num)
            
            print(f"\n--- Result ---")
            print(f"IDENTIFIED AS: {best_num}")
            print(f"MATCH SCORE:   {best_score:.2f}%")
            
            cont = input("\nIdentify another image? (y/n): ").lower()
            if cont != 'y': break

    def visualize(self, test_m, ref_m, label):
        """Visual terminal comparison"""
        print(f"\n[Input Selection]  |  [Reference {label}]")
        for r in range(self.target_size[1]):
            row_test = "".join(["#" if test_m[r][c] == 1 else "." for c in range(self.target_size[0])])
            row_ref = "".join(["#" if ref_m[r][c] == 1 else "." for c in range(self.target_size[0])])
            print(f"{row_test}   |   {row_ref}")

# --- Main Script ---
if __name__ == "__main__":
    # Ensure the folder 'Image' contains 1.png, 2.png, etc.
    app = ImageDigitMatcher(ref_folder="Image", target_size=(16, 16))
    app.load_references()

    if not app.database:
        print("\nFATAL ERROR: The reference database is empty.")
    else:
        app.run_identification()
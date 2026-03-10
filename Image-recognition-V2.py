import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageOps
import numpy as np  # New dependency for speed

class DigitIdentifier:
    def __init__(self, ref_folder="Image", target_size=(25, 25), threshold=128):
        self.ref_folder = ref_folder
        self.target_size = target_size
        self.threshold = threshold
        self.database = {} 

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title="Select Number")
        root.destroy()
        return path

    def to_array(self, path):
        """Processes image into a flat NumPy array (0s and 1s)"""
        try:
            img = Image.open(path).convert('L')
            img = ImageOps.invert(img)
            
            bbox = img.getbbox()
            if bbox:
                img = img.crop(bbox)
                img = ImageOps.expand(img, border=2, fill=0)
            
            img = img.resize(self.target_size)
            
            # Convert to NumPy array and binarize in one step
            arr = np.array(img)
            return (arr > self.threshold).astype(int).flatten()
        except Exception as e:
            print(f"Error: {e}")
            return None

    def load_database(self):
        print(f"Loading references...")
        for i in range(1, 9):
            path = os.path.join(self.ref_folder, f"{i}.png")
            if os.path.exists(path):
                # Store as flattened NumPy arrays
                self.database[str(i)] = self.to_array(path)
        print("Database Ready.")

    def find_best_match(self, test_path):
        test_arr = self.to_array(test_path)
        if test_arr is None: return

        best_label = None
        highest_score = -1

        # Leaner Comparison: No nested loops
        for label, ref_arr in self.database.items():
            # NumPy calculates matches across the whole array instantly
            matches = np.sum(test_arr == ref_arr)
            score = (matches / len(test_arr)) * 100
            
            if score > highest_score:
                highest_score = score
                best_label = label

        print(f"\nResult: {best_label} ({highest_score:.2f}% match)")
        # Visualize only the result
        self.visualize(test_arr, self.database[best_label], best_label)

    def visualize(self, test_arr, ref_arr, label):
        """Efficiently reshapes 1D arrays back to 2D for printing"""
        w = self.target_size[0]
        test_2d = test_arr.reshape(self.target_size)
        ref_2d = ref_arr.reshape(self.target_size)
        
        for r in range(w):
            t_row = "".join("1" if val else "." for val in test_2d[r])
            r_row = "".join("1" if val else "." for val in ref_2d[r])
            print(f"{t_row}   |   {r_row}")

# --- Main Logic ---
if __name__ == "__main__":
    app = DigitIdentifier(ref_folder="Image", target_size=(25, 25), threshold=128)
    app.load_database()

    if not app.database:
        print("\nError: Could not load the reference database. Check your 'Image' folder.")
    else:
        # Loop to allow multiple identifications
        while True:
            print("\nPlease select an image to identify...")
            selected_path = app.select_file()
            if not selected_path:
                print("No selection made. Exiting.")
                break
            
            app.find_best_match(selected_path)
            
            if input("\nIdentify another? (y/n): ").lower() != 'y':
                break
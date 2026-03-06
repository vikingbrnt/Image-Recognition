import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

class DigitIdentifier:
    def __init__(self, ref_folder="Image", target_size=(10, 10), threshold=128):
        self.ref_folder = ref_folder
        self.target_size = target_size
        self.threshold = threshold
        self.database = {}  # Stores reference matrices (1-9)

    def select_file(self):
        """Step 1: Graphical Image Acquisition (Window Selection)"""
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title="Select Number to Identify")
        root.destroy()
        return path

    def to_matrix(self, path):
        """Steps 2-5: Grayscale, Normalize, Binarize, Matrix"""
        try:
            # Load, Grayscale, and Normalize size
            img = Image.open(path).convert('L').resize(self.target_size)
            pixels = list(img.getdata())
            w, h = self.target_size
            
            # Binarization: 1 for light/background, 0 for dark/digit
            return [[(1 if pixels[y * w + x] > self.threshold else 0) 
                     for x in range(w)] for y in range(h)]
        except Exception as e:
            print(f"Error processing image: {e}")
            return None

    def load_database(self):
        """Step 6: Build the Reference Database"""
        print(f"Loading references from '{self.ref_folder}'...")
        for i in range(1, 10):
            filename = f"{i}.png"
            path = os.path.join(self.ref_folder, filename)
            if os.path.exists(path):
                self.database[str(i)] = self.to_matrix(path)
                print(f"  [✓] Loaded {filename}")
            else:
                print(f"  [!] Missing {filename}")

    def find_best_match(self, test_path):
        """Step 7 & 8: Comparison and Identification"""
        test_matrix = self.to_matrix(test_path)
        if not test_matrix: return

        best_label = None
        highest_score = -1
        all_results = {}

        for label, ref_matrix in self.database.items():
            # Pixel-by-pixel matching
            matches = 0
            total_pixels = self.target_size[0] * self.target_size[1]
            
            for r in range(self.target_size[1]):
                for c in range(self.target_size[0]):
                    if test_matrix[r][c] == ref_matrix[r][c]:
                        matches += 1
            
            score = (matches / total_pixels) * 100
            all_results[label] = score
            
            if score > highest_score:
                highest_score = score
                best_label = label

        # Display Visualization
        self.visualize(test_matrix, self.database[best_label], best_label)
        
        print(f"\n--- MATCHING RESULTS ---")
        print(f"The best match is Number: {best_label}")
        print(f"Confidence Level: {highest_score:.2f}%")
        
        print("\nFull Comparison Breakdown:")
        for num, s in sorted(all_results.items()):
            print(f"  Number {num}: {s:.2f}% match")

    def visualize(self, test_m, ref_m, label):
        """Displays the binary matrices in the terminal"""
        print(f"\n[Your Selection]  |  [Best Reference: {label}]")
        for r in range(self.target_size[1]):
            t_row = "".join(["1" if test_m[r][c] == 1 else "." for c in range(self.target_size[0])])
            r_row = "".join(["1" if ref_m[r][c] == 1 else "." for c in range(self.target_size[0])])
            print(f"{t_row}   |   {r_row}")

# --- Main Logic ---
if __name__ == "__main__":
    app = DigitIdentifier(ref_folder="Image", target_size=(10, 10))
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
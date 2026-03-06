class ImageProcessor:
    def __init__(self, threshold=128):
        self.threshold = threshold
        self.database = {} # Stores { "Label": [[Matrix]] }

    def to_grayscale_and_binary(self, rgb_matrix):
        """Converts a 3D RGB list to a 2D Binary (0/1) matrix."""
        binary_matrix = []
        for row in rgb_matrix:
            new_row = []
            for pixel in row:
                # RGB Average
                gray = sum(pixel) / 3
                # Binarization
                new_row.append(1 if gray > self.threshold else 0)
            binary_matrix.append(new_row)
        return binary_matrix

    def compare(self, input_matrix, label):
        """Calculates similarity percentage."""
        ref_matrix = self.database[label]
        matches = 0
        total_pixels = len(input_matrix) * len(input_matrix[0])
        
        for r in range(len(input_matrix)):
            for c in range(len(input_matrix[0])):
                if input_matrix[r][c] == ref_matrix[r][c]:
                    matches += 1
        
        return (matches / total_pixels) * 100

# Example Usage
processor = ImageProcessor()
# Reference: A simple 'X' shape in a 3x3 matrix
processor.database["Letter_X"] = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

# Output the Result
print("Reference Database Built.")
# result = processor.compare(my_input, "Letter_X")
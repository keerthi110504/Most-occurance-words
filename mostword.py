import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

class WordFrequencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Frequency Counter from CSV")

        # UI components
        self.label = tk.Label(root, text="Upload a CSV File with Text Data")
        self.label.pack(pady=10)

        self.upload_button = tk.Button(root, text="Browse File", command=self.browse_file)
        self.upload_button.pack(pady=5)

        self.count_button = tk.Button(root, text="Count Words", command=self.count_words)
        self.count_button.pack(pady=5)

        self.plot_button = tk.Button(root, text="Show Bar Graph", command=self.show_bar_graph)
        self.plot_button.pack(pady=5)

        self.filepath = None
        self.word_counts = None

    def browse_file(self):
        # Open file dialog to select a CSV file
        self.filepath = filedialog.askopenfilename(
            title="Open CSV File",
            filetypes=[("CSV Files", "*.csv")]
        )
        if self.filepath:
            self.label.config(text=f"Selected File: {self.filepath}")

    def count_words(self):
        if self.filepath is None:
            messagebox.showerror("Error", "Please select a file first!")
            return

        try:
            # Read the CSV file
            self.data = pd.read_csv(self.filepath)

            # Ensure there is at least one column
            if self.data.empty or self.data.shape[1] == 0:
                messagebox.showerror("Error", "CSV file is empty or has no columns.")
                return

            # Concatenate all text columns into one
            text = ' '.join(self.data.astype(str).fillna('').values.flatten())

            # Process the text
            text = text.lower()
            words = re.findall(r'\b\w+\b', text)
            self.word_counts = Counter(words)
            
            # Display a message
            messagebox.showinfo("Word Count", f"Word count completed. Total unique words: {len(self.word_counts)}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file: {e}")

    def show_bar_graph(self):
        if self.word_counts is None:
            messagebox.showerror("Error", "Please count words first!")
            return

        # Prepare data for plotting
        most_common_words = self.word_counts.most_common(10)
        words, counts = zip(*most_common_words)

        # Plot the bar graph
        plt.figure(figsize=(10, 6))
        plt.bar(words, counts, color='skyblue')
        plt.title('Top 10 Most Frequent Words')
        plt.xlabel('Words')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Display the plot
        plt.show()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = WordFrequencyApp(root)
    root.mainloop()

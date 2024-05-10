import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import Counter

class DataVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PYVISUAL")

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0)

        self.data_label = ttk.Label(self.main_frame, text="Data:")
        self.data_label.grid(row=0, column=0, sticky="w")
        self.data_entry = ttk.Entry(self.main_frame, width=30)
        self.data_entry.grid(row=0, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(self.main_frame, text="Load Data", command=self.load_data)
        self.load_button.grid(row=0, column=2, padx=5, pady=5)

        self.analysis_menu = tk.Menu(root)
        self.root.config(menu=self.analysis_menu)

        self.analysis_submenu = tk.Menu(self.analysis_menu, tearoff=0)
        self.analysis_menu.add_cascade(label="Analysis Parameters", menu=self.analysis_submenu)
        self.analysis_submenu.add_command(label="Export Data", command=self.export_data)
        self.analysis_submenu.add_command(label="View Analysis", command=self.view_analysis)

        self.x_label_label = ttk.Label(self.main_frame, text="X Label:")
        self.x_label_label.grid(row=1, column=0, sticky="w")
        self.x_label_combobox = ttk.Combobox(self.main_frame, width=27, state="readonly")
        self.x_label_combobox.grid(row=1, column=1, padx=5, pady=5)

        self.y_label_label = ttk.Label(self.main_frame, text="Y Label:")
        self.y_label_label.grid(row=2, column=0, sticky="w")
        self.y_label_combobox = ttk.Combobox(self.main_frame, width=27, state="readonly")
        self.y_label_combobox.grid(row=2, column=1, padx=5, pady=5)

        self.title_label = ttk.Label(self.main_frame, text="Plot Title:")
        self.title_label.grid(row=3, column=0, sticky="w")
        self.title_entry = ttk.Entry(self.main_frame, width=30)
        self.title_entry.grid(row=3, column=1, padx=5, pady=5)

        self.plot_type_label = ttk.Label(self.main_frame, text="Plot Type:")
        self.plot_type_label.grid(row=4, column=0, sticky="w")
        self.plot_type_combobox = ttk.Combobox(self.main_frame, values=["line", "bar", "scatter", "pie", "histogram", "heatmap"], state="readonly")
        self.plot_type_combobox.current(0)
        self.plot_type_combobox.grid(row=4, column=1, padx=5, pady=5)

        self.marker_label = ttk.Label(self.main_frame, text="Marker (for line plot):")
        self.marker_label.grid(row=5, column=0, sticky="w")
        self.marker_combobox = ttk.Combobox(self.main_frame, width=27, state="readonly")
        self.marker_combobox['values'] = ['', '.', 'o', 'x', '+', '*', 's', 'D']
        self.marker_combobox.current(0)
        self.marker_combobox.grid(row=5, column=1, padx=5, pady=5)

        self.visualize_button = ttk.Button(self.main_frame, text="Visualize", command=self.visualize)
        self.visualize_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.dataset = None

    def load_data(self):
        filename = filedialog.askopenfilename()
        self.data_entry.delete(0, tk.END)
        self.data_entry.insert(0, filename)
        self.load_dataset()

    def export_data(self):
        if self.dataset is None:
            messagebox.showerror("Error", "Please load a dataset first.")
            return

        filename = "result.txt"
        try:
            with open(filename, 'w') as f:
                f.write("Dataset Description:\n")
                f.write(self.dataset.describe().to_string() + "\n\n")
                f.write("Correlation Matrix:\n")
                f.write(self.dataset.corr().to_string() + "\n\n")
                f.write("Top 10 Most Common Words:\n")
                word_counts = Counter(" ".join(self.dataset).split()).most_common(10)
                f.write("\n".join([f"{word}: {count}" for word, count in word_counts]) + "\n\n")
                messagebox.showinfo("Export Data", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def view_analysis(self):
        if self.dataset is None:
            messagebox.showerror("Error", "Please load a dataset first.")
            return
        top = tk.Toplevel(self.root)
        top.title("Analysis View")
        text = tk.Text(top)
        text.pack(expand=True, fill="both")
        text.insert(tk.END, "Dataset Description:\n")
        text.insert(tk.END, self.dataset.describe().to_string() + "\n\n")
        text.insert(tk.END, "Top 10 Most Common Words:\n")
        word_counts = Counter(" ".join(self.dataset).split()).most_common(10)
        text.insert(tk.END, "\n".join([f"{word}: {count}" for word, count in word_counts]) + "\n\n")
        text.config(state=tk.DISABLED)

    def load_dataset(self):
        filename = self.data_entry.get()
        try:
            self.dataset = pd.read_csv(filename)
            self.dataset.fillna(self.dataset.mean(), inplace=True) 
            for col in self.dataset.select_dtypes(include=['object']).columns:
                self.dataset[col] = self.dataset[col].astype('category') 
            clean_column_names = [col.replace('_', ' ').title() for col in self.dataset.columns]

            self.x_label_combobox['values'] = clean_column_names
            self.y_label_combobox['values'] = clean_column_names

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def visualize(self):
        if self.dataset is None:
            messagebox.showerror("Error", "Please load a dataset first.")
            return

        x_label = self.x_label_combobox.get()
        y_label = self.y_label_combobox.get()
        title = self.title_entry.get()
        plot_type = self.plot_type_combobox.get()
        marker = self.marker_combobox.get()

        try:
            if plot_type == 'pie':
                self.plot_pie_chart(x_label, title)
            elif plot_type == 'histogram':
                self.plot_histogram(x_label, title)
            elif plot_type == 'heatmap':
                self.plot_heatmap(title)
            elif plot_type == 'bar':
                self.plot_bar_chart(x_label, y_label, title)
            elif plot_type == 'scatter':
                self.plot_scatter(x_label, y_label, title)
            else:
                self.plot_basic_chart(x_label, y_label, title, plot_type, marker)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_basic_chart(self, x_label, y_label, title, plot_type, marker):
        plt.figure(figsize=(8, 6))
        if plot_type == 'line':
            grouped_data = self.dataset.groupby(x_label)[y_label].mean()
            plt.plot(grouped_data.index, grouped_data.values, marker=marker)
            plt.xlim(self.dataset[x_label].min(), self.dataset[x_label].max())       
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.show()
    def plot_scatter(self, x_label, y_label, title):
        top = tk.Toplevel(self.root)
        top.title("Select Other Column")
        other_column_label = ttk.Label(top, text="Other Column:")
        other_column_label.grid(row=0, column=0, sticky="w")
        other_column_combobox = ttk.Combobox(top, width=27, state="readonly")
        other_column_combobox.grid(row=0, column=1, padx=5, pady=5)
        other_column_combobox['values'] = list(self.dataset.columns)
        other_column_combobox.current(0)
        def plot():
            other_column = other_column_combobox.get()
            plt.figure(figsize=(10, 8))
            plt.title(title)
            plt.xlabel(x_label)
            plt.ylabel(y_label)
            sns.scatterplot(x=self.dataset[x_label], y=self.dataset[y_label], hue=self.dataset[other_column], palette='viridis')
            plt.legend(title=other_column, loc='upper right')
            plt.show()
            top.destroy()  
        plot_button = ttk.Button(top, text="Plot", command=plot)
        plot_button.grid(row=1, column=0, columnspan=2, pady=10)


    def plot_pie_chart(self, x_label, title):
        plt.figure(figsize=(8, 6))
        age_groups = pd.cut(self.dataset[x_label], bins=range(0, 100, 20))
        age_group_counts = age_groups.value_counts()
        age_group_counts.plot(kind='pie', autopct='%1.1f%%')
        plt.title(title)
        plt.ylabel('')
        plt.show()


    def plot_histogram(self, x_label, title):
        plt.figure(figsize=(10, 8))
        sns.histplot(self.dataset[x_label], kde=True, color='skyblue', edgecolor='black', linewidth=1.5)
        mean_value = self.dataset[x_label].mean()
        median_value = self.dataset[x_label].median()
        std_dev = self.dataset[x_label].std()
        plt.axvline(mean_value, color='red', linestyle='--', label=f'Mean: {mean_value:.2f}')
        plt.axvline(median_value, color='green', linestyle='--', label=f'Median: {median_value:.2f}')
        plt.axvline(mean_value + std_dev, color='orange', linestyle='--', label=f'Std Dev: {std_dev:.2f}')
        plt.axvline(mean_value - std_dev, color='orange', linestyle='--')
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    def plot_bar_chart(self, x_label, y_label, title):
        plt.figure(figsize=(8, 6))
        sns.barplot(x=self.dataset[x_label], y=self.dataset[y_label], estimator=sum, ci=None, palette="viridis")
        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()


    def plot_heatmap(self, title):
        plt.figure(figsize=(10, 8))
        if self.dataset is None:
            messagebox.showerror("Error", "Please load a dataset first.")
            return
        correlations = self.dataset.corr()
        if correlations.empty:
            messagebox.showwarning("Warning", "No correlations to plot.")
            return
        sns.heatmap(correlations, annot=True, fmt=".2f", cmap='coolwarm', center=0, square=True)
        plt.title(title)
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = DataVisualizerApp(root)
    root.mainloop()

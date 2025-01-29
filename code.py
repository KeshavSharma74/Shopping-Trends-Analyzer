import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
from datetime import datetime
import os

class ShoppingTrendsAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Shopping Trends Analyzer")
        self.root.geometry("1200x800")
        self.df = None
        
        # Create main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create UI elements
        self.create_upload_section()
        self.create_analysis_section()
        self.create_visualization_section()
        
    def create_upload_section(self):
        # File Upload Section
        upload_frame = ttk.LabelFrame(self.main_container, text="Data Upload", padding="5")
        upload_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(upload_frame, text="Upload CSV", command=self.upload_file).grid(row=0, column=0, padx=5)
        ttk.Button(upload_frame, text="Load Sample Data", command=self.load_sample_data).grid(row=0, column=1, padx=5)
        
    def create_analysis_section(self):
        # Analysis Options Section
        analysis_frame = ttk.LabelFrame(self.main_container, text="Analysis Options", padding="5")
        analysis_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        analysis_options = [
            "Total Sales Over Time",
            "Popular Categories",
            "Customer Spending Patterns",
            "Peak Shopping Hours"
        ]
        
        self.analysis_var = tk.StringVar()
        for i, option in enumerate(analysis_options):
            ttk.Radiobutton(analysis_frame, text=option, value=option, 
                           variable=self.analysis_var, command=self.update_visualization
                           ).grid(row=i, column=0, sticky=tk.W, pady=2)
            
    def create_visualization_section(self):
        # Visualization Section
        self.viz_frame = ttk.LabelFrame(self.main_container, text="Visualization", padding="5")
        self.viz_frame.grid(row=1, column=1, rowspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                self.df['Date'] = pd.to_datetime(self.df['Date'])
                messagebox.showinfo("Success", "Data loaded successfully!")
                self.update_visualization()
            except Exception as e:
                messagebox.showerror("Error", f"Error loading file: {str(e)}")
                
    def load_sample_data(self):
        # Create sample data
        dates = pd.date_range(start='2024-01-01', end='2024-01-31', freq='D')
        products = ['Laptop', 'Shoes', 'T-shirt', 'Phone', 'Watch']
        categories = ['Electronics', 'Fashion', 'Fashion', 'Electronics', 'Accessories']
        
        data = []
        for date in dates:
            for p, c in zip(products, categories):
                price = np.random.uniform(50, 1000) if c == 'Electronics' else np.random.uniform(20, 200)
                quantity = np.random.randint(1, 10)
                data.append({
                    'Date': date,
                    'Product': p,
                    'Category': c,
                    'Price': price,
                    'Quantity': quantity,
                    'Total_Sales': price * quantity
                })
        
        self.df = pd.DataFrame(data)
        messagebox.showinfo("Success", "Sample data loaded successfully!")
        self.update_visualization()
        
    def update_visualization(self):
        if self.df is None:
            return
            
        self.ax.clear()
        analysis_type = self.analysis_var.get()
        
        if analysis_type == "Total Sales Over Time":
            daily_sales = self.df.groupby('Date')['Total_Sales'].sum().reset_index()
            self.ax.plot(daily_sales['Date'], daily_sales['Total_Sales'])
            self.ax.set_title('Daily Sales Trend')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Total Sales ($)')
            plt.xticks(rotation=45)
            
        elif analysis_type == "Popular Categories":
            category_sales = self.df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
            category_sales.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Sales by Category')
            self.ax.set_xlabel('Category')
            self.ax.set_ylabel('Total Sales ($)')
            plt.xticks(rotation=45)
            
        elif analysis_type == "Customer Spending Patterns":
            price_bins = pd.cut(self.df['Price'], bins=5)
            price_distribution = self.df.groupby(price_bins).size()
            price_distribution.plot(kind='bar', ax=self.ax)
            self.ax.set_title('Price Distribution')
            self.ax.set_xlabel('Price Range')
            self.ax.set_ylabel('Number of Transactions')
            plt.xticks(rotation=45)
            
        elif analysis_type == "Peak Shopping Hours":
            self.df['Hour'] = self.df['Date'].dt.hour
            hourly_sales = self.df.groupby('Hour')['Total_Sales'].sum()
            hourly_sales.plot(kind='line', ax=self.ax, marker='o')
            self.ax.set_title('Sales by Hour of Day')
            self.ax.set_xlabel('Hour')
            self.ax.set_ylabel('Total Sales ($)')
            
        self.fig.tight_layout()
        self.canvas.draw()
        
    def save_report(self):
        if self.df is None:
            messagebox.showwarning("Warning", "No data to generate report!")
            return
            
        # Create report directory if it doesn't exist
        if not os.path.exists('reports'):
            os.makedirs('reports')
            
        # Save current visualization
        plt.savefig('reports/visualization.png')
        
        # Generate summary statistics
        report = f"""
        Shopping Trends Analysis Report
        Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        Summary Statistics:
        ------------------
        Total Sales: ${self.df['Total_Sales'].sum():,.2f}
        Total Transactions: {len(self.df):,}
        Average Transaction Value: ${self.df['Total_Sales'].mean():,.2f}
        
        Top Categories by Sales:
        {self.df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False).to_string()}
        
        Top Products by Quantity:
        {self.df.groupby('Product')['Quantity'].sum().sort_values(ascending=False).to_string()}
        """
        
        with open('reports/analysis_report.txt', 'w') as f:
            f.write(report)
            
        messagebox.showinfo("Success", "Report saved in 'reports' directory!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ShoppingTrendsAnalyzer(root)
    
    # Add Report Generation Button
    ttk.Button(app.main_container, text="Generate Report", 
               command=app.save_report).grid(row=2, column=0, pady=5)
    
    root.mainloop()
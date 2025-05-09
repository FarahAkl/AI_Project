import tkinter as tk
from tkinter import messagebox, LabelFrame
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Create the main window
root = tk.Tk()
root.title("Interactive Map Coloring Tool")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

# Global variables
G = nx.Graph()
color_map = {}

# Available colors
colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33']  # 4-color map theorem

# Function to add a new region
def add_region():
    region_name = region_entry.get().strip()
    if not region_name:
        messagebox.showwarning("Input Error", "Please enter a valid region name.")
        return
    if region_name in G.nodes:
        messagebox.showwarning("Duplicate Region", f"Region '{region_name}' already exists.")
        return
    G.add_node(region_name)
    update_graph_display()
    region_entry.delete(0, tk.END)

# Function to add a border between two regions
def add_border():
    region1 = border_entry1.get().strip()
    region2 = border_entry2.get().strip()
    if not region1 or not region2:
        messagebox.showwarning("Input Error", "Please enter two valid regions.")
        return
    if region1 not in G.nodes or region2 not in G.nodes:
        messagebox.showwarning("Invalid Region", "One or both regions do not exist.")
        return
    if G.has_edge(region1, region2):
        messagebox.showwarning("Duplicate Border", f"Border between '{region1}' and '{region2}' already exists.")
        return
    G.add_edge(region1, region2)
    update_graph_display()
    border_entry1.delete(0, tk.END)
    border_entry2.delete(0, tk.END)

# Function to update the graph display
def update_graph_display():
    ax.clear()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10, font_weight='bold', ax=ax)
    canvas.draw()

# CSP Backtracking Algorithm
def is_safe(node, color, assignment):
    for neighbor in G.neighbors(node):
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(assignment, nodes):
    if len(assignment) == len(nodes):
        return assignment
    node = next(n for n in nodes if n not in assignment)
    for color in range(len(colors)):
        if is_safe(node, color, assignment):
            assignment[node] = color
            result = backtrack(assignment, nodes)
            if result:
                return result
            del assignment[node]
    return None

def color_map_func():
    global color_map
    if not G.nodes:
        messagebox.showwarning("Empty Map", "Please add regions and borders first.")
        return

    assignment = backtrack({}, list(G.nodes))
    if assignment is None:
        messagebox.showerror("CSP Failed", "Unable to color the map with the given colors.")
        return

    color_map = assignment

    node_colors = [colors[color_map[node]] for node in G.nodes]
    ax.clear()
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray',
            font_size=10, font_weight='bold', ax=ax)
    canvas.draw()

# Function to save the map as an image
def save_map():
    if not G.nodes:
        messagebox.showwarning("Empty Map", "There is no map to save.")
        return
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    node_colors = [colors[color_map[node]] for node in G.nodes]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray',
            font_size=10, font_weight='bold')
    plt.savefig("colored_map.png")
    plt.close()
    messagebox.showinfo("Save Successful", "The map has been saved as 'colored_map.png'.")

# GUI Components
input_frame = LabelFrame(root, text="Map Input", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10)
input_frame.pack(fill="x", padx=20, pady=10)

tk.Label(input_frame, text="Add Region:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, padx=5, pady=5)
region_entry = tk.Entry(input_frame, width=20, font=("Arial", 10))
region_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(input_frame, text="Add", command=add_region, bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5, pady=5)

tk.Label(input_frame, text="Add Border Between:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, padx=5, pady=5)
border_entry1 = tk.Entry(input_frame, width=10, font=("Arial", 10))
border_entry1.grid(row=1, column=1, padx=5, pady=5)
border_entry2 = tk.Entry(input_frame, width=10, font=("Arial", 10))
border_entry2.grid(row=1, column=2, padx=5, pady=5)
tk.Button(input_frame, text="Add", command=add_border, bg="#4CAF50", fg="white", font=("Arial", 10)).grid(row=1, column=3, padx=5, pady=5)

button_frame = LabelFrame(root, text="Actions", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10)
button_frame.pack(fill="x", padx=20, pady=10)

tk.Button(button_frame, text="Color Map", command=color_map_func, bg="#008CBA", fg="white", font=("Arial", 10), width=15).pack(side="left", padx=10)
tk.Button(button_frame, text="Save Map", command=save_map, bg="#f44336", fg="white", font=("Arial", 10), width=15).pack(side="right", padx=10)

graph_frame = LabelFrame(root, text="Graph Display", bg="#f0f0f0", font=("Arial", 12, "bold"), padx=10, pady=10)
graph_frame.pack(fill="both", expand=True, padx=20, pady=10)

fig, ax = plt.subplots(figsize=(6, 4))
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill="both", expand=True)

# Start the GUI event loop
root.mainloop()
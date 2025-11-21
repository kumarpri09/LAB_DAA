import csv
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def load_graph_from_csv(file_path):
    G = nx.DiGraph()
    try:
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)

            required_cols = {"Order", "Destination", "Distance"}
            if not required_cols.issubset(reader.fieldnames):
                raise ValueError("CSV must contain: source, target, weight")

            for row in reader:
                src = row["Order"].strip()
                tgt = row["Destination"].strip()
                w = float(row["Distance"])
                G.add_edge(src, tgt, weight=w)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read CSV:\n{e}")
        return None
    return G

def shortest_path_dijkstra(G, start, end):
    try:
        length, path = nx.single_source_dijkstra(G, start, end, weight="weight")
        return length, path
    except nx.NetworkXNoPath:
        return float("inf"), []
    except nx.NodeNotFound:
        return None, None

def shortest_path_floyd_warshall(G, start, end):
    try:
        pred, dist = nx.floyd_warshall_predecessor_and_distance(G, weight="weight")
        length = dist[start][end]

        if length == float("inf"):
            return float("inf"), []

        path = nx.reconstruct_path(start, end, pred)
        return length, path

    except Exception:
        return None, None

def draw_graph(G, path, title):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue',
            node_size=800, font_size=10)
    nx.draw_networkx_edge_labels(G, pos,
                                 edge_labels=nx.get_edge_attributes(G, "weight"))
    if path:
        edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=edges,
                               edge_color='red', width=2, arrows=True)
    plt.title(title)
    plt.show()

def select_csv():
    global G
    file_path = filedialog.askopenfilename(
        title="Select CSV File",
        filetypes=[("CSV Files", "*.csv")]
    )

    if not file_path:
        return

    G = load_graph_from_csv(file_path)
    if G is None:
        return

    city_list = sorted(list(G.nodes()))
    start_menu["values"] = city_list
    end_menu["values"] = city_list
    messagebox.showinfo("Success", "CSV Loaded Successfully!")

def compute_paths():
    if G is None:
        messagebox.showerror("Error", "Load a CSV file first.")
        return
    
    start = start_var.get()
    end = end_var.get()

    if not start or not end:
        messagebox.showerror("Error", "Select both start and end cities.")
        return

    d_length, d_path = shortest_path_dijkstra(G, start, end)
    f_length, f_path = shortest_path_floyd_warshall(G, start, end)
    result_box.delete("1.0", tk.END)

    result_box.insert(tk.END, "--- Dijkstra Shortest Path ---\n")
    result_box.insert(tk.END, f"Distance: {d_length}\nPath: {d_path}\n\n")

    result_box.insert(tk.END, "--- Floyd–Warshall Shortest Path ---\n")
    result_box.insert(tk.END, f"Distance: {f_length}\nPath: {f_path}\n")

    draw_graph(G, d_path, "Dijkstra Shortest Path")
    draw_graph(G, f_path, "Floyd–Warshall Shortest Path")

root = tk.Tk()
root.title("Shortest Path Finder (Dijkstra + Floyd–Warshall)")
root.geometry("650x500")
root.resizable(False, False)

G = None
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="Load CSV", font=("Arial", 12),
          command=select_csv).grid(row=0, column=0, padx=10)

start_var = tk.StringVar()
end_var = tk.StringVar()

tk.Label(frame, text="Start City:", font=("Arial", 12)).grid(row=1, column=0, pady=10)
start_menu = ttk.Combobox(frame, textvariable=start_var, width=20)
start_menu.grid(row=1, column=1)

tk.Label(frame, text="End City:", font=("Arial", 12)).grid(row=2, column=0, pady=10)
end_menu = ttk.Combobox(frame, textvariable=end_var, width=20)
end_menu.grid(row=2, column=1)

tk.Button(frame, text="Compute Shortest Paths", font=("Arial", 12),
          command=compute_paths).grid(row=3, column=0, columnspan=2, pady=15)

result_box = tk.Text(root, height=12, width=70, font=("Arial", 10))
result_box.pack(pady=10)

root.mainloop()
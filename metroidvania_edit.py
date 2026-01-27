import tkinter as tk

# Configuration matches the JS Map (10 columns, 8 rows)
COLS = 10
ROWS = 8
TILE_SIZE = 50

class LevelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon-Vania Level Architect")
        
        self.current_char = "#"
        self.grid_data = [["." for _ in range(COLS)] for _ in range(ROWS)]
        
        # UI Buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Wall (#)", command=lambda: self.set_tool("#"), bg="#333", fg="white").grid(row=0, column=0)
        tk.Button(btn_frame, text="Empty (.)", command=lambda: self.set_tool("."), bg="white").grid(row=0, column=1)
        tk.Button(btn_frame, text="Exit (_)", command=lambda: self.set_tool("_"), bg="#555", fg="yellow").grid(row=0, column=2)
        tk.Button(btn_frame, text="Upgrade (J)", command=lambda: self.set_tool("J"), bg="purple", fg="white").grid(row=0, column=3)
        tk.Button(btn_frame, text="GENERATE CODE", command=self.generate_code, bg="green", fg="white").grid(row=0, column=4, padx=20)

        # Canvas for drawing
        self.canvas = tk.Canvas(root, width=COLS*TILE_SIZE, height=ROWS*TILE_SIZE, bg="black")
        self.canvas.pack(padx=20, pady=20)
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.paint)

        self.draw_grid()

    def set_tool(self, char):
        self.current_char = char

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c * TILE_SIZE, r * TILE_SIZE
                x2, y2 = x1 + TILE_SIZE, y1 + TILE_SIZE
                
                color = "black"
                char = self.grid_data[r][c]
                if char == "#": color = "#222"
                elif char == "_": color = "#444"
                elif char == "J": color = "purple"
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#333")
                if char != ".":
                    self.canvas.create_text(x1+25, y1+25, text=char, fill="white")

    def paint(self, event):
        c = event.x // TILE_SIZE
        r = event.y // TILE_SIZE
        if 0 <= r < ROWS and 0 <= c < COLS:
            self.grid_data[r][c] = self.current_char
            self.draw_grid()

    def generate_code(self):
        output = '[\n'
        for row in self.grid_data:
            line = "".join(row)
            output += f'    "{line}",\n'
        output = output.rstrip(',\n') + '\n]'
        
        # Show in a popup
        popup = tk.Toplevel(self.root)
        popup.title("Copy this code")
        text_area = tk.Text(popup, height=12, width=30)
        text_area.insert(tk.END, output)
        text_area.pack(padx=10, pady=10)
        print("Generated Layout:\n", output)

if __name__ == "__main__":
    root = tk.Tk()
    editor = LevelEditor(root)
    root.mainloop()
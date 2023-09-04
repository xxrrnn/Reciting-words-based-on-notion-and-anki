import tkinter as tk
from PIL import Image, ImageTk

class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("图片查看器")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill="both", expand=True)

        self.image = None
        self.image_tk = None
        self.img_width = 0
        self.img_height = 0

        self.load_image("2023-08-29.png")  # 自动加载图片

        self.canvas.bind("<Configure>", self.resize_image)
        self.canvas.bind("<ButtonPress-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<ButtonRelease-1>", self.end_drag)

        self.drag_data = {"x": 0, "y": 0}
        self.dragging = False

    def load_image(self, image_path):
        image = Image.open(image_path)
        self.image = image
        self.img_width, self.img_height = image.size
        self.image_tk = ImageTk.PhotoImage(image)

        self.canvas.config(scrollregion=(0, 0, self.img_width, self.img_height))
        self.canvas.create_image(0, 0, anchor="nw", image=self.image_tk)

        # 设置窗口高度与图片高度一致
        self.root.geometry(f"{self.img_width}x{self.img_height}")

    def resize_image(self, event):
        if self.image:
            new_width = event.width
            self.canvas.itemconfig(self.image_tk, width=new_width)

    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.dragging = True

    def drag(self, event):
        if self.dragging:
            delta_x = event.x - self.drag_data["x"]
            delta_y = event.y - self.drag_data["y"]
            self.canvas.xview_scroll(-delta_x, "units")
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

    def end_drag(self, event):
        self.dragging = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()

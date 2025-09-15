import tkinter as tk
from watermarker_gui import WaterMarkerApp


# GUI
root = tk.Tk()
app = WaterMarkerApp(root)
root.mainloop()

# --- Main content on the left ---
main_frame = tk.Frame(root, bg="lightgrey")

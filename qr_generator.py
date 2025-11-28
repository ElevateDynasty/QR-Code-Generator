import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser
import qrcode
from PIL import Image, ImageTk
import os


class QRCodeGenerator:
    
    def __init__(self, root):
        self.root = root
        self.root.title("🔲 QR Code Generator")
        self.root.geometry("550x680")
        self.root.resizable(True, True)
        self.root.configure(bg="#f0f0f0")
        
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.qr_image = None
        
        self.create_widgets()
        
    def create_widgets(self):
        canvas_container = ttk.Frame(self.root)
        canvas_container.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_container, bg="#f0f0f0", highlightthickness=0)
        
        scrollbar = ttk.Scrollbar(canvas_container, orient=tk.VERTICAL, command=self.canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.scrollable_frame = ttk.Frame(self.canvas, padding="15")
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)
        
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        
        title_label = tk.Label(
            self.scrollable_frame,
            text="🔲 QR Code Generator",
            font=("Helvetica", 20, "bold"),
            bg="#f0f0f0",
            fg="#333333"
        )
        title_label.pack(pady=15)
        
        main_frame = ttk.Frame(self.scrollable_frame, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        input_frame = ttk.LabelFrame(main_frame, text="📝 Enter Text or URL", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        self.text_input = tk.Text(
            input_frame,
            height=3,
            width=50,
            font=("Consolas", 11),
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=2
        )
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.insert("1.0", "https://github.com")
        
        settings_frame = ttk.LabelFrame(main_frame, text="⚙️ Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        ec_frame = ttk.Frame(settings_frame)
        ec_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(ec_frame, text="Error Correction:", font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.error_correction = ttk.Combobox(
            ec_frame,
            values=["L - 7% (Low)", "M - 15% (Medium)", "Q - 25% (Quartile)", "H - 30% (High)"],
            width=20,
            state="readonly"
        )
        self.error_correction.set("H - 30% (High)")
        self.error_correction.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(
            ec_frame,
            text="(Higher = more damage resistant)",
            font=("Helvetica", 8),
            foreground="gray"
        ).pack(side=tk.LEFT)
        
        size_frame = ttk.Frame(settings_frame)
        size_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(size_frame, text="QR Code Size:", font=("Helvetica", 10)).pack(side=tk.LEFT)
        self.box_size = ttk.Scale(
            size_frame,
            from_=5,
            to=15,
            orient=tk.HORIZONTAL,
            length=150
        )
        self.box_size.set(10)
        self.box_size.pack(side=tk.LEFT, padx=10)
        
        self.size_label = ttk.Label(size_frame, text="10", font=("Helvetica", 10, "bold"))
        self.size_label.pack(side=tk.LEFT)
        
        self.box_size.configure(command=self.update_size_label)
        
        color_frame = ttk.Frame(settings_frame)
        color_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(color_frame, text="Colors:", font=("Helvetica", 10)).pack(side=tk.LEFT)
        
        self.fill_btn = ttk.Button(
            color_frame,
            text="QR Color",
            command=self.choose_fill_color,
            width=12
        )
        self.fill_btn.pack(side=tk.LEFT, padx=5)
        
        self.fill_preview = tk.Label(
            color_frame,
            bg=self.fill_color,
            width=3,
            height=1,
            relief=tk.SOLID,
            bd=1
        )
        self.fill_preview.pack(side=tk.LEFT, padx=2)
        
        self.back_btn = ttk.Button(
            color_frame,
            text="Background",
            command=self.choose_back_color,
            width=12
        )
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        self.back_preview = tk.Label(
            color_frame,
            bg=self.back_color,
            width=3,
            height=1,
            relief=tk.SOLID,
            bd=1
        )
        self.back_preview.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(
            color_frame,
            text="Reset",
            command=self.reset_colors,
            width=8
        ).pack(side=tk.LEFT, padx=10)
        
        generate_btn = tk.Button(
            main_frame,
            text="✨ Generate QR Code",
            command=self.generate_qr,
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=10
        )
        generate_btn.pack(pady=15)
        
        preview_frame = ttk.LabelFrame(main_frame, text="👁️ Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_label = ttk.Label(preview_frame, anchor=tk.CENTER)
        self.preview_label.pack(expand=True, fill=tk.BOTH)
        
        self.preview_placeholder = ttk.Label(
            preview_frame,
            text="Your QR code will appear here",
            font=("Helvetica", 11),
            foreground="gray"
        )
        self.preview_placeholder.pack(expand=True)
        
        save_btn = tk.Button(
            main_frame,
            text="💾 Save QR Code",
            command=self.save_qr,
            font=("Helvetica", 11, "bold"),
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        save_btn.pack(pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("Ready to generate QR codes!")
        
        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W,
            padding=(10, 5)
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    
    def update_size_label(self, value):
        self.size_label.configure(text=str(int(float(value))))
    
    def choose_fill_color(self):
        color = colorchooser.askcolor(
            title="Choose QR Code Color",
            initialcolor=self.fill_color
        )
        if color[1]:
            self.fill_color = color[1]
            self.fill_preview.configure(bg=self.fill_color)
            self.status_var.set(f"QR color changed to {self.fill_color}")
    
    def choose_back_color(self):
        color = colorchooser.askcolor(
            title="Choose Background Color",
            initialcolor=self.back_color
        )
        if color[1]:
            self.back_color = color[1]
            self.back_preview.configure(bg=self.back_color)
            self.status_var.set(f"Background color changed to {self.back_color}")
    
    def reset_colors(self):
        self.fill_color = "#000000"
        self.back_color = "#FFFFFF"
        self.fill_preview.configure(bg=self.fill_color)
        self.back_preview.configure(bg=self.back_color)
        self.status_var.set("Colors reset to default")
    
    def generate_qr(self):
        data = self.text_input.get("1.0", tk.END).strip()
        
        if not data:
            messagebox.showwarning("⚠️ Warning", "Please enter some text or URL!")
            return
        
        ec_map = {
            "L - 7% (Low)": qrcode.constants.ERROR_CORRECT_L,
            "M - 15% (Medium)": qrcode.constants.ERROR_CORRECT_M,
            "Q - 25% (Quartile)": qrcode.constants.ERROR_CORRECT_Q,
            "H - 30% (High)": qrcode.constants.ERROR_CORRECT_H,
        }
        
        try:
            qr = qrcode.QRCode(
                version=None,
                error_correction=ec_map.get(
                    self.error_correction.get(),
                    qrcode.constants.ERROR_CORRECT_H
                ),
                box_size=int(self.box_size.get()),
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            self.qr_image = qr.make_image(
                fill_color=self.fill_color,
                back_color=self.back_color
            )
            
            self.show_preview()
            
            data_preview = data[:30] + "..." if len(data) > 30 else data
            self.status_var.set(f"✓ QR code generated for: {data_preview}")
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to generate QR code:\n{str(e)}")
            self.status_var.set("Error generating QR code")
    
    def show_preview(self):
        if self.qr_image:
            self.preview_placeholder.pack_forget()
            
            preview_size = 250
            preview = self.qr_image.copy()
            preview.thumbnail((preview_size, preview_size), Image.Resampling.LANCZOS)
            
            photo = ImageTk.PhotoImage(preview)
            
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
    
    def save_qr(self):
        if not self.qr_image:
            messagebox.showwarning("⚠️ Warning", "Generate a QR code first!")
            return
        
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("All Files", "*.*")
            ],
            title="Save QR Code As",
            initialfile="qrcode"
        )
        
        if filepath:
            try:
                if filepath.lower().endswith('.jpg') or filepath.lower().endswith('.jpeg'):
                    rgb_image = self.qr_image.convert('RGB')
                    rgb_image.save(filepath)
                else:
                    self.qr_image.save(filepath)
                
                self.status_var.set(f"✓ Saved to: {os.path.basename(filepath)}")
                messagebox.showinfo("✅ Success", f"QR code saved successfully!\n\n{filepath}")
                
            except Exception as e:
                messagebox.showerror("❌ Error", f"Failed to save QR code:\n{str(e)}")


def main():
    root = tk.Tk()
    
    try:
        root.iconbitmap("qr_icon.ico")
    except:
        pass
    
    app = QRCodeGenerator(root)
    
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()

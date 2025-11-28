# 🔲 QR Code Generator

A simple Python GUI application to generate QR codes from text or URLs.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Features

- 📝 Generate QR codes from any text or URL
- 🎨 Customize QR code and background colors
- 📏 Adjustable QR code size
- 🛡️ Multiple error correction levels (L, M, Q, H)
- 👁️ Live preview before saving
- 💾 Save as PNG or JPG

## 📦 Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/qr-code-generator.git
cd qr-code-generator
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install qrcode[pil] Pillow
```

## 🚀 Usage

Run the application:
```bash
python qr_generator.py
```

### How to use:
1. Enter your text or URL in the input box
2. Adjust settings (size, error correction, colors)
3. Click **"Generate QR Code"**
4. Preview the QR code
5. Click **"Save QR Code"** to save as an image

## 📸 Screenshot

The application provides a user-friendly GUI with:
- Text input area
- Settings panel for customization
- Color pickers for QR and background colors
- Live preview of generated QR code
- Save functionality

## 🛠️ Requirements

- Python 3.8+
- qrcode
- Pillow (PIL)
- tkinter (included with Python)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

Made with ❤️ as a Python Mini Project

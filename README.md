# Image Watermarking Desktop App

A simple desktop application built with **Python Tkinter** for adding text watermarks to images. Users can upload images, customise watermark text, font, size, colour, and position, and then save the watermarked image.

---

## Features

- Upload images in **JPG, JPEG, PNG** formats.
- Add custom watermark text.
- Adjust watermark **font, size, colour, and position**.
- Preview watermark on the image before saving.
- Save the watermarked image in **PNG** or **JPEG** format.
- User-friendly **GUI** using Tkinter.

---

## Screenshots
### app basic window
<img width="1200" height="860" alt="Screenshot from 2025-09-29 14-41-59" src="https://github.com/user-attachments/assets/f91050de-0e65-456c-a4cc-4c18fd01d8e5" />

### menu bar
<img width="1200" height="860" alt="Screenshot from 2025-09-29 14-42-06" src="https://github.com/user-attachments/assets/227a5b4f-d1e0-4c45-b9b8-8e88ebe711f1" />

### Watermarking popup window
<img width="1200" height="860" alt="Screenshot from 2025-09-29 14-46-30" src="https://github.com/user-attachments/assets/e06e88fb-94f1-4ab1-932c-7605b34a7204" />

---

## Installation

1. Clone the repository:

```git clone <repository-url>```<br/>
```cd image_watermarking_desktop_app```<br/>

2. Install required packages:

```pip install pillow matplotlib```<br/>
*Tkinter is included in standard Python installations.

## Usage
Run the app using:

```python main.py```

1. Upload Image: Use the "File → Upload Image" menu to select an image.

2. Add Watermark: Go to "File → Watermarking" and customise the text, font, size, colour, and position.

3. Save Image: Save your watermarked image using "File → Save" or "File → Save as...".

## Watermark Options
**Text**: Enter the watermark text.

**Font**: Select a system font.

**Font Size**: Percentage of the image size.

**Font Colour**: Choose via a color picker.

**Position**: Place watermark at top-left, top, top-right, left, center, right, bottom-left, bottom, or bottom-right.

## Dependencies
- Python 3.8+
- Pillow
- Matplotlib (used optionally for previewing)

## Install dependencies with:

```pip install pillow matplotlib```

### License
This project is licensed under the **MIT License**.

### Author
LegradiK
GitHub: LegradiK

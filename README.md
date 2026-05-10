# Stenography-Tool
🔐 Steganography Tool
A desktop application to hide secret text inside images using LSB (Least Significant Bit) steganography. Built with Python and Tkinter.

<img width="982" height="764" alt="image" src="https://github.com/user-attachments/assets/98a07727-a86b-4a2f-a22c-297a73964faa" />


📸 How It Works
LSB steganography works by replacing the least significant bit of each RGB channel in a pixel with a bit from your secret message. The change in color value is just ±1 — completely invisible to the human eye — while the message is perfectly recoverable.
A 16-bit delimiter is embedded after the message so the decoder knows exactly where the message ends.
Capacity: An image can hold roughly (width × height × 3) / 8 characters. A 1000×1000 image can store ~375,000 characters.

🚀 Getting Started
Prerequisites

Python 3.10 or higher
pip

Installation
bashgit clone https://github.com/your-username/steganography-tool.git
cd steganography-tool
pip install -r requirements.txt
Running the App
bashpython main.py

🖥️ Usage
Encoding a message

Click Open Image and select a PNG, JPG, or BMP file.
Type your secret message in the Secret Message box.
Click Encode.
Choose a location to save the output — it will always be saved as a PNG file (required to preserve the hidden data; lossy formats like JPEG would destroy it).

Decoding a message

Click Open Image and load a stego image (one that has a message hidden in it).
Click Decode.
The hidden message appears in the Decoded Message box.


📁 Project Structure
steganography-tool/
├── main.py              # Entry point — launches the app
├── app.py               # Tkinter GUI
├── steganography.py     # Core LSB encode/decode logic
└── requirements.txt     # Dependencies

📦 Dependencies
PackageVersionPurposePillow10.3.0Image loading, manipulation, and savinghypothesis6.100.0Property-based testing

⚠️ Limitations

ASCII text only — characters outside the ASCII range (emoji, Arabic, Hindi, etc.) are not supported in the current version and may corrupt the encoded message.
PNG output required — the app enforces saving as PNG. Never re-save a stego image as JPEG, as JPEG compression will destroy the hidden data.
No encryption — the message is hidden, not encrypted. Anyone with this tool can decode it. For sensitive data, encrypt your message before encoding.
Delimiter collision — the delimiter pattern corresponds to the two-character sequence ÿþ. If your message naturally contains those characters, decoding may truncate early.


🛠️ Running Tests
bashpip install hypothesis
python -m pytest

📄 License
This project is licensed under the MIT License. See LICENSE for details.

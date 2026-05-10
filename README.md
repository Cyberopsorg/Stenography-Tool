# Stenography-Tool

Steganography Tool

A desktop application to hide secret text inside images using LSB (Least Significant Bit)
steganography. Built with Python and Tkinter.

<img width="982" height="764" alt="image" src="https://github.com/user-attachments/assets/98a07727-a86b-4a2f-a22c-297a73964faa" />

## How It Works
LSB steganography works by replacing the least significant bit of each RGB channel
in a pixel with a bit from your secret message. The change in color value is just
plus/minus 1, which is invisible to the human eye, while the message is recoverable.
A 16-bit delimiter is embedded after the message so the decoder knows where the
message ends.

Capacity: an image can hold roughly (width * height * 3) / 8 bytes. A 1000x1000
image can store about 375,000 bytes.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation
```
git clone https://github.com/your-username/steganography-tool.git
cd steganography-tool
pip install -r steganography_tool/requirements.txt
```

### Running the App
```
python main.py
```

## Usage

### Encoding a message
- Click Open Image and select a PNG, JPG, or BMP file.
- Type your secret message in the Secret Message box.
- Click Encode.
- Choose a location to save the output. It will be saved as a PNG file to preserve
	the hidden data. Lossy formats like JPEG will destroy it.

### Decoding a message
- Click Open Image and load a stego image (one that has a message hidden in it).
- Click Decode.
- The hidden message appears in the Decoded Message box.

## Project Structure
steganography_tool/
├── main.py              # Entry point - launches the app
├── steganography_tool/app.py               # Tkinter GUI
├── steganography_tool/steganography.py     # Core LSB encode/decode logic
└── steganography_tool/requirements.txt     # Dependencies

## Dependencies
Package   Version   Purpose
Pillow    10.3.0    Image loading, manipulation, and saving
hypothesis 6.100.0  Property-based testing

## Limitations
- PNG output required: the app enforces saving as PNG. Never re-save a stego image
	as JPEG, as JPEG compression will destroy the hidden data.
- No encryption: the message is hidden, not encrypted. Anyone with this tool can
	decode it. For sensitive data, encrypt your message before encoding.
- Delimiter collision: the delimiter pattern corresponds to the two-byte sequence
	0xFF 0xFE. If your message bytes naturally contain that sequence, decoding may
	truncate early.

## Running Tests
```
pip install hypothesis
python -m pytest
```

## License
MIT License. Add a LICENSE file if you want to publish it explicitly.

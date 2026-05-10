# Steganography Tool

A desktop application to hide secret text inside images using LSB (Least Significant Bit) steganography. Built with Python and Tkinter.

<img width="982" height="764" alt="App Screenshot" src="https://github.com/user-attachments/assets/98a07727-a86b-4a2f-a22c-297a73964faa" />

## How It Works
LSB steganography hides your message by replacing the least significant bit of each pixel's RGB channels with bits from your message. Changes are visually undetectable but the message can be recovered.  
A 16-bit delimiter is embedded after the message so the decoder knows where the message ends.

- **Capacity**: Roughly `(width × height × 3) ÷ 8` bytes per image. For example, a 1000×1000 image can store about 375,000 bytes.

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip

### Installation
```bash
git clone https://github.com/Cyberopsorg/Stenography-Tool.git
cd Stenography-Tool
pip install -r steganography_tool/requirements.txt
```

### Running the App
```bash
python main.py
```

## Usage

### Encoding a Message
1. Click **Open Image** and select a PNG, JPG, or BMP file.
2. Type your secret message in the Secret Message box.
3. Click **Encode**.
4. Choose a location to save the output (saved as PNG to preserve hidden data).

> **Note:** Do not use lossy formats like JPEG to save output as they will destroy the hidden data.

### Decoding a Message
1. Click **Open Image** and load a stego image (with a hidden message).
2. Click **Decode**.
3. The hidden message will appear in the Decoded Message box.

## Project Structure
```
steganography_tool/
├── main.py                   # Entry point - launches the app
├── steganography_tool/
│   ├── app.py                # Tkinter GUI
│   ├── steganography.py      # Core LSB encode/decode logic
│   └── requirements.txt      # Dependencies
```

## Dependencies

| Package    | Version   | Purpose                                   |
|------------|-----------|-------------------------------------------|
| Pillow     | 10.3.0    | Image loading, manipulation, and saving   |
| hypothesis | 6.100.0   | Property-based testing                    |

## Limitations
- **PNG output required:** The app enforces saving only as PNG. Never re-save a stego image as JPEG—JPEG compression will destroy hidden data.
- **No encryption:** Messages are hidden but not encrypted. Anyone with this tool can decode them. For sensitive data, encrypt your message before encoding.
- **Delimiter collision:** The delimiter pattern (0xFF 0xFE) marks the message end. If your message naturally contains that two-byte sequence, decoding may truncate early.

## Running Tests
```bash
pip install hypothesis
python -m pytest
```

## License
MIT License. Add a LICENSE file if you want to make this explicit.

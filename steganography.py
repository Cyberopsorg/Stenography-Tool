"""steganography.py - Core LSB steganography logic."""
from PIL import Image

# 16-bit end-of-message delimiter (two 0xFF bytes = 1111111111111111 won't appear
# in valid UTF-8, so we use the sequence below as a safe sentinel)
DELIMITER_BITS = "1111111111111110"
DELIMITER_BYTE_LEN = 2  # delimiter occupies 2 bytes (16 bits) of capacity


def max_message_length(image):
    """Return max number of UTF-8 *bytes* encodable in the image."""
    w, h = image.size
    return (w * h * 3) // 8 - DELIMITER_BYTE_LEN


def encode(image, message):
    """
    Embed *message* (any Unicode string) into *image* using LSB steganography.

    - Encodes message as UTF-8 bytes so all Unicode characters work correctly.
    - Raises ValueError if message is empty/whitespace-only or too large.
    - Returns a new PIL Image with the message embedded.
    """
    if not message or not message.strip():
        raise ValueError("Message must not be empty or whitespace-only.")

    # Encode to UTF-8 bytes — handles ASCII, Hindi, emoji, Arabic, etc.
    message_bytes = message.encode("utf-8")

    # Build binary payload: 8 bits per byte + 16-bit delimiter
    binary_payload = "".join(format(b, "08b") for b in message_bytes) + DELIMITER_BITS

    img = image.convert("RGB")
    pixels = list(img.getdata())
    total_channels = len(pixels) * 3

    if len(binary_payload) > total_channels:
        max_bytes = max_message_length(img)
        raise ValueError(
            "Message too large for this image. "
            "Maximum capacity: {} bytes (~{} ASCII characters).".format(
                max_bytes, max_bytes
            )
        )

    payload_index = 0
    new_pixels = []

    for pixel in pixels:
        channels = list(pixel)
        for i in range(3):
            if payload_index < len(binary_payload):
                channels[i] = (channels[i] & ~1) | int(binary_payload[payload_index])
                payload_index += 1
        new_pixels.append(tuple(channels))

    result = Image.new("RGB", img.size)
    result.putdata(new_pixels)
    return result


def decode(image):
    """
    Extract a hidden message from *image*.

    - Reads LSBs, reconstructs UTF-8 bytes, decodes to Unicode string.
    - Returns the decoded message string, or "" if no delimiter is found.
    """
    img = image.convert("RGB")
    pixels = list(img.getdata())

    # Collect all LSBs
    bits = []
    for pixel in pixels:
        for channel in pixel:
            bits.append(channel & 1)

    # Reconstruct bytes 8 bits at a time
    raw_bytes = []
    for i in range(0, len(bits) - 7, 8):
        byte_bits = bits[i:i + 8]
        byte_val = 0
        for b in byte_bits:
            byte_val = (byte_val << 1) | b
        raw_bytes.append(byte_val)

        # Check if last 2 bytes form the delimiter (0xFF 0xFE = 1111111111111110)
        if len(raw_bytes) >= 2:
            last_two_bits = format(raw_bytes[-2], "08b") + format(raw_bytes[-1], "08b")
            if last_two_bits == DELIMITER_BITS:
                # Decode the bytes before the delimiter as UTF-8
                payload = bytes(raw_bytes[:-2])
                try:
                    return payload.decode("utf-8")
                except UnicodeDecodeError:
                    return payload.decode("latin-1")

    return ""

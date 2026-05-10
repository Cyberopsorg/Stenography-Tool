"""main.py - Launch the Steganography Tool"""
import sys
import os

# Resolve the steganography_tool directory relative to this file
_base = os.path.dirname(os.path.abspath(__file__))
_tool_dir = os.path.join(_base, "steganography_tool")

if not os.path.isdir(_tool_dir):
    print(f"Error: Cannot find steganography_tool/ folder at {_tool_dir}")
    sys.exit(1)

sys.path.insert(0, _tool_dir)

from app import App

if __name__ == "__main__":
    app = App()
    app.mainloop()

#!/usr/bin/env python3
"""
Test script to create a sample Quake PAK file for testing the extractor.
"""

import struct
import os


def create_test_pak(output_file="test.pak"):
    """Create a sample Quake PAK file with test files."""
    
    # Test files to include in the PAK
    test_files = [
        ("readme.txt", b"This is a test readme file.\nHello from PAK archive!"),
        ("data/config.cfg", b"# Configuration file\nvolume=80\nquality=high"),
        ("textures/logo.txt", b"ASCII art logo would go here..."),
    ]
    
    # Calculate offsets
    header_size = 12
    current_offset = header_size
    
    # Store file data and metadata
    file_entries = []
    file_data = b""
    
    for filename, content in test_files:
        file_entries.append((filename, current_offset, len(content)))
        file_data += content
        current_offset += len(content)
    
    # Directory offset starts after all file data
    directory_offset = header_size + len(file_data)
    
    # Build directory
    directory = b""
    for filename, offset, size in file_entries:
        # Filename (56 bytes, null-padded)
        filename_bytes = filename.encode('ascii').ljust(56, b'\x00')
        # Offset (4 bytes)
        offset_bytes = struct.pack('<I', offset)
        # Size (4 bytes)
        size_bytes = struct.pack('<I', size)
        
        directory += filename_bytes + offset_bytes + size_bytes
    
    directory_size = len(directory)
    
    # Build header
    header = b'PACK'  # Signature
    header += struct.pack('<I', directory_offset)  # Directory offset
    header += struct.pack('<I', directory_size)     # Directory size
    
    # Write the PAK file
    with open(output_file, 'wb') as f:
        f.write(header)
        f.write(file_data)
        f.write(directory)
    
    print(f"Created test PAK file: {output_file}")
    print(f"  - Files: {len(test_files)}")
    print(f"  - Total size: {os.path.getsize(output_file)} bytes")
    print(f"\nYou can now test the extractor with:")
    print(f"  python3 pak_extractor.py {output_file} --list")
    print(f"  python3 pak_extractor.py {output_file} --extract-all")


if __name__ == "__main__":
    create_test_pak()

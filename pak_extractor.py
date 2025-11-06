#!/usr/bin/env python3
"""
PAK File Extractor
Supports extraction of PAK archive files commonly used in games.
Supports Quake PAK format and other common variants.
"""

import struct
import os
import sys
import argparse
from pathlib import Path
from typing import List, Tuple, BinaryIO


class PAKFileEntry:
    """Represents a file entry in a PAK archive."""
    
    def __init__(self, filename: str, offset: int, size: int):
        self.filename = filename
        self.offset = offset
        self.size = size
    
    def __repr__(self):
        return f"PAKFileEntry(filename={self.filename}, offset={self.offset}, size={self.size})"


class PAKExtractor:
    """Extracts files from PAK archives."""
    
    # Quake PAK format signature
    QUAKE_PAK_SIGNATURE = b'PACK'
    
    def __init__(self, pak_file_path: str):
        self.pak_file_path = pak_file_path
        self.entries: List[PAKFileEntry] = []
        self.format_type = None
        
        if not os.path.exists(pak_file_path):
            raise FileNotFoundError(f"PAK file not found: {pak_file_path}")
    
    def detect_format(self) -> str:
        """Detect the PAK file format."""
        with open(self.pak_file_path, 'rb') as f:
            signature = f.read(4)
            
            if signature == self.QUAKE_PAK_SIGNATURE:
                return "QUAKE"
            else:
                # Try to detect other formats or use generic
                return "GENERIC"
    
    def parse_quake_pak(self) -> List[PAKFileEntry]:
        """Parse Quake PAK format.
        
        Format:
        - Header (12 bytes):
          - Signature: "PACK" (4 bytes)
          - Directory offset (4 bytes, little-endian)
          - Directory size (4 bytes, little-endian)
        - File data
        - Directory entries (64 bytes each):
          - Filename (56 bytes, null-terminated string)
          - File offset (4 bytes, little-endian)
          - File size (4 bytes, little-endian)
        """
        entries = []
        
        with open(self.pak_file_path, 'rb') as f:
            # Read header
            signature = f.read(4)
            if signature != self.QUAKE_PAK_SIGNATURE:
                raise ValueError("Invalid Quake PAK file signature")
            
            dir_offset = struct.unpack('<I', f.read(4))[0]
            dir_size = struct.unpack('<I', f.read(4))[0]
            
            # Calculate number of entries
            entry_size = 64  # 56 bytes filename + 4 bytes offset + 4 bytes size
            num_entries = dir_size // entry_size
            
            # Read directory
            f.seek(dir_offset)
            for _ in range(num_entries):
                # Read filename (56 bytes)
                filename_bytes = f.read(56)
                filename = filename_bytes.split(b'\x00')[0].decode('ascii', errors='ignore')
                
                # Read offset and size
                file_offset = struct.unpack('<I', f.read(4))[0]
                file_size = struct.unpack('<I', f.read(4))[0]
                
                if filename:  # Skip empty entries
                    entries.append(PAKFileEntry(filename, file_offset, file_size))
        
        return entries
    
    def parse_generic_pak(self) -> List[PAKFileEntry]:
        """Parse generic PAK format (simple header + files).
        
        This is a fallback for simple PAK formats that might have:
        - A simple header with file count
        - File entries with name, offset, and size
        """
        entries = []
        
        try:
            with open(self.pak_file_path, 'rb') as f:
                # Try to read a simple header
                # Many PAK formats have: magic (4 bytes), version (4 bytes), file count (4 bytes)
                magic = f.read(4)
                version = struct.unpack('<I', f.read(4))[0]
                file_count = struct.unpack('<I', f.read(4))[0]
                
                # Sanity check
                if file_count > 100000 or file_count <= 0:
                    raise ValueError("Invalid file count")
                
                # Read file entries
                for _ in range(file_count):
                    # Read filename length and filename
                    name_len = struct.unpack('<I', f.read(4))[0]
                    if name_len > 512 or name_len <= 0:  # Sanity check
                        continue
                    
                    filename = f.read(name_len).decode('utf-8', errors='ignore')
                    file_offset = struct.unpack('<I', f.read(4))[0]
                    file_size = struct.unpack('<I', f.read(4))[0]
                    
                    entries.append(PAKFileEntry(filename, file_offset, file_size))
        
        except Exception as e:
            # If generic parsing fails, return empty list
            print(f"Warning: Could not parse as generic PAK format: {e}")
        
        return entries
    
    def parse(self) -> List[PAKFileEntry]:
        """Parse the PAK file and return list of entries."""
        self.format_type = self.detect_format()
        
        if self.format_type == "QUAKE":
            self.entries = self.parse_quake_pak()
        elif self.format_type == "GENERIC":
            self.entries = self.parse_generic_pak()
        else:
            raise ValueError(f"Unsupported PAK format: {self.format_type}")
        
        return self.entries
    
    def list_files(self) -> None:
        """List all files in the PAK archive."""
        if not self.entries:
            self.parse()
        
        if not self.entries:
            print("No files found in PAK archive")
            return
        
        print(f"\nPAK Archive: {self.pak_file_path}")
        print(f"Format: {self.format_type}")
        print(f"Total files: {len(self.entries)}\n")
        print(f"{'Filename':<50} {'Size':>12} {'Offset':>12}")
        print("-" * 76)
        
        for entry in self.entries:
            size_kb = entry.size / 1024
            if size_kb < 1024:
                size_str = f"{size_kb:.2f} KB"
            else:
                size_str = f"{size_kb/1024:.2f} MB"
            
            print(f"{entry.filename:<50} {size_str:>12} {entry.offset:>12}")
    
    def extract_file(self, entry: PAKFileEntry, output_dir: str) -> None:
        """Extract a single file from the PAK archive."""
        output_path = os.path.join(output_dir, entry.filename)
        
        # Create directory structure if needed
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(self.pak_file_path, 'rb') as pak_file:
            pak_file.seek(entry.offset)
            data = pak_file.read(entry.size)
            
            with open(output_path, 'wb') as out_file:
                out_file.write(data)
    
    def extract_all(self, output_dir: str = "extracted") -> None:
        """Extract all files from the PAK archive."""
        if not self.entries:
            self.parse()
        
        if not self.entries:
            print("No files to extract")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nExtracting {len(self.entries)} files to: {output_dir}")
        
        for i, entry in enumerate(self.entries, 1):
            try:
                self.extract_file(entry, output_dir)
                print(f"[{i}/{len(self.entries)}] Extracted: {entry.filename}")
            except Exception as e:
                print(f"[{i}/{len(self.entries)}] Error extracting {entry.filename}: {e}")
        
        print(f"\nExtraction complete! Files extracted to: {output_dir}")
    
    def extract_specific(self, filename: str, output_dir: str = ".") -> None:
        """Extract a specific file by name."""
        if not self.entries:
            self.parse()
        
        for entry in self.entries:
            if entry.filename == filename or entry.filename.endswith(filename):
                try:
                    self.extract_file(entry, output_dir)
                    print(f"Extracted: {entry.filename} -> {output_dir}")
                    return
                except Exception as e:
                    print(f"Error extracting {entry.filename}: {e}")
                    return
        
        print(f"File not found in archive: {filename}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="PAK File Extractor - Extract files from PAK archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all files in a PAK archive
  python pak_extractor.py myfile.pak --list

  # Extract all files
  python pak_extractor.py myfile.pak --extract-all

  # Extract all files to a specific directory
  python pak_extractor.py myfile.pak --extract-all --output ./my_extracted_files

  # Extract a specific file
  python pak_extractor.py myfile.pak --extract textures/image.png

  # Get info about the PAK file
  python pak_extractor.py myfile.pak --info
        """
    )
    
    parser.add_argument('pak_file', help="Path to the PAK file")
    parser.add_argument('-l', '--list', action='store_true', 
                       help="List all files in the archive")
    parser.add_argument('-a', '--extract-all', action='store_true',
                       help="Extract all files from the archive")
    parser.add_argument('-e', '--extract', metavar='FILENAME',
                       help="Extract a specific file")
    parser.add_argument('-o', '--output', default='extracted',
                       help="Output directory for extracted files (default: extracted)")
    parser.add_argument('-i', '--info', action='store_true',
                       help="Show information about the PAK file")
    
    args = parser.parse_args()
    
    try:
        extractor = PAKExtractor(args.pak_file)
        
        # If no action specified, default to listing
        if not (args.list or args.extract_all or args.extract or args.info):
            args.list = True
        
        if args.info or args.list:
            extractor.list_files()
        
        if args.extract_all:
            extractor.extract_all(args.output)
        
        if args.extract:
            extractor.extract_specific(args.extract, args.output)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

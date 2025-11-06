#!/usr/bin/env python3
"""
Unreal Engine PAK File Extractor
Extracts game assets from Unreal Engine PAK archives without requiring encryption keys.
Supports PAK versions 1-11 with compression support.
"""

import struct
import os
import sys
import zlib
import argparse
from pathlib import Path
from typing import List, Dict, BinaryIO, Optional
from dataclasses import dataclass
import hashlib


@dataclass
class UnrealPakEntry:
    """Represents a file entry in an Unreal Engine PAK archive."""
    filename: str
    offset: int
    compressed_size: int
    uncompressed_size: int
    compression_method: int
    timestamp: int
    hash: bytes
    compression_blocks: List[tuple] = None
    encrypted: bool = False
    compression_block_size: int = 0
    
    def __repr__(self):
        return (f"UnrealPakEntry(filename={self.filename}, "
                f"offset={self.offset}, "
                f"uncompressed_size={self.uncompressed_size}, "
                f"compressed={self.is_compressed()})")
    
    def is_compressed(self) -> bool:
        """Check if the entry is compressed."""
        return self.compression_method != 0 and self.compressed_size != self.uncompressed_size


class UnrealPakExtractor:
    """Extracts files from Unreal Engine PAK archives."""
    
    # Unreal PAK magic number (stored at end of file)
    PAK_MAGIC = 0x5A6F12E1
    
    # Compression methods
    COMPRESS_None = 0x00
    COMPRESS_ZLIB = 0x01
    COMPRESS_GZIP = 0x02
    COMPRESS_Custom = 0x04
    
    # Encryption flag
    ENCRYPTED_FLAG = 0x01
    
    def __init__(self, pak_file_path: str):
        """Initialize the PAK extractor.
        
        Args:
            pak_file_path: Path to the PAK file
        """
        self.pak_file_path = pak_file_path
        self.entries: Dict[str, UnrealPakEntry] = {}
        self.pak_version = 0
        self.index_offset = 0
        self.index_size = 0
        self.mount_point = ""
        self.encrypted = False
        
        if not os.path.exists(pak_file_path):
            raise FileNotFoundError(f"PAK file not found: {pak_file_path}")
    
    def read_string(self, f: BinaryIO) -> str:
        """Read a length-prefixed string from the file.
        
        Args:
            f: File handle
            
        Returns:
            Decoded string
        """
        length = struct.unpack('<i', f.read(4))[0]
        
        if length == 0:
            return ""
        
        # Handle negative length (UTF-16)
        if length < 0:
            length = -length
            raw_string = f.read(length * 2)
            # Remove null terminator
            return raw_string.decode('utf-16-le', errors='ignore').rstrip('\x00')
        else:
            raw_string = f.read(length)
            # Remove null terminator
            return raw_string.decode('ascii', errors='ignore').rstrip('\x00')
    
    def parse_footer(self) -> bool:
        """Parse the PAK file footer to get index information.
        
        Returns:
            True if footer was parsed successfully, False otherwise
        """
        with open(self.pak_file_path, 'rb') as f:
            # Get file size
            f.seek(0, 2)
            file_size = f.tell()
            
            if file_size < 44:  # Minimum size for footer
                print("File too small to be a valid PAK file")
                return False
            
            # Read footer (last 44 bytes for most versions)
            f.seek(-44, 2)
            footer_data = f.read(44)
            
            # Try to parse as PAK version 7+ footer
            try:
                encryption_guid = footer_data[0:16]
                encrypted_index = struct.unpack('<B', footer_data[16:17])[0]
                magic = struct.unpack('<I', footer_data[17:21])[0]
                
                if magic != self.PAK_MAGIC:
                    # Try older format (without encryption info)
                    f.seek(-28, 2)
                    footer_data = f.read(28)
                    magic = struct.unpack('<I', footer_data[0:4])[0]
                    
                    if magic != self.PAK_MAGIC:
                        print(f"Invalid PAK magic: {hex(magic)}, expected {hex(self.PAK_MAGIC)}")
                        return False
                    
                    self.pak_version = struct.unpack('<I', footer_data[4:8])[0]
                    self.index_offset = struct.unpack('<Q', footer_data[8:16])[0]
                    self.index_size = struct.unpack('<Q', footer_data[16:24])[0]
                    self.encrypted = False
                else:
                    self.pak_version = struct.unpack('<I', footer_data[21:25])[0]
                    self.index_offset = struct.unpack('<Q', footer_data[25:33])[0]
                    self.index_size = struct.unpack('<Q', footer_data[33:41])[0]
                    self.encrypted = encrypted_index != 0
                
                # Validate values
                if self.index_offset >= file_size or self.index_size == 0:
                    print(f"Invalid index offset or size: offset={self.index_offset}, size={self.index_size}")
                    return False
                
                return True
                
            except Exception as e:
                print(f"Error parsing footer: {e}")
                return False
    
    def parse_index(self) -> bool:
        """Parse the PAK file index to extract file entries.
        
        Returns:
            True if index was parsed successfully, False otherwise
        """
        if self.encrypted:
            print("ERROR: This PAK file is encrypted!")
            print("Encrypted PAK files require an AES encryption key to extract.")
            print("This extractor only supports unencrypted PAK files.")
            return False
        
        try:
            with open(self.pak_file_path, 'rb') as f:
                f.seek(self.index_offset)
                
                # Read mount point
                self.mount_point = self.read_string(f)
                
                # Read number of entries
                entry_count = struct.unpack('<I', f.read(4))[0]
                
                if entry_count > 1000000:  # Sanity check
                    print(f"Suspicious entry count: {entry_count}")
                    return False
                
                # Read each entry
                for _ in range(entry_count):
                    try:
                        # Read filename
                        filename = self.read_string(f)
                        
                        if not filename:
                            continue
                        
                        # Remove mount point prefix if present
                        if self.mount_point and filename.startswith(self.mount_point):
                            filename = filename[len(self.mount_point):]
                        
                        # Normalize path separators
                        filename = filename.replace('\\', '/')
                        filename = filename.lstrip('/')
                        
                        # Read entry data based on version
                        offset = struct.unpack('<Q', f.read(8))[0]
                        compressed_size = struct.unpack('<Q', f.read(8))[0]
                        uncompressed_size = struct.unpack('<Q', f.read(8))[0]
                        compression_method = struct.unpack('<I', f.read(4))[0]
                        
                        # Read timestamp if version >= 8
                        if self.pak_version >= 8:
                            timestamp = struct.unpack('<Q', f.read(8))[0]
                        else:
                            timestamp = 0
                        
                        # Read SHA1 hash (20 bytes)
                        file_hash = f.read(20)
                        
                        # Read compression blocks if compressed
                        compression_blocks = []
                        if compression_method != self.COMPRESS_None:
                            block_count = struct.unpack('<I', f.read(4))[0]
                            for _ in range(block_count):
                                block_start = struct.unpack('<Q', f.read(8))[0]
                                block_end = struct.unpack('<Q', f.read(8))[0]
                                compression_blocks.append((block_start, block_end))
                        
                        # Check if encrypted
                        encrypted = (compression_method & self.ENCRYPTED_FLAG) != 0
                        
                        # Create entry
                        entry = UnrealPakEntry(
                            filename=filename,
                            offset=offset,
                            compressed_size=compressed_size,
                            uncompressed_size=uncompressed_size,
                            compression_method=compression_method,
                            timestamp=timestamp,
                            hash=file_hash,
                            compression_blocks=compression_blocks,
                            encrypted=encrypted
                        )
                        
                        self.entries[filename] = entry
                        
                    except Exception as e:
                        print(f"Error reading entry: {e}")
                        continue
                
                return True
                
        except Exception as e:
            print(f"Error parsing index: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def decompress_data(self, data: bytes, method: int) -> bytes:
        """Decompress data using the specified method.
        
        Args:
            data: Compressed data
            method: Compression method
            
        Returns:
            Decompressed data
        """
        if method == self.COMPRESS_ZLIB:
            return zlib.decompress(data)
        elif method == self.COMPRESS_GZIP:
            return zlib.decompress(data, zlib.MAX_WBITS | 16)
        else:
            # Unknown compression method, return as-is
            return data
    
    def extract_file_data(self, entry: UnrealPakEntry) -> Optional[bytes]:
        """Extract and decompress file data.
        
        Args:
            entry: PAK entry to extract
            
        Returns:
            Decompressed file data, or None if extraction failed
        """
        if entry.encrypted:
            print(f"Cannot extract encrypted file: {entry.filename}")
            return None
        
        try:
            with open(self.pak_file_path, 'rb') as f:
                f.seek(entry.offset)
                
                if entry.is_compressed():
                    # Handle compressed data
                    if entry.compression_blocks:
                        # Extract using compression blocks
                        output_data = bytearray()
                        
                        for block_start, block_end in entry.compression_blocks:
                            f.seek(entry.offset + block_start)
                            compressed_block = f.read(block_end - block_start)
                            
                            try:
                                decompressed_block = self.decompress_data(
                                    compressed_block, 
                                    entry.compression_method
                                )
                                output_data.extend(decompressed_block)
                            except Exception as e:
                                print(f"Warning: Error decompressing block: {e}")
                                output_data.extend(compressed_block)
                        
                        return bytes(output_data)
                    else:
                        # No compression blocks, decompress entire file
                        compressed_data = f.read(entry.compressed_size)
                        return self.decompress_data(compressed_data, entry.compression_method)
                else:
                    # Uncompressed data
                    return f.read(entry.uncompressed_size)
                    
        except Exception as e:
            print(f"Error extracting {entry.filename}: {e}")
            return None
    
    def list_files(self) -> None:
        """List all files in the PAK archive."""
        if not self.entries:
            print("No files found in PAK archive (did you parse it first?)")
            return
        
        print(f"\n{'='*80}")
        print(f"Unreal Engine PAK Archive: {self.pak_file_path}")
        print(f"{'='*80}")
        print(f"PAK Version: {self.pak_version}")
        print(f"Mount Point: {self.mount_point}")
        print(f"Total Files: {len(self.entries)}")
        print(f"Encrypted: {'Yes' if self.encrypted else 'No'}")
        print(f"{'='*80}\n")
        
        print(f"{'Filename':<60} {'Size':>12} {'Compressed':>12}")
        print("-" * 86)
        
        for filename, entry in sorted(self.entries.items()):
            size = entry.uncompressed_size
            if size < 1024:
                size_str = f"{size} B"
            elif size < 1024 * 1024:
                size_str = f"{size / 1024:.2f} KB"
            else:
                size_str = f"{size / (1024*1024):.2f} MB"
            
            compressed_str = "Yes" if entry.is_compressed() else "No"
            
            print(f"{filename:<60} {size_str:>12} {compressed_str:>12}")
        
        # Calculate total size
        total_size = sum(entry.uncompressed_size for entry in self.entries.values())
        total_compressed = sum(entry.compressed_size for entry in self.entries.values())
        
        print("-" * 86)
        if total_compressed < total_size:
            ratio = (1 - total_compressed / total_size) * 100 if total_size > 0 else 0
            print(f"Total Size: {total_size / (1024*1024):.2f} MB "
                  f"(Compressed: {total_compressed / (1024*1024):.2f} MB, "
                  f"Ratio: {ratio:.1f}%)")
        else:
            print(f"Total Size: {total_size / (1024*1024):.2f} MB")
    
    def extract_file(self, filename: str, output_dir: str) -> bool:
        """Extract a single file from the PAK archive.
        
        Args:
            filename: Name of file to extract
            output_dir: Output directory
            
        Returns:
            True if extraction succeeded, False otherwise
        """
        if filename not in self.entries:
            print(f"File not found in archive: {filename}")
            return False
        
        entry = self.entries[filename]
        output_path = os.path.join(output_dir, filename)
        
        # Create directory structure
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Extract file data
        data = self.extract_file_data(entry)
        
        if data is None:
            return False
        
        # Write to file
        try:
            with open(output_path, 'wb') as f:
                f.write(data)
            return True
        except Exception as e:
            print(f"Error writing file {output_path}: {e}")
            return False
    
    def extract_all(self, output_dir: str = "extracted") -> None:
        """Extract all files from the PAK archive.
        
        Args:
            output_dir: Output directory for extracted files
        """
        if not self.entries:
            print("No files to extract")
            return
        
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"\nExtracting {len(self.entries)} files to: {output_dir}\n")
        
        success_count = 0
        fail_count = 0
        
        for i, (filename, entry) in enumerate(sorted(self.entries.items()), 1):
            try:
                status = "OK" if self.extract_file(filename, output_dir) else "FAILED"
                
                if status == "OK":
                    success_count += 1
                else:
                    fail_count += 1
                
                # Show progress
                print(f"[{i}/{len(self.entries)}] {status:8} {filename}")
                
            except Exception as e:
                fail_count += 1
                print(f"[{i}/{len(self.entries)}] ERROR   {filename}: {e}")
        
        print(f"\n{'='*80}")
        print(f"Extraction Complete!")
        print(f"  Success: {success_count}")
        print(f"  Failed:  {fail_count}")
        print(f"  Output:  {output_dir}")
        print(f"{'='*80}\n")
    
    def parse(self) -> bool:
        """Parse the PAK file and extract index.
        
        Returns:
            True if parsing succeeded, False otherwise
        """
        print(f"Parsing PAK file: {self.pak_file_path}")
        
        if not self.parse_footer():
            print("Failed to parse PAK footer")
            return False
        
        print(f"PAK Version: {self.pak_version}")
        print(f"Index Offset: {self.index_offset}")
        print(f"Index Size: {self.index_size}")
        print(f"Encrypted: {self.encrypted}")
        
        if not self.parse_index():
            print("Failed to parse PAK index")
            return False
        
        print(f"Successfully parsed {len(self.entries)} files")
        return True


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Unreal Engine PAK File Extractor - Extract game assets from PAK archives",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all files in a PAK archive
  python unreal_pak_extractor.py game.pak --list

  # Extract all files
  python unreal_pak_extractor.py game.pak --extract-all

  # Extract all files to a specific directory
  python unreal_pak_extractor.py game.pak --extract-all --output ./assets

  # Extract a specific file
  python unreal_pak_extractor.py game.pak --extract Content/Textures/player.png

  # Get info about the PAK file
  python unreal_pak_extractor.py game.pak --info

Note: This extractor only supports UNENCRYPTED PAK files.
Encrypted PAK files require AES encryption keys which are not supported.
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
        extractor = UnrealPakExtractor(args.pak_file)
        
        # Parse the PAK file
        if not extractor.parse():
            print("\nFailed to parse PAK file!")
            sys.exit(1)
        
        # If no action specified, default to listing
        if not (args.list or args.extract_all or args.extract or args.info):
            args.list = True
        
        if args.info or args.list:
            extractor.list_files()
        
        if args.extract_all:
            extractor.extract_all(args.output)
        
        if args.extract:
            if extractor.extract_file(args.extract, args.output):
                print(f"\nSuccessfully extracted: {args.extract}")
            else:
                print(f"\nFailed to extract: {args.extract}")
                sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nExtraction cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

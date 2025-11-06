#!/usr/bin/env python3
"""
Unreal Engine PAK Manager
Interactive tool for unpacking, editing, and repacking PAK files
"""

import os
import sys
import shutil
import struct
import zlib
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import hashlib

# Import our extractor
from unreal_pak_extractor import UnrealPakExtractor, UnrealPakEntry


class PAKManager:
    """Manages PAK file unpacking, editing, and repacking."""
    
    def __init__(self):
        """Initialize PAK Manager with folder structure."""
        self.base_dir = os.getcwd()
        self.folders = {
            'original': 'Original pak file',
            'extracted': 'extracted data-blocks',
            'edited': 'edited game assets here',
            'repacked': 'repacked pak file with edited data'
        }
        
        self.original_pak = None
        self.extractor = None
        
    def setup_folders(self):
        """Create the required folder structure."""
        print("\n" + "="*60)
        print("I have create new folders")
        print("="*60 + "\n")
        
        for key, folder_name in self.folders.items():
            folder_path = os.path.join(self.base_dir, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
                print(f"✓ Created: {folder_name}/")
            else:
                print(f"✓ Exists:  {folder_name}/")
        
        print("\n" + "="*60)
        print("Folder structure ready!")
        print("="*60 + "\n")
    
    def detect_pak_file(self) -> Optional[str]:
        """Detect PAK file in the 'Original pak file' folder."""
        original_folder = os.path.join(self.base_dir, self.folders['original'])
        
        # Find all .pak files
        pak_files = [f for f in os.listdir(original_folder) 
                     if f.lower().endswith('.pak') and os.path.isfile(os.path.join(original_folder, f))]
        
        if not pak_files:
            return None
        
        if len(pak_files) == 1:
            return os.path.join(original_folder, pak_files[0])
        
        # Multiple PAK files found - let user choose
        print("\nMultiple PAK files found:")
        for i, pak in enumerate(pak_files, 1):
            size = os.path.getsize(os.path.join(original_folder, pak))
            size_mb = size / (1024 * 1024)
            print(f"  {i}. {pak} ({size_mb:.2f} MB)")
        
        while True:
            try:
                choice = input(f"\nSelect PAK file (1-{len(pak_files)}): ").strip()
                idx = int(choice) - 1
                if 0 <= idx < len(pak_files):
                    return os.path.join(original_folder, pak_files[idx])
            except (ValueError, IndexError):
                print("Invalid choice. Please try again.")
    
    def unpack_pak(self):
        """Unpack the PAK file from 'Original pak file' folder."""
        print("\n" + "="*60)
        print("UNPACKING PAK FILE")
        print("="*60 + "\n")
        
        # Detect PAK file
        pak_path = self.detect_pak_file()
        
        if not pak_path:
            print("❌ ERROR: No PAK file found in 'Original pak file' folder!")
            print(f"\nPlease place your .pak file in: {self.folders['original']}/")
            input("\nPress Enter to continue...")
            return
        
        print(f"📦 Found PAK file: {os.path.basename(pak_path)}")
        self.original_pak = pak_path
        
        # Initialize extractor
        try:
            self.extractor = UnrealPakExtractor(pak_path)
            
            print("\n⏳ Parsing PAK file...")
            if not self.extractor.parse():
                print("\n❌ Failed to parse PAK file!")
                print("The file might be encrypted or corrupted.")
                input("\nPress Enter to continue...")
                return
            
            if self.extractor.encrypted:
                print("\n❌ ERROR: This PAK file is ENCRYPTED!")
                print("Encrypted PAK files cannot be unpacked without the encryption key.")
                input("\nPress Enter to continue...")
                return
            
            # Show info
            print(f"\n✓ PAK Version: {self.extractor.pak_version}")
            print(f"✓ Mount Point: {self.extractor.mount_point}")
            print(f"✓ Total Files: {len(self.extractor.entries)}")
            
            # Extract to 'extracted data-blocks' folder
            extract_dir = os.path.join(self.base_dir, self.folders['extracted'])
            
            # Clear existing extracted files
            if os.path.exists(extract_dir) and os.listdir(extract_dir):
                response = input("\n⚠️  Extracted folder is not empty. Clear it? (y/n): ").strip().lower()
                if response == 'y':
                    shutil.rmtree(extract_dir)
                    os.makedirs(extract_dir)
            
            print(f"\n⏳ Extracting {len(self.extractor.entries)} files...")
            print("-" * 60)
            
            self.extractor.extract_all(extract_dir)
            
            print("\n" + "="*60)
            print("✓ UNPACKING COMPLETE!")
            print("="*60)
            print(f"\nFiles extracted to: {self.folders['extracted']}/")
            
        except Exception as e:
            print(f"\n❌ ERROR during unpacking: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to continue...")
    
    def repack_pak(self):
        """Repack PAK file with edited assets."""
        print("\n" + "="*60)
        print("REPACKING PAK FILE")
        print("="*60 + "\n")
        
        if not self.original_pak or not self.extractor:
            print("❌ ERROR: Please unpack a PAK file first!")
            input("\nPress Enter to continue...")
            return
        
        extracted_dir = os.path.join(self.base_dir, self.folders['extracted'])
        edited_dir = os.path.join(self.base_dir, self.folders['edited'])
        output_dir = os.path.join(self.base_dir, self.folders['repacked'])
        
        if not os.path.exists(extracted_dir) or not os.listdir(extracted_dir):
            print("❌ ERROR: No extracted files found!")
            print("Please unpack a PAK file first.")
            input("\nPress Enter to continue...")
            return
        
        print("⏳ Scanning for edited files...")
        
        # Find edited files
        edited_files = []
        if os.path.exists(edited_dir):
            for root, dirs, files in os.walk(edited_dir):
                for file in files:
                    edited_path = os.path.join(root, file)
                    rel_path = os.path.relpath(edited_path, edited_dir)
                    edited_files.append(rel_path)
        
        if edited_files:
            print(f"\n✓ Found {len(edited_files)} edited file(s):")
            for ef in edited_files[:10]:  # Show first 10
                print(f"  • {ef}")
            if len(edited_files) > 10:
                print(f"  ... and {len(edited_files) - 10} more")
        else:
            print("\n⚠️  No edited files found in 'edited game assets here' folder.")
            print("Repacking with original files only.")
        
        # Replace edited files in extracted directory
        for edited_file in edited_files:
            src = os.path.join(edited_dir, edited_file)
            dst = os.path.join(extracted_dir, edited_file)
            
            if os.path.exists(dst):
                print(f"\n🔄 Replacing: {edited_file}")
                shutil.copy2(src, dst)
            else:
                # New file - add it
                print(f"\n➕ Adding new file: {edited_file}")
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
        
        # Generate output PAK filename
        original_name = os.path.basename(self.original_pak)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_pak = os.path.join(output_dir, f"repacked_{original_name}")
        
        print(f"\n⏳ Creating PAK file: {os.path.basename(output_pak)}")
        
        try:
            # Repack the PAK
            self._create_pak_file(extracted_dir, output_pak)
            
            print("\n" + "="*60)
            print("✓ REPACKING COMPLETE!")
            print("="*60)
            print(f"\nRepacked PAK saved to: {self.folders['repacked']}/")
            print(f"Filename: {os.path.basename(output_pak)}")
            
            # Show file size
            size = os.path.getsize(output_pak)
            size_mb = size / (1024 * 1024)
            print(f"Size: {size_mb:.2f} MB")
            
        except Exception as e:
            print(f"\n❌ ERROR during repacking: {e}")
            import traceback
            traceback.print_exc()
        
        input("\nPress Enter to continue...")
    
    def _create_pak_file(self, source_dir: str, output_pak: str):
        """Create a PAK file from directory contents.
        
        Args:
            source_dir: Directory containing files to pack
            output_pak: Output PAK file path
        """
        print("\n📦 Building file list...")
        
        # Collect all files
        files_to_pack = []
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_dir)
                # Normalize path separators for Unreal
                rel_path = rel_path.replace(os.sep, '/')
                files_to_pack.append((rel_path, full_path))
        
        print(f"✓ Found {len(files_to_pack)} files to pack")
        
        # Create PAK file
        os.makedirs(os.path.dirname(output_pak), exist_ok=True)
        
        with open(output_pak, 'wb') as pak:
            # Write placeholder header
            pak.write(b'\x00' * 1024)  # Reserve space
            
            current_offset = 1024
            file_entries = []
            
            print("\n⏳ Writing files to PAK...")
            
            # Write all file data
            for i, (rel_path, full_path) in enumerate(files_to_pack, 1):
                if i % 100 == 0 or i == len(files_to_pack):
                    print(f"  Progress: {i}/{len(files_to_pack)} files", end='\r')
                
                with open(full_path, 'rb') as f:
                    file_data = f.read()
                
                file_size = len(file_data)
                
                # Write file data
                pak.write(file_data)
                
                # Store entry info
                file_entries.append({
                    'filename': rel_path,
                    'offset': current_offset,
                    'size': file_size,
                    'compressed_size': file_size,
                    'compression': 0,  # No compression
                    'timestamp': int(os.path.getmtime(full_path)),
                    'hash': hashlib.sha1(file_data).digest()
                })
                
                current_offset += file_size
            
            print(f"\n✓ All files written")
            
            # Write index
            print("\n⏳ Writing PAK index...")
            index_offset = current_offset
            
            # Mount point (use original or default)
            mount_point = self.extractor.mount_point if self.extractor else "../../../"
            self._write_string(pak, mount_point)
            
            # Number of entries
            pak.write(struct.pack('<I', len(file_entries)))
            
            # Write each entry
            for entry in file_entries:
                # Filename
                self._write_string(pak, entry['filename'])
                
                # Offset, sizes, compression
                pak.write(struct.pack('<Q', entry['offset']))
                pak.write(struct.pack('<Q', entry['compressed_size']))
                pak.write(struct.pack('<Q', entry['size']))
                pak.write(struct.pack('<I', entry['compression']))
                
                # Timestamp (version 8+)
                pak.write(struct.pack('<Q', entry['timestamp']))
                
                # SHA1 hash
                pak.write(entry['hash'])
                
                # No compression blocks
                pak.write(struct.pack('<I', 0))
            
            index_size = current_offset - index_offset + pak.tell() - current_offset
            
            # Write footer
            print("⏳ Writing PAK footer...")
            
            # Encryption GUID (all zeros = not encrypted)
            pak.write(b'\x00' * 16)
            
            # Encrypted index flag (0 = not encrypted)
            pak.write(struct.pack('<B', 0))
            
            # Magic number
            pak.write(struct.pack('<I', 0x5A6F12E1))
            
            # Version (use original or default to 8)
            version = self.extractor.pak_version if self.extractor else 8
            pak.write(struct.pack('<I', version))
            
            # Index offset and size
            pak.write(struct.pack('<Q', index_offset))
            pak.write(struct.pack('<Q', index_size))
            
            print("✓ PAK footer written")
    
    def _write_string(self, f, s: str):
        """Write a length-prefixed string to file."""
        if not s:
            f.write(struct.pack('<i', 0))
            return
        
        # Write as ASCII with null terminator
        encoded = s.encode('utf-8') + b'\x00'
        f.write(struct.pack('<i', len(encoded)))
        f.write(encoded)
    
    def clear_output(self):
        """Clear extracted and repacked folders."""
        print("\n" + "="*60)
        print("CLEAR OUTPUT")
        print("="*60 + "\n")
        
        folders_to_clear = [
            self.folders['extracted'],
            self.folders['repacked']
        ]
        
        print("This will delete:")
        for folder in folders_to_clear:
            print(f"  • {folder}/")
        
        response = input("\nAre you sure? (y/n): ").strip().lower()
        
        if response == 'y':
            for folder in folders_to_clear:
                folder_path = os.path.join(self.base_dir, folder)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
                    os.makedirs(folder_path)
                    print(f"✓ Cleared: {folder}/")
            
            # Also clear edited folder
            edited_folder = os.path.join(self.base_dir, self.folders['edited'])
            if os.path.exists(edited_folder) and os.listdir(edited_folder):
                response = input("\nAlso clear 'edited game assets here' folder? (y/n): ").strip().lower()
                if response == 'y':
                    shutil.rmtree(edited_folder)
                    os.makedirs(edited_folder)
                    print(f"✓ Cleared: {self.folders['edited']}/")
            
            # Reset state
            self.original_pak = None
            self.extractor = None
            
            print("\n✓ All output folders cleared!")
        else:
            print("\n✗ Operation cancelled")
        
        input("\nPress Enter to continue...")
    
    def show_paths(self):
        """Show all folder paths."""
        print("\n" + "="*60)
        print("FOLDER PATHS")
        print("="*60 + "\n")
        
        for key, folder in self.folders.items():
            folder_path = os.path.join(self.base_dir, folder)
            exists = "✓" if os.path.exists(folder_path) else "✗"
            print(f"{exists} {folder}/")
            print(f"   Path: {folder_path}")
            
            if os.path.exists(folder_path):
                # Count files
                file_count = sum(1 for _, _, files in os.walk(folder_path) for _ in files)
                print(f"   Files: {file_count}")
            print()
        
        # Show detected PAK
        if self.original_pak:
            print("Current PAK File:")
            print(f"  {os.path.basename(self.original_pak)}")
            print(f"  Path: {self.original_pak}")
            size = os.path.getsize(self.original_pak)
            print(f"  Size: {size / (1024*1024):.2f} MB")
        else:
            print("No PAK file loaded")
        
        input("\nPress Enter to continue...")
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("UNREAL ENGINE PAK MANAGER")
        print("="*60)
        print("\nMain Menu\n")
        print("  1. Unpack OBB (.pak file)")
        print("  2. Clear Output")
        print("  3. Repack OBB")
        print("  4. Show Paths")
        print("  5. Exit")
        print("\n" + "="*60)
    
    def run(self):
        """Run the interactive PAK manager."""
        # Setup folders first
        self.setup_folders()
        
        while True:
            self.show_menu()
            
            choice = input("\nEnter your choice [1/2/3/4/5] (1): ").strip()
            
            if not choice:
                choice = '1'
            
            if choice == '1':
                self.unpack_pak()
            elif choice == '2':
                self.clear_output()
            elif choice == '3':
                self.repack_pak()
            elif choice == '4':
                self.show_paths()
            elif choice == '5':
                print("\n" + "="*60)
                print("Thank you for using Unreal Engine PAK Manager!")
                print("="*60 + "\n")
                sys.exit(0)
            else:
                print("\n❌ Invalid choice. Please select 1-5.")
                input("\nPress Enter to continue...")


def main():
    """Main entry point."""
    try:
        manager = PAKManager()
        manager.run()
    except KeyboardInterrupt:
        print("\n\n✗ Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

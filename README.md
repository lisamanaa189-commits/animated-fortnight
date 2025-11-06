# PAK File Extractors

A comprehensive collection of Python-based tools to extract and manage PAK archive files commonly used in video games. Supports multiple PAK formats including Unreal Engine PAK and Quake PAK formats.

## Tools Included

### 1. Unreal Engine PAK Extractor (`unreal_pak_extractor.py`) ⭐ **NEW**

Extract game assets from **Unreal Engine PAK archives** without requiring encryption keys!

#### Features
- 🎮 **Unreal Engine Support**: Supports PAK versions 1-11
- 🔓 **No Keys Required**: Works with unencrypted PAK files without asking for keys
- 📦 **Compression Support**: Handles ZLIB and GZIP compressed assets
- 🗂️ **Directory Structure**: Preserves original directory structure
- 📊 **Detailed Info**: Shows compression ratios, file sizes, and more
- ⚡ **Fast Extraction**: Efficient multi-block decompression

#### Supported Formats
- **Unreal Engine PAK**: Versions 1-11 (UE3, UE4, UE5)
- **Compression**: ZLIB, GZIP
- **Note**: Only unencrypted PAK files are supported

### 2. Quake PAK Extractor (`pak_extractor.py`)

Extract assets from classic **Quake PAK format** archives.

#### Features
- 📦 **List Files**: View all files contained in a PAK archive
- 🔓 **Extract All**: Extract all files from a PAK archive
- 🎯 **Extract Specific**: Extract individual files by name
- 🔍 **Format Detection**: Automatically detects PAK file format
- 📊 **File Information**: Display file sizes, offsets, and archive statistics

#### Supported Formats
- **Quake PAK Format**: The classic PAK format used by Quake and many other games
- **Generic PAK Format**: Support for other simple PAK archive formats

## Installation

No additional dependencies required! Both extractors use only Python standard library modules.

```bash
# Clone or download this repository
git clone <repository-url>
cd <repository-directory>

# Make the scripts executable (optional)
chmod +x unreal_pak_extractor.py pak_extractor.py
```

## Quick Start

### For Unreal Engine PAK Files (Most Modern Games) ⭐

```bash
# List all files in an Unreal Engine PAK
python3 unreal_pak_extractor.py YourGame.pak --list

# Extract all files
python3 unreal_pak_extractor.py YourGame.pak --extract-all --output ./game_assets

# Extract a specific file
python3 unreal_pak_extractor.py YourGame.pak --extract Content/Textures/player.png
```

### For Quake PAK Files (Classic Games)

A sample Quake PAK file (`test.pak`) is included for testing. You can recreate it anytime with:

```bash
python3 create_test_pak.py
```

Then test the Quake PAK extractor:

```bash
python3 pak_extractor.py test.pak --list
python3 pak_extractor.py test.pak --extract-all
```

---

## Usage Guide

## Unreal Engine PAK Extractor Usage

### List all files in an Unreal PAK archive

```bash
python3 unreal_pak_extractor.py game.pak --list
```

Or simply:

```bash
python3 unreal_pak_extractor.py game.pak
```

### Extract all files

Extract all files to the default `extracted` directory:

```bash
python3 unreal_pak_extractor.py game.pak --extract-all
```

Extract to a custom directory:

```bash
python3 unreal_pak_extractor.py game.pak --extract-all --output ./game_assets
```

### Extract a specific file

```bash
python3 unreal_pak_extractor.py game.pak --extract Content/Textures/player.png
```

With custom output directory:

```bash
python3 unreal_pak_extractor.py game.pak --extract Content/Models/player.uasset --output ./models
```

### Show PAK file information

```bash
python3 unreal_pak_extractor.py game.pak --info
```

### Command Line Options (Unreal Engine Extractor)

```
usage: unreal_pak_extractor.py [-h] [-l] [-a] [-e FILENAME] [-o OUTPUT] [-i] pak_file

positional arguments:
  pak_file              Path to the PAK file

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all files in the archive
  -a, --extract-all     Extract all files from the archive
  -e FILENAME, --extract FILENAME
                        Extract a specific file
  -o OUTPUT, --output OUTPUT
                        Output directory for extracted files (default: extracted)
  -i, --info            Show information about the PAK file
```

---

## Quake PAK Extractor Usage

### List all files in a Quake PAK archive

```bash
python3 pak_extractor.py myfile.pak --list
```

### Extract all files

```bash
python3 pak_extractor.py myfile.pak --extract-all --output ./my_files
```

### Extract a specific file

```bash
python3 pak_extractor.py myfile.pak --extract textures/image.png --output ./models
```

### Command Line Options (Quake Extractor)

```
usage: pak_extractor.py [-h] [-l] [-a] [-e FILENAME] [-o OUTPUT] [-i] pak_file

positional arguments:
  pak_file              Path to the PAK file

optional arguments:
  -h, --help            show this help message and exit
  -l, --list            List all files in the archive
  -a, --extract-all     Extract all files from the archive
  -e FILENAME, --extract FILENAME
                        Extract a specific file
  -o OUTPUT, --output OUTPUT
                        Output directory for extracted files (default: extracted)
  -i, --info            Show information about the PAK file
```

## Python API

### Unreal Engine PAK Extractor API

You can use the Unreal Engine extractor programmatically in your Python scripts:

```python
from unreal_pak_extractor import UnrealPakExtractor

# Initialize extractor
extractor = UnrealPakExtractor("game.pak")

# Parse the PAK file
if extractor.parse():
    # List all files
    extractor.list_files()
    
    # Extract all files
    extractor.extract_all(output_dir="extracted")
    
    # Extract a specific file
    extractor.extract_file("Content/Textures/player.png", output_dir=".")
    
    # Access file entries directly
    for filename, entry in extractor.entries.items():
        print(f"{filename}: {entry.uncompressed_size} bytes")
        print(f"  Compressed: {entry.is_compressed()}")
        print(f"  Offset: {entry.offset}")
```

### Quake PAK Extractor API

You can also use the Quake extractor programmatically:

```python
from pak_extractor import PAKExtractor

# Initialize extractor
extractor = PAKExtractor("myfile.pak")

# Parse the PAK file
entries = extractor.parse()

# List all files
extractor.list_files()

# Extract all files
extractor.extract_all(output_dir="extracted")

# Extract a specific file
extractor.extract_specific("textures/image.png", output_dir=".")

# Access file entries directly
for entry in extractor.entries:
    print(f"{entry.filename}: {entry.size} bytes at offset {entry.offset}")
```

## PAK File Formats

### Unreal Engine PAK Format

The Unreal Engine PAK format is more complex and consists of:

1. **File Data**: All file contents stored at the beginning
2. **Index**: Directory of all files (stored near end of file)
   - Mount point
   - File entries with:
     - Filename
     - Offset and sizes
     - Compression method
     - Compression blocks (if compressed)
     - SHA1 hash
     - Timestamps
3. **Footer** (at end of file):
   - Encryption GUID (version 7+)
   - Magic number: 0x5A6F12E1
   - Version number
   - Index offset and size

**Supported Versions**: 1-11 (covers UE3, UE4, UE5)
**Compression**: ZLIB, GZIP
**Encryption**: Not supported (unencrypted files only)

### Quake PAK Format

The Quake PAK format consists of:

1. **Header (12 bytes)**:
   - Signature: "PACK" (4 bytes)
   - Directory offset (4 bytes, little-endian)
   - Directory size (4 bytes, little-endian)

2. **File Data**: Raw file contents

3. **Directory Entries (64 bytes each)**:
   - Filename (56 bytes, null-terminated)
   - File offset (4 bytes, little-endian)
   - File size (4 bytes, little-endian)

## Examples

### Example 1: Extracting Unreal Engine game assets

```bash
# List contents of an Unreal Engine game's PAK file
python3 unreal_pak_extractor.py GameName-Windows.pak --list

# Extract all textures and models
python3 unreal_pak_extractor.py GameName-Windows.pak --extract-all --output ./game_assets

# Extract only textures
python3 unreal_pak_extractor.py GameName-Windows.pak --extract Content/Textures/Character.uasset
```

### Example 2: Working with compressed Unreal Engine PAK files

```bash
# The extractor automatically handles compressed files
python3 unreal_pak_extractor.py CompressedGame.pak --extract-all

# View compression statistics
python3 unreal_pak_extractor.py CompressedGame.pak --list
```

### Example 3: Extracting Quake PAK assets

```bash
# Extract from classic Quake PAK
python3 pak_extractor.py pak0.pak --list
python3 pak_extractor.py pak0.pak --extract-all --output ./quake_assets
```

## Troubleshooting

### Unreal Engine PAK Issues

#### "This PAK file is encrypted!" error

The PAK file requires an AES encryption key to decrypt. This extractor **only supports unencrypted PAK files**. To extract encrypted PAK files, you would need:
- The game's AES encryption key
- A different tool that supports encryption

#### "Invalid PAK magic" error

The file might not be an Unreal Engine PAK file. Try the Quake PAK extractor instead:
```bash
python3 pak_extractor.py yourfile.pak --list
```

#### Decompression errors

If files fail to decompress, the PAK might use an unsupported compression method. Currently supported:
- ZLIB
- GZIP

#### Which extractor should I use?

- **Modern games (2012+)**: Try `unreal_pak_extractor.py` first
- **Classic games (pre-2000s)**: Try `pak_extractor.py`
- **Not sure**: Try both! They'll tell you if the format is unsupported

### Quake PAK Issues

#### "Invalid Quake PAK file signature" error

This means the file is not in Quake PAK format. Try the Unreal Engine extractor instead.

### General Issues

#### Empty file list

If the extractor shows "No files found in PAK archive", the file might be:
- Corrupted
- In an unsupported format
- Encrypted
- Not actually a PAK file

#### Extraction errors

If specific files fail to extract, check:
- Available disk space
- Write permissions in the output directory
- Whether the PAK file is corrupted

## Contributing

Contributions are welcome! If you encounter PAK files that aren't supported, please:
1. Open an issue with details about the file format
2. Provide a sample file if possible
3. Submit a pull request with format support

## License

This project is provided as-is for educational and archival purposes.

## Acknowledgments

- Quake PAK format specification
- Various game modding communities for format documentation

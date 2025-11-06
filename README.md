# PAK File Extractor

A Python-based tool to extract and manage PAK archive files commonly used in video games. Supports multiple PAK formats including Quake PAK format and other common variants.

## Features

- 📦 **List Files**: View all files contained in a PAK archive
- 🔓 **Extract All**: Extract all files from a PAK archive
- 🎯 **Extract Specific**: Extract individual files by name
- 🔍 **Format Detection**: Automatically detects PAK file format
- 📊 **File Information**: Display file sizes, offsets, and archive statistics

## Supported Formats

- **Quake PAK Format**: The classic PAK format used by Quake and many other games
- **Generic PAK Format**: Support for other simple PAK archive formats

## Installation

No additional dependencies required! The extractor uses only Python standard library modules.

```bash
# Clone or download this repository
git clone <repository-url>
cd <repository-directory>

# Make the script executable (optional)
chmod +x pak_extractor.py
```

## Quick Test

A sample PAK file (`test.pak`) is included for testing. You can recreate it anytime with:

```bash
python3 create_test_pak.py
```

Then test the extractor:

```bash
python3 pak_extractor.py test.pak --list
python3 pak_extractor.py test.pak --extract-all
```

## Usage

### List all files in a PAK archive

```bash
python pak_extractor.py myfile.pak --list
```

Or simply:

```bash
python pak_extractor.py myfile.pak
```

### Extract all files

Extract all files to the default `extracted` directory:

```bash
python pak_extractor.py myfile.pak --extract-all
```

Extract to a custom directory:

```bash
python pak_extractor.py myfile.pak --extract-all --output ./my_files
```

### Extract a specific file

```bash
python pak_extractor.py myfile.pak --extract textures/image.png
```

With custom output directory:

```bash
python pak_extractor.py myfile.pak --extract models/player.mdl --output ./models
```

### Show PAK file information

```bash
python pak_extractor.py myfile.pak --info
```

## Command Line Options

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

You can also use the extractor programmatically in your Python scripts:

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

## PAK File Format

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

### Example 1: Extracting game assets

```bash
# List contents of a game's PAK file
python pak_extractor.py game_assets.pak --list

# Extract all textures and models
python pak_extractor.py game_assets.pak --extract-all --output ./game_files
```

### Example 2: Working with specific files

```bash
# Extract only a specific texture
python pak_extractor.py textures.pak --extract sprites/player.png

# Extract a specific map file
python pak_extractor.py maps.pak --extract maps/level1.bsp --output ./maps
```

## Troubleshooting

### "Invalid Quake PAK file signature" error

This means the file is not in Quake PAK format. The extractor will attempt to parse it as a generic PAK format, but if that fails, the format may not be supported yet.

### Empty file list

If the extractor shows "No files found in PAK archive", the file might be:
- Corrupted
- In an unsupported format
- Not actually a PAK file

### Extraction errors

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

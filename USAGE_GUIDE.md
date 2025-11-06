# Unreal Engine PAK Extractor - Usage Guide

## Overview

This is a comprehensive Unreal Engine PAK file extractor that can extract game assets **without requiring encryption keys**. It supports PAK versions 1-11 (covering UE3, UE4, and UE5 games).

## Key Features

✅ **No Encryption Keys Required** - Works with unencrypted PAK files automatically
✅ **Automatic Decompression** - Handles ZLIB and GZIP compressed assets
✅ **Smart Format Detection** - Automatically detects PAK version and format
✅ **Preserves Directory Structure** - Maintains original file paths
✅ **Detailed Statistics** - Shows compression ratios, file sizes, and more
✅ **Progress Tracking** - Real-time extraction progress

## Quick Start

### 1. List Files in a PAK Archive

```bash
python3 unreal_pak_extractor.py YourGame.pak --list
```

This will display:
- PAK version
- Mount point
- Total number of files
- Each file's size and compression status
- Total compressed/uncompressed sizes

### 2. Extract All Files

```bash
python3 unreal_pak_extractor.py YourGame.pak --extract-all
```

By default, files are extracted to the `./extracted` directory.

To specify a custom output directory:

```bash
python3 unreal_pak_extractor.py YourGame.pak --extract-all --output ./my_assets
```

### 3. Extract a Specific File

```bash
python3 unreal_pak_extractor.py YourGame.pak --extract Content/Textures/player.png --output ./textures
```

## Common Use Cases

### Extracting Textures from a Game

```bash
# First, list all files to find texture paths
python3 unreal_pak_extractor.py GameName.pak --list | grep Textures

# Then extract specific textures
python3 unreal_pak_extractor.py GameName.pak --extract Content/Textures/Character.uasset
```

### Extracting All Assets from Multiple PAK Files

Many games use multiple PAK files (e.g., `GameName-Windows.pak`, `GameName-Content.pak`).

```bash
# Extract from all PAK files
for pak in *.pak; do
    python3 unreal_pak_extractor.py "$pak" --extract-all --output "./extracted_$(basename $pak .pak)"
done
```

### Analyzing PAK Contents

```bash
# Get detailed information about a PAK file
python3 unreal_pak_extractor.py GameName.pak --info

# Count files by type
python3 unreal_pak_extractor.py GameName.pak --list | grep -c "\.uasset"
python3 unreal_pak_extractor.py GameName.pak --list | grep -c "\.umap"
```

## Understanding PAK File Structure

### Unreal Engine PAK Format

```
[File Data 1]
[File Data 2]
...
[File Data N]
[Index - Contains file metadata]
[Footer - 44 bytes]
```

The footer contains:
- Magic number: `0x5A6F12E1`
- PAK version
- Index offset and size
- Encryption information

### File Entries

Each file entry in the index contains:
- **Filename**: Full path including mount point
- **Offset**: Location in PAK file
- **Compressed Size**: Size when compressed
- **Uncompressed Size**: Original file size
- **Compression Method**: None, ZLIB, or GZIP
- **Timestamp**: File modification time
- **SHA1 Hash**: For integrity verification
- **Compression Blocks**: For multi-block compressed files

## What About Encrypted PAK Files?

### Detection

The extractor will automatically detect if a PAK file is encrypted:

```
ERROR: This PAK file is encrypted!
Encrypted PAK files require an AES encryption key to extract.
This extractor only supports unencrypted PAK files.
```

### Why No Encryption Support?

This extractor focuses on **unencrypted** PAK files because:
1. Many indie and older games don't use encryption
2. Encryption keys are game-specific and legally sensitive
3. Keeping the tool simple and legal

### How to Tell if a PAK is Encrypted?

Run the extractor - it will tell you immediately:

```bash
python3 unreal_pak_extractor.py game.pak --info
```

Look for: `Encrypted: Yes` or `Encrypted: No`

## Supported Games

This extractor should work with **unencrypted** PAK files from:

### Unreal Engine 3 Games
- Mirrors Edge
- Batman: Arkham Asylum (unencrypted PAKs)
- Borderlands (unencrypted PAKs)
- BioShock Infinite (unencrypted PAKs)

### Unreal Engine 4 Games
- Many indie games
- Satisfactory (early versions)
- Astroneer (early versions)
- Deep Rock Galactic (unencrypted PAKs)

### Unreal Engine 5 Games
- Various indie titles with unencrypted PAKs

**Note**: Most commercial AAA games use encrypted PAK files, which are NOT supported.

## Compression Support

The extractor handles these compression methods:

### ✅ Supported
- **ZLIB** (most common)
- **GZIP**
- **None** (uncompressed)

### ❌ Not Supported
- **Oodle** (proprietary, requires license)
- **LZ4** (may be added in future)
- **Custom** compression methods

## File Types You Can Extract

Common Unreal Engine file types:

- **`.uasset`** - Asset files (models, textures, blueprints)
- **`.umap`** - Map/level files
- **`.uexp`** - Export data (paired with .uasset)
- **`.ubulk`** - Bulk data
- **`.png`, `.jpg`** - Texture files
- **`.wav`, `.ogg`** - Audio files
- **`.ini`, `.cfg`** - Configuration files
- **`.locres`** - Localization resources

## Troubleshooting

### "Invalid PAK magic" Error

**Problem**: The file is not an Unreal Engine PAK file.

**Solutions**:
1. Try the Quake PAK extractor: `python3 pak_extractor.py yourfile.pak --list`
2. The file might be corrupted
3. The file might not be a PAK file at all

### "This PAK file is encrypted!" Error

**Problem**: The PAK requires an AES key.

**Solutions**:
1. This extractor doesn't support encrypted PAK files
2. Look for unencrypted PAK files in the game directory (some games have both)
3. Search for game-specific extraction tools

### Decompression Errors

**Problem**: Files fail to decompress.

**Solutions**:
1. The PAK might use Oodle or another unsupported compression
2. The PAK file might be corrupted
3. File a bug report with the PAK version info

### "No files found in PAK archive"

**Problem**: Index parsing failed.

**Solutions**:
1. The PAK might be encrypted (check for encryption warning)
2. The PAK version might be too new/old
3. The PAK file might be corrupted

### Files Extract but Don't Open

**Problem**: Extracted files are corrupt or in wrong format.

**Explanation**:
- `.uasset` and `.umap` files are Unreal Engine proprietary formats
- You need Unreal Engine Editor or UE Viewer to open them
- Raw texture/audio files will work in standard programs

## Python API Usage

You can integrate the extractor into your own Python scripts:

```python
from unreal_pak_extractor import UnrealPakExtractor

# Initialize
extractor = UnrealPakExtractor("game.pak")

# Parse the PAK
if not extractor.parse():
    print("Failed to parse PAK file")
    exit(1)

# Check if encrypted
if extractor.encrypted:
    print("PAK is encrypted!")
    exit(1)

# Get info
print(f"PAK Version: {extractor.pak_version}")
print(f"Mount Point: {extractor.mount_point}")
print(f"Files: {len(extractor.entries)}")

# List all texture files
for filename, entry in extractor.entries.items():
    if 'Textures' in filename:
        print(f"{filename} - {entry.uncompressed_size} bytes")

# Extract specific file
if "Content/Textures/player.png" in extractor.entries:
    extractor.extract_file("Content/Textures/player.png", "./output")

# Extract all files
extractor.extract_all(output_dir="./all_assets")
```

## Performance Tips

### For Large PAK Files (> 1 GB)

```bash
# List files first to see what you need
python3 unreal_pak_extractor.py huge_game.pak --list > file_list.txt

# Extract only what you need
python3 unreal_pak_extractor.py huge_game.pak --extract Content/Specific/File.uasset
```

### Batch Extraction

```bash
# Create a script for multiple extractions
#!/bin/bash
FILES=(
    "Content/Textures/player.uasset"
    "Content/Models/weapon.uasset"
    "Content/Maps/level1.umap"
)

for file in "${FILES[@]}"; do
    python3 unreal_pak_extractor.py game.pak --extract "$file" --output ./extracted
done
```

## Example Output

### Listing Files

```
================================================================================
Unreal Engine PAK Archive: GameName-Windows.pak
================================================================================
PAK Version: 8
Mount Point: ../../../GameName/
Total Files: 1,543
Encrypted: No
================================================================================

Filename                                                     Size   Compressed
------------------------------------------------------------------------------
Content/Textures/Character_Diffuse.uasset               2.34 MB          Yes
Content/Textures/Character_Normal.uasset                1.89 MB          Yes
Content/Models/Character_Skeleton.uasset              156.78 KB           No
Content/Blueprints/BP_Player.uasset                    45.23 KB           No
...
------------------------------------------------------------------------------
Total Size: 3.45 GB (Compressed: 2.12 GB, Ratio: 38.6%)
```

### Extracting Files

```
Extracting 1,543 files to: ./extracted

[1/1543] OK       Content/Textures/Character_Diffuse.uasset
[2/1543] OK       Content/Textures/Character_Normal.uasset
[3/1543] OK       Content/Models/Character_Skeleton.uasset
...
[1543/1543] OK   Content/Maps/FinalLevel.umap

================================================================================
Extraction Complete!
  Success: 1543
  Failed:  0
  Output:  ./extracted
================================================================================
```

## Need Help?

1. **Check the main README**: `README.md`
2. **Run with --help**: `python3 unreal_pak_extractor.py --help`
3. **Check PAK is unencrypted**: Run `--info` first
4. **Try the Quake extractor**: For non-Unreal PAK files

## Legal Notice

This tool is for educational, modding, and archival purposes. Always respect:
- Game EULAs and Terms of Service
- Copyright and intellectual property rights
- The original game developers' wishes

Only extract assets from games you own and for personal use.

# 🎮 Unreal Engine PAK Manager

**Interactive tool for unpacking, editing, and repacking Unreal Engine PAK files**

## ✨ Features

- 🗂️ **Automatic Folder Management** - Creates organized folder structure
- 📦 **Auto-Detection** - Automatically finds PAK files
- 🔓 **Unpack** - Extract all game assets from PAK files
- ✏️ **Edit** - Modify game assets (textures, models, etc.)
- 📦 **Repack** - Create new PAK with your edits
- 🧹 **Clear Output** - Clean up extracted files
- 📁 **Show Paths** - View all folder locations

## 🚀 Quick Start

### Step 1: Run the Tool

```bash
python3 pak_manager.py
```

### Step 2: Follow the Interactive Menu

```
I have create new folders
============================================================
✓ Created: Original pak file/
✓ Created: extracted data-blocks/
✓ Created: edited game assets here/
✓ Created: repacked pak file with edited data/

============================================================
UNREAL ENGINE PAK MANAGER
============================================================

Main Menu

  1. Unpack OBB (.pak file)
  2. Clear Output
  3. Repack OBB
  4. Show Paths
  5. Exit

============================================================
Enter your choice [1/2/3/4/5] (1):
```

## 📋 Complete Workflow

### 1️⃣ **Unpack PAK File**

1. Place your `.pak` file in the `Original pak file/` folder
2. Select option **1** (Unpack OBB)
3. The tool will automatically:
   - Detect your PAK file
   - Parse and validate it
   - Extract all files to `extracted data-blocks/`

**Example:**
```
📦 Found PAK file: YourGame-Windows.pak
⏳ Parsing PAK file...
✓ PAK Version: 8
✓ Mount Point: ../../../YourGame/
✓ Total Files: 1,543
⏳ Extracting 1,543 files...
✓ UNPACKING COMPLETE!
```

### 2️⃣ **Edit Game Assets**

1. Navigate to `extracted data-blocks/` folder
2. Find the files you want to edit (textures, models, etc.)
3. Copy them to `edited game assets here/` folder
4. Edit the files using your tools (Photoshop, Blender, etc.)
5. Keep the same filename and folder structure!

**Example:**
```
edited game assets here/
  └── Content/
      └── Textures/
          ├── Character_Diffuse.uasset  ← Your edited texture
          └── Logo.png                   ← Your edited image
```

### 3️⃣ **Repack PAK File**

1. Select option **3** (Repack OBB)
2. The tool will:
   - Scan for edited files
   - Replace originals with your edits
   - Create a new PAK file
3. Find your repacked PAK in `repacked pak file with edited data/`

**Example:**
```
✓ Found 2 edited file(s):
  • Content/Textures/Character_Diffuse.uasset
  • Content/Textures/Logo.png

🔄 Replacing: Content/Textures/Character_Diffuse.uasset
🔄 Replacing: Content/Textures/Logo.png

✓ REPACKING COMPLETE!
Filename: repacked_YourGame-Windows.pak
Size: 2,345.67 MB
```

### 4️⃣ **Use Your Modded PAK**

1. Find your new PAK in `repacked pak file with edited data/`
2. Back up the original game PAK
3. Replace with your repacked PAK
4. Launch the game and enjoy your mods! 🎉

## 📂 Folder Structure

After running the tool, you'll have:

```
workspace/
├── Original pak file/              ← Place your .pak file here
│   └── YourGame-Windows.pak
│
├── extracted data-blocks/          ← Extracted game files (auto-generated)
│   └── Content/
│       ├── Textures/
│       ├── Models/
│       └── ...
│
├── edited game assets here/        ← Place your edited files here
│   └── Content/
│       └── Textures/
│           └── Character_Diffuse.uasset  ← Your edit
│
└── repacked pak file with edited data/  ← Your new PAK file (output)
    └── repacked_YourGame-Windows.pak
```

## 🎯 Menu Options Explained

### Option 1: Unpack OBB (.pak file)
- Searches for PAK files in `Original pak file/` folder
- Extracts all contents to `extracted data-blocks/`
- Shows PAK info (version, file count, etc.)
- **Requirement**: PAK must be unencrypted

### Option 2: Clear Output
- Clears `extracted data-blocks/` folder
- Clears `repacked pak file with edited data/` folder
- Optionally clears `edited game assets here/` folder
- Resets the tool state

### Option 3: Repack OBB
- Scans `edited game assets here/` for modified files
- Replaces originals in `extracted data-blocks/`
- Creates new PAK in `repacked pak file with edited data/`
- **Requirement**: Must unpack first (Option 1)

### Option 4: Show Paths
- Displays all folder paths
- Shows file counts
- Shows currently loaded PAK info
- Useful for troubleshooting

### Option 5: Exit
- Safely exits the program

## 💡 Tips & Best Practices

### Editing Assets

✅ **DO:**
- Keep the exact same filename
- Maintain the folder structure
- Test with small edits first
- Back up original PAK files
- Use compatible file formats

❌ **DON'T:**
- Rename files
- Change folder structure
- Edit files directly in `extracted data-blocks/`
- Skip backing up originals

### File Types You Can Edit

- **Textures**: `.png`, `.jpg`, `.tga`, `.uasset` (texture assets)
- **Models**: `.uasset`, `.uexp` (paired files)
- **Audio**: `.wav`, `.ogg`
- **Text**: `.ini`, `.cfg`, `.locres`
- **Blueprints**: `.uasset` (requires Unreal Engine knowledge)

### Keeping Folder Structure

When editing `Content/Textures/Player.uasset`:

```
✅ CORRECT:
edited game assets here/
  └── Content/
      └── Textures/
          └── Player.uasset

❌ WRONG:
edited game assets here/
  └── Player.uasset  ← Missing folder structure!
```

## ⚠️ Important Limitations

### What Works ✅
- **Unencrypted PAK files** only
- PAK versions 1-11 (UE3, UE4, UE5)
- Asset replacement (same size or larger)
- Adding new files
- Texture modding
- Audio replacement

### What Doesn't Work ❌
- **Encrypted PAK files** (most AAA games)
- Oodle compression (will create uncompressed PAK)
- Automatic compression (repacked PAKs are uncompressed)
- Blueprint logic editing (needs Unreal Engine)

### Encrypted PAK Files

If you see this error:
```
❌ ERROR: This PAK file is ENCRYPTED!
```

The PAK requires an AES encryption key. This tool only works with **unencrypted** PAK files.

## 🔧 Troubleshooting

### "No PAK file found in 'Original pak file' folder!"

**Solution**: Place your `.pak` file in the `Original pak file/` folder

### "Please unpack a PAK file first!"

**Solution**: Run Option 1 (Unpack) before trying to repack

### "No edited files found"

**Solutions**:
- Make sure edited files are in `edited game assets here/` folder
- Maintain the same folder structure as extracted files
- Check file names match exactly

### Repacked PAK doesn't work in game

**Common causes**:
1. Wrong filename - must match original
2. Game uses signature verification
3. PAK file is in wrong directory
4. Game requires encryption (not supported)

**Solutions**:
- Ensure filename matches original
- Check game modding community for requirements
- Some games don't support modded PAKs

### Files extract but are corrupted

**Causes**:
- Original PAK uses unsupported compression
- PAK file is actually encrypted
- PAK file is corrupted

**Solution**: Try a different PAK file or check game forums

## 📊 Example Session

```bash
$ python3 pak_manager.py

I have create new folders
============================================================
✓ Created: Original pak file/
✓ Created: extracted data-blocks/
✓ Created: edited game assets here/
✓ Created: repacked pak file with edited data/

Main Menu
  1. Unpack OBB (.pak file)
  2. Clear Output
  3. Repack OBB
  4. Show Paths
  5. Exit

Enter your choice [1/2/3/4/5] (1): 1

============================================================
UNPACKING PAK FILE
============================================================

📦 Found PAK file: MyGame-Windows.pak

⏳ Parsing PAK file...
✓ PAK Version: 8
✓ Mount Point: ../../../MyGame/
✓ Total Files: 523

⏳ Extracting 523 files...
[523/523] OK   Content/Maps/MainMenu.umap

✓ UNPACKING COMPLETE!

Press Enter to continue...

Enter your choice [1/2/3/4/5] (1): 3

============================================================
REPACKING PAK FILE
============================================================

⏳ Scanning for edited files...

✓ Found 1 edited file(s):
  • Content/Textures/Logo.png

🔄 Replacing: Content/Textures/Logo.png

⏳ Creating PAK file: repacked_MyGame-Windows.pak
📦 Building file list...
✓ Found 523 files to pack
⏳ Writing files to PAK...
  Progress: 523/523 files
✓ All files written
⏳ Writing PAK index...
⏳ Writing PAK footer...
✓ PAK footer written

✓ REPACKING COMPLETE!
Filename: repacked_MyGame-Windows.pak
Size: 1,234.56 MB

Press Enter to continue...
```

## 🎮 Modding Workflow

### Texture Modding

1. **Unpack**: Extract PAK (Option 1)
2. **Find**: Locate texture in `extracted data-blocks/Content/Textures/`
3. **Copy**: Copy to `edited game assets here/Content/Textures/`
4. **Edit**: Modify with Photoshop/GIMP
5. **Repack**: Create new PAK (Option 3)
6. **Test**: Replace original PAK and test in-game

### Audio Replacement

1. **Unpack**: Extract PAK
2. **Find**: Locate audio in `extracted data-blocks/Content/Audio/`
3. **Copy**: Copy to `edited game assets here/Content/Audio/`
4. **Edit**: Replace with same format (OGG/WAV)
5. **Repack**: Create new PAK
6. **Test**: Test in-game

## 🔗 Related Tools

- **pak_extractor.py** - Quake PAK extractor (for old games)
- **unreal_pak_extractor.py** - Command-line UE PAK extractor
- **Unreal Engine** - For advanced asset editing
- **UE Viewer (umodel)** - View .uasset files

## 📝 Notes

- First run creates all folders automatically
- Tool remembers last unpacked PAK during session
- Repacked PAKs are uncompressed (larger file size)
- Always test with a backup of original PAK
- Some games verify PAK signatures (won't work)

## ⚖️ Legal Notice

This tool is for:
- **Personal modding** of games you own
- **Educational purposes**
- **Game development** testing

Always respect:
- Game EULAs and Terms of Service
- Copyright and IP rights
- Developer wishes regarding modding

## 🆘 Support

If you encounter issues:

1. Check this README
2. Try Option 4 (Show Paths) to verify folders
3. Check if PAK is encrypted (see error message)
4. Ensure unpack completed successfully before repacking
5. Verify edited files have correct folder structure

---

**Created**: 2025-11-06  
**Tool**: pak_manager.py  
**Requires**: Python 3.6+, unreal_pak_extractor.py  
**Status**: Ready to use! 🚀

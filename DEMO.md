# 🎬 DEMO - See It In Action

## Watch The Tool Work!

Here's exactly what you'll see when you run `pak_manager.py`:

---

## 🎯 First Run - Folder Creation

```bash
$ python3 pak_manager.py
```

**OUTPUT:**
```
============================================================
I have create new folders
============================================================

✓ Created: Original pak file/
✓ Created: extracted data-blocks/
✓ Created: edited game assets here/
✓ Created: repacked pak file with edited data/

============================================================
Folder structure ready!
============================================================


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

---

## 📦 Option 1 - Unpack OBB

**YOU TYPE:** `1` [Enter]

**IF NO PAK FILE:**
```
============================================================
UNPACKING PAK FILE
============================================================

❌ ERROR: No PAK file found in 'Original pak file' folder!

Please place your .pak file in: Original pak file/

Press Enter to continue...
```

**AFTER PLACING PAK FILE:**
```
============================================================
UNPACKING PAK FILE
============================================================

📦 Found PAK file: GameName-Windows.pak

⏳ Parsing PAK file...
✓ PAK Version: 8
✓ Mount Point: ../../../GameName/
✓ Total Files: 1,543

⏳ Extracting 1,543 files...
------------------------------------------------------------
[1/1543] OK       Content/Textures/Character_Diffuse.uasset
[2/1543] OK       Content/Textures/Character_Normal.uasset
[3/1543] OK       Content/Models/Character_Skeleton.uasset
...
[1543/1543] OK   Content/Maps/FinalLevel.umap

============================================================
✓ UNPACKING COMPLETE!
============================================================

Files extracted to: extracted data-blocks/

Press Enter to continue...
```

---

## 🧹 Option 2 - Clear Output

**YOU TYPE:** `2` [Enter]

```
============================================================
CLEAR OUTPUT
============================================================

This will delete:
  • extracted data-blocks/
  • repacked pak file with edited data/

Are you sure? (y/n): y
✓ Cleared: extracted data-blocks/
✓ Cleared: repacked pak file with edited data/

Also clear 'edited game assets here' folder? (y/n): n

✓ All output folders cleared!

Press Enter to continue...
```

---

## 📦 Option 3 - Repack OBB

**YOU TYPE:** `3` [Enter]

**IF NOT UNPACKED YET:**
```
============================================================
REPACKING PAK FILE
============================================================

❌ ERROR: Please unpack a PAK file first!

Press Enter to continue...
```

**AFTER UNPACKING AND EDITING:**
```
============================================================
REPACKING PAK FILE
============================================================

⏳ Scanning for edited files...

✓ Found 2 edited file(s):
  • Content/Textures/Logo.png
  • Content/Audio/MenuMusic.ogg

🔄 Replacing: Content/Textures/Logo.png
🔄 Replacing: Content/Audio/MenuMusic.ogg

⏳ Creating PAK file: repacked_GameName-Windows.pak

📦 Building file list...
✓ Found 1,543 files to pack

⏳ Writing files to PAK...
  Progress: 1543/1543 files
✓ All files written

⏳ Writing PAK index...
⏳ Writing PAK footer...
✓ PAK footer written

============================================================
✓ REPACKING COMPLETE!
============================================================

Repacked PAK saved to: repacked pak file with edited data/
Filename: repacked_GameName-Windows.pak
Size: 2,345.67 MB

Press Enter to continue...
```

---

## 📁 Option 4 - Show Paths

**YOU TYPE:** `4` [Enter]

```
============================================================
FOLDER PATHS
============================================================

✓ Original pak file/
   Path: /workspace/Original pak file
   Files: 1

✓ extracted data-blocks/
   Path: /workspace/extracted data-blocks
   Files: 1543

✓ edited game assets here/
   Path: /workspace/edited game assets here
   Files: 2

✓ repacked pak file with edited data/
   Path: /workspace/repacked pak file with edited data
   Files: 1

Current PAK File:
  GameName-Windows.pak
  Path: /workspace/Original pak file/GameName-Windows.pak
  Size: 2,234.56 MB

Press Enter to continue...
```

---

## 🚪 Option 5 - Exit

**YOU TYPE:** `5` [Enter]

```
============================================================
Thank you for using Unreal Engine PAK Manager!
============================================================
```

---

## 🎮 Complete Workflow Demo

### 1. Place Your PAK File

```bash
$ ls
pak_manager.py  unreal_pak_extractor.py  ...

$ cp ~/MyGame/Content.pak "Original pak file/"
```

### 2. Run & Unpack

```bash
$ python3 pak_manager.py

# Choose 1 (Unpack)
Enter your choice [1/2/3/4/5] (1): 1

# Watch it extract...
✓ UNPACKING COMPLETE!
```

### 3. Edit Files

```bash
$ cd "extracted data-blocks/Content/Textures"
$ ls
Logo.png  Character.uasset  ...

# Copy file you want to edit
$ mkdir -p "../../../edited game assets here/Content/Textures"
$ cp Logo.png "../../../edited game assets here/Content/Textures/"

# Edit it
$ gimp "../../../edited game assets here/Content/Textures/Logo.png"
# (Make your changes, save, exit)
```

### 4. Repack

```bash
$ python3 pak_manager.py

# Choose 3 (Repack)
Enter your choice [1/2/3/4/5] (1): 3

# Watch it repack...
✓ REPACKING COMPLETE!
```

### 5. Use Your Modded PAK

```bash
$ cd "repacked pak file with edited data"
$ ls
repacked_Content.pak

# Backup original
$ cp ~/MyGame/Content.pak ~/MyGame/Content.pak.backup

# Install modded PAK
$ cp repacked_Content.pak ~/MyGame/Content.pak

# Play!
$ cd ~/MyGame && ./GameName.exe
```

---

## 🎯 Error Handling Demo

### Encrypted PAK File

```
============================================================
UNPACKING PAK FILE
============================================================

📦 Found PAK file: EncryptedGame.pak

⏳ Parsing PAK file...
✓ PAK Version: 8
✓ Encrypted: Yes

❌ ERROR: This PAK file is ENCRYPTED!
Encrypted PAK files cannot be unpacked without the encryption key.

Press Enter to continue...
```

### Invalid PAK File

```
============================================================
UNPACKING PAK FILE
============================================================

📦 Found PAK file: notapak.pak

⏳ Parsing PAK file...
Invalid PAK magic: 0x0, expected 0x5a6f12e1

❌ Failed to parse PAK file!
The file might be encrypted or corrupted.

Press Enter to continue...
```

### No Edited Files

```
============================================================
REPACKING PAK FILE
============================================================

⏳ Scanning for edited files...

⚠️  No edited files found in 'edited game assets here' folder.
Repacking with original files only.

⏳ Creating PAK file: repacked_Game.pak
...
```

---

## 🎊 That's It!

The tool is **fully interactive** and **guides you through every step**.

### Key Points:
- ✅ Clear visual feedback (✓, ✗, ⏳, 🔄)
- ✅ Progress indicators
- ✅ Error messages with solutions
- ✅ Confirmation prompts for destructive operations
- ✅ Press Enter to continue after each operation
- ✅ Default option (1) if you just press Enter

### Try It Now:

```bash
python3 pak_manager.py
```

**That's all you need!** The tool does the rest. 🚀

---

**Pro Tip**: Run option 4 (Show Paths) anytime to see where all your files are!

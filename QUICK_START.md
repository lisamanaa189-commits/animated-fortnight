# 🚀 QUICK START - PAK Manager

## 🎯 What You Got

A complete **interactive tool** for modding Unreal Engine games!

## ⚡ Start Using It NOW

### Step 1: Run the Tool

```bash
python3 pak_manager.py
```

### Step 2: What You'll See

```
============================================================
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

## 📦 The 4 Folders Created

| Folder | Purpose | You Do |
|--------|---------|--------|
| **Original pak file/** | Source PAK location | **Put your .pak file here** |
| **extracted data-blocks/** | Extracted game files | Don't touch (read-only) |
| **edited game assets here/** | Your edited files | **Put edited files here** |
| **repacked pak file with edited data/** | Output PAK | Take your new PAK from here |

## 🎮 Complete Modding Process (3 Steps)

### 1️⃣ Extract the PAK

```
1. Place YourGame.pak in "Original pak file/" folder
2. Run: python3 pak_manager.py
3. Choose option 1 (Unpack OBB)
4. Wait for extraction to complete
```

### 2️⃣ Edit Your Files

```
1. Go to "extracted data-blocks/" folder
2. Find the file you want to edit (e.g., Content/Textures/Logo.png)
3. Copy it to "edited game assets here/" (same folder structure!)
4. Edit it with your tools (Photoshop, etc.)
```

**IMPORTANT**: Keep the same folder structure!
```
extracted data-blocks/
  └── Content/Textures/Logo.png

↓ COPY TO ↓

edited game assets here/
  └── Content/Textures/Logo.png  ← Edit this!
```

### 3️⃣ Repack & Use

```
1. Run: python3 pak_manager.py
2. Choose option 3 (Repack OBB)
3. Find your new PAK in "repacked pak file with edited data/"
4. Backup original game PAK
5. Replace with your repacked PAK
6. Play the game! 🎉
```

## 🎯 Menu Options Quick Reference

| Option | What It Does | When to Use |
|--------|--------------|-------------|
| **1. Unpack OBB** | Extracts PAK file | First step - extract game files |
| **2. Clear Output** | Deletes extracted/repacked files | Start fresh, free up space |
| **3. Repack OBB** | Creates new PAK with edits | After editing files |
| **4. Show Paths** | Shows folder locations | Check where files are |
| **5. Exit** | Quit the program | When done |

## ⚠️ Important Rules

### ✅ DO:
- Keep exact same filenames
- Maintain folder structure
- Backup original PAK files
- Test with small edits first

### ❌ DON'T:
- Rename files
- Change folder structure  
- Edit files in "extracted data-blocks/" directly
- Use encrypted PAK files (not supported)

## 💡 Example: Texture Modding

Let's mod a character texture!

**1. Unpack:**
```bash
$ python3 pak_manager.py
# Choose option 1
# Wait for: ✓ UNPACKING COMPLETE!
```

**2. Find & Copy:**
```bash
$ cd "extracted data-blocks/Content/Textures"
$ ls
Character_Diffuse.uasset  Character_Normal.uasset  Logo.png

$ mkdir -p "../../../edited game assets here/Content/Textures"
$ cp Logo.png "../../../edited game assets here/Content/Textures/"
```

**3. Edit:**
- Open `edited game assets here/Content/Textures/Logo.png` in Photoshop
- Make your changes
- Save (keep same filename!)

**4. Repack:**
```bash
$ python3 pak_manager.py
# Choose option 3
# Wait for: ✓ REPACKING COMPLETE!
```

**5. Use:**
```bash
$ cd "repacked pak file with edited data"
$ ls
repacked_YourGame.pak

# Copy this to your game folder!
```

## 🔍 Troubleshooting

### "No PAK file found!"
→ Put your .pak file in "Original pak file/" folder

### "Please unpack first!"
→ Run option 1 (Unpack) before option 3 (Repack)

### "No edited files found"
→ Make sure edited files are in "edited game assets here/" with correct folder structure

### "PAK is encrypted!"
→ This tool only works with **unencrypted** PAK files (sorry!)

### Repacked PAK doesn't work
→ Check filename matches original
→ Some games don't allow modded PAKs
→ Check game modding forums

## 📚 More Help

- **Full Documentation**: See `PAK_MANAGER_README.md`
- **PAK Extractor**: See `README.md`
- **Usage Guide**: See `USAGE_GUIDE.md`

## 🎊 You're Ready!

Just run:
```bash
python3 pak_manager.py
```

And start modding! 🚀

---

**Quick Tips:**
- Press Enter at menu to use default option (1)
- Tool auto-detects PAK files in "Original pak file/" folder
- Repacked PAKs are larger (uncompressed) - this is normal
- Always backup original PAK files!

**Happy Modding! 🎮✨**

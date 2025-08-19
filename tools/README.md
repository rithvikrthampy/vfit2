# Tools Directory

This directory contains external tools and dependencies needed for the virtual try-on system.

## Required Tools

### Blender
The system requires Blender for 3D rendering. 

**Option 1: Install Blender to this directory**
1. Download Blender from https://www.blender.org/download/
2. Extract to `tools/blender/` directory
3. Ensure `blender.exe` is at `tools/blender/blender.exe`

**Option 2: System installation**
The system will automatically detect Blender installed in:
- `C:\Program Files\Blender Foundation\Blender\blender.exe`
- `C:\Program Files (x86)\Blender Foundation\Blender\blender.exe`
- Or any location in your system PATH

**Option 3: Environment variable**
Set `BLENDER_BIN` environment variable to point to your Blender executable.

## Directory Structure
```
tools/
├── blender/           # Blender installation (optional)
│   ├── blender.exe    # Blender executable
│   └── ...            # Other Blender files
└── README.md          # This file
```
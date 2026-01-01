# Pixel Perfect - C# WPF Version

A professional pixel art editor built with C# and WPF (.NET 8).

## Prerequisites

- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- Visual Studio 2022 or VS Code with C# extension

## Building & Running

```bash
# Navigate to project directory
cd Pix_Perf_C_WPF

# Restore dependencies
dotnet restore

# Build
dotnet build

# Run
dotnet run
```

## Project Structure

```
Pix_Perf_C_WPF/
├── Core/                    # Core data models
│   ├── PixelColor.cs       # RGBA color struct
│   ├── Layer.cs            # Layer with pixel storage
│   ├── PixelCanvas.cs      # Canvas with layer management
│   └── Tools.cs            # Brush, Eraser, Fill, Eyedropper
├── ViewModels/
│   └── MainViewModel.cs    # MVVM ViewModel with commands
├── Views/
│   ├── MainWindow.xaml     # Main UI layout
│   └── MainWindow.xaml.cs  # Mouse event handling
├── Themes/
│   └── DarkTheme.xaml      # Dark theme styling
├── App.xaml                # Application entry point
└── PixelPerfect.csproj     # .NET project file
```

## Architecture

- **MVVM Pattern**: Clean separation of concerns using CommunityToolkit.Mvvm
- **WriteableBitmap**: High-performance pixel rendering
- **Layer System**: Supports multiple layers with visibility and opacity
- **Tool System**: Extensible tool interface (ITool)

## Current Features

- ✅ Brush tool with variable size
- ✅ Eraser tool
- ✅ Fill tool (scanline optimized)
- ✅ Eyedropper tool
- ✅ Layer system with visibility toggle
- ✅ Zoom control
- ✅ Dark theme UI

## Roadmap

### Phase 1 - Core Features
- [ ] Undo/Redo system
- [ ] Selection tool
- [ ] Move tool
- [ ] Color picker panel
- [ ] Save/Load (PNG export)

### Phase 2 - Advanced Features
- [ ] Shape tools (Line, Rectangle, Circle)
- [ ] Symmetry modes
- [ ] Color palettes
- [ ] Animation timeline
- [ ] Edge tool

### Phase 3 - Polish
- [ ] Keyboard shortcuts
- [ ] Grid overlay
- [ ] Pan tool
- [ ] Theme customization
- [ ] Recent colors

## License

Copyright © 2024-2026 Diamond Clad Studios - All Rights Reserved

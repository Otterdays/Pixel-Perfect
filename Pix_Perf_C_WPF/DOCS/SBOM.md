# Pixel Perfect C# WPF — Software Bill of Materials (SBOM)

**Last Updated**: February 23, 2026  
**Project Version**: 0.1.0  
**Status**: Initial Scaffold

---

## Project Information

| Field | Value |
|-------|-------|
| **Project Name** | Pixel Perfect — C# WPF Version |
| **Version** | 0.1.0 |
| **Created** | February 2026 |
| **Platform** | Windows (.NET 8 WPF) |
| **Language** | C# 12 |
| **Runtime** | .NET 8.0-windows |

---

## Runtime Environment

| Component | Version | Notes |
|-----------|---------|-------|
| **.NET SDK** | 8.0+ | Required |
| **C#** | 12 (implicit with .NET 8) | |
| **WPF** | Included with .NET 8-windows | |
| **Target Framework** | `net8.0-windows` | Windows-only target |
| **Nullable** | Enabled | Full nullable reference types |

---

## NuGet Dependencies

### Production Dependencies

| Package | Version | License | Purpose | Status |
|---------|---------|---------|---------|--------|
| **CommunityToolkit.Mvvm** | 8.2.2 | MIT | MVVM base classes (`ObservableObject`, `RelayCommand`, `[ObservableProperty]`) | ✅ Active |

### No Other Runtime Dependencies
Unlike the Python version which required Pillow, numpy, and customtkinter, the WPF version leverages:
- **WPF DrawingBrush** — Checkerboard transparency pattern
- **WPF WriteableBitmap** — Direct pixel manipulation (replaces Pillow)
- **WPF LayoutTransform** — Zoom scaling (replaces pygame canvas scaling)

---

## Installation

### Prerequisites
```powershell
# Install .NET 8 SDK from:
# https://dotnet.microsoft.com/download/dotnet/8.0

# Verify installation
dotnet --version  # Should show 8.0.x
```

### Restore NuGet Packages
```powershell
cd Pix_Perf_C_WPF
dotnet restore
```

### Build & Run
```powershell
dotnet build
dotnet run
```

---

## Security Status

| Check | Status | Notes |
|-------|--------|-------|
| Known CVEs | ✅ None | CommunityToolkit.Mvvm 8.2.2 — no known vulnerabilities |
| External network calls | ✅ None | Fully offline, local file operations only |
| Trusted source | ✅ Yes | NuGet.org, Microsoft-maintained package |
| HSTS/TLS concerns | ✅ N/A | Desktop app, no network stack |

---

## License Compliance

| Package | License | Compatible |
|---------|---------|-----------|
| CommunityToolkit.Mvvm | MIT | ✅ Yes |
| .NET Runtime (WPF) | MIT | ✅ Yes |
| Project itself | Proprietary © Diamond Clad Studios | — |

---

## Planned Future Dependencies

| Package | Purpose | When | Risk |
|---------|---------|------|------|
| None planned yet | — | — | Low |

> **Note**: The goal is to keep dependencies minimal. WPF provides all needed rendering primitives. If image import is needed, `System.Drawing` (included in .NET 8) or the built-in `BitmapDecoder`/`BitmapEncoder` classes handle PNG/GIF without third-party packages.

---

## Comparison to Python SBOM

| Python Version | C# WPF Version |
|---------------|----------------|
| customtkinter ≥5.2.0 | WPF (built into .NET) |
| Pillow ≥10.0.0 | `System.Windows.Media.Imaging` (built-in) |
| numpy ≥1.24.0 | Native arrays + LINQ |
| PyInstaller ≥6.0.0 | `dotnet publish` (built-in) |
| **4 packages** | **1 package** |

---

## Update History

| Date | Change |
|------|--------|
| 2026-02-23 | Initial SBOM created — CommunityToolkit.Mvvm 8.2.2 added |

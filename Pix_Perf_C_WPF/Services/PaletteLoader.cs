using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.Json;
using PixelPerfect.Core;

namespace PixelPerfect.Services;

/// <summary>
/// Loads color palettes from JSON files (assets/palettes/*.json)
/// </summary>
public static class PaletteLoader
{
    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true,
        ReadCommentHandling = JsonCommentHandling.Skip,
        AllowTrailingCommas = true
    };

    /// <summary>One section within a palette (title + color list).</summary>
    public sealed class PaletteSection
    {
        public string Title { get; }
        public IReadOnlyList<PixelColor> Colors { get; }

        public PaletteSection(string title, IReadOnlyList<PixelColor> colors)
        {
            Title = title ?? string.Empty;
            Colors = colors ?? Array.Empty<PixelColor>();
        }
    }

    /// <summary>
    /// Palette entry with name, flat colors, and optional sections for UI grouping.
    /// </summary>
    public sealed class PaletteEntry
    {
        public string Name { get; }
        public IReadOnlyList<PixelColor> Colors { get; }
        public IReadOnlyList<PaletteSection> Sections { get; }

        public PaletteEntry(string name, IReadOnlyList<PixelColor> colors)
        {
            Name = name;
            Colors = colors ?? Array.Empty<PixelColor>();
            Sections = new List<PaletteSection> { new PaletteSection("Colors", Colors) };
        }

        public PaletteEntry(string name, IReadOnlyList<PaletteSection> sections)
        {
            Name = name;
            var list = new List<PixelColor>();
            foreach (var s in sections ?? Array.Empty<PaletteSection>())
                list.AddRange(s.Colors);
            Colors = list;
            Sections = sections ?? Array.Empty<PaletteSection>();
        }
    }

    /// <summary>
    /// Gets the palettes folder path (next to executable, or fallback to project assets)
    /// </summary>
    public static string GetPalettesFolder()
    {
        var exeDir = Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location);
        if (!string.IsNullOrEmpty(exeDir))
        {
            var assetsPath = Path.Combine(exeDir, "assets", "palettes");
            if (Directory.Exists(assetsPath))
                return assetsPath;
        }
        // Fallback: project root assets (for development)
        var projectRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", ".."));
        return Path.Combine(projectRoot, "assets", "palettes");
    }

    /// <summary>
    /// Loads all palettes from the palettes folder. Includes built-in SNES Classic first.
    /// </summary>
    public static IReadOnlyList<PaletteEntry> LoadAll()
    {
        var result = new List<PaletteEntry>
        {
            new("SNES Classic", Palette.SnesClassic.ToList())
        };

        var folder = GetPalettesFolder();
        if (!Directory.Exists(folder)) return result;

        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase) { "SNES Classic" };
        foreach (var file in Directory.EnumerateFiles(folder, "*.json"))
        {
            try
            {
                var entry = LoadFromFile(file);
                if (entry != null && entry.Colors.Count > 0 && seen.Add(entry.Name))
                    result.Add(entry);
            }
            catch
            {
                // Skip invalid palettes
            }
        }

        return result;
    }

    /// <summary>
    /// Loads a single palette from a JSON file.
    /// Format: {"name":"...","colors":[[r,g,b,a],...]} or
    /// {"name":"...","sections":[{"title":"Section Name","colors":[[r,g,b,a],...]},...]}
    /// </summary>
    public static PaletteEntry? LoadFromFile(string filePath)
    {
        var json = File.ReadAllText(filePath);
        using var doc = JsonDocument.Parse(json);
        var root = doc.RootElement;

        var name = root.TryGetProperty("name", out var nameProp)
            ? nameProp.GetString() ?? Path.GetFileNameWithoutExtension(filePath)
            : Path.GetFileNameWithoutExtension(filePath);

        if (root.TryGetProperty("sections", out var sectionsProp))
        {
            var sections = new List<PaletteSection>();
            foreach (var secEl in sectionsProp.EnumerateArray())
            {
                var title = secEl.TryGetProperty("title", out var t) ? t.GetString() ?? "Colors" : "Colors";
                if (!secEl.TryGetProperty("colors", out var secColors))
                    continue;
                var colors = ParseColorArray(secColors);
                if (colors.Count > 0)
                    sections.Add(new PaletteSection(title, colors));
            }
            if (sections.Count > 0)
                return new PaletteEntry(name, sections);
        }

        if (!root.TryGetProperty("colors", out var colorsProp))
            return null;

        var flat = ParseColorArray(colorsProp);
        return flat.Count > 0 ? new PaletteEntry(name, flat) : null;
    }

    private static List<PixelColor> ParseColorArray(JsonElement colorsProp)
    {
        var colors = new List<PixelColor>();
        foreach (var arr in colorsProp.EnumerateArray())
        {
            var parts = arr.EnumerateArray().Select(e => e.GetInt32()).ToArray();
            if (parts.Length >= 3)
            {
                byte a = (byte)(parts.Length >= 4 ? Math.Clamp(parts[3], 0, 255) : 255);
                colors.Add(new PixelColor(
                    (byte)Math.Clamp(parts[0], 0, 255),
                    (byte)Math.Clamp(parts[1], 0, 255),
                    (byte)Math.Clamp(parts[2], 0, 255),
                    a));
            }
        }
        return colors;
    }
}

using System;
using System.Collections.Generic;
using System.Windows;

namespace PixelPerfect.Services;

/// <summary>
/// Manages application themes. Swaps merged ResourceDictionaries for runtime theme switching.
/// </summary>
public class ThemeManager
{
    private const int ThemeDictionaryIndex = 0;
    private readonly Dictionary<string, string> _themePaths = new(StringComparer.OrdinalIgnoreCase)
    {
        ["Dark"] = "Themes/DarkTheme.xaml",
        ["Basic Grey"] = "Themes/BasicGreyTheme.xaml",
        ["Light"] = "Themes/LightTheme.xaml",
        ["Gemini"] = "Themes/GeminiTheme.xaml",
        ["Claude"] = "Themes/ClaudeTheme.xaml"
    };

    private static readonly string[] ThemeOrder = { "Dark", "Basic Grey", "Light", "Gemini", "Claude" };
    public IReadOnlyList<string> ThemeNames { get; } = ThemeOrder;
    public string CurrentThemeName { get; private set; } = "Dark";

    public ThemeManager()
    {
    }

    /// <summary>
    /// Applies a theme by name. Replaces the theme ResourceDictionary.
    /// </summary>
    public void ApplyTheme(string name)
    {
        if (string.IsNullOrEmpty(name) || !_themePaths.TryGetValue(name, out var path))
            return;

        var app = Application.Current;
        if (app == null || app.Resources?.MergedDictionaries == null || app.Resources.MergedDictionaries.Count <= ThemeDictionaryIndex)
            return;

        try
        {
            var uri = new Uri($"pack://application:,,,/PixelPerfect;component/{path}", UriKind.Absolute);
            var dict = new ResourceDictionary { Source = uri };
            app.Resources.MergedDictionaries[ThemeDictionaryIndex] = dict;
            CurrentThemeName = name;
            ThemeChanged?.Invoke(this, name);
        }
        catch (Exception)
        {
            // Keep current theme on load failure
        }
    }

    public event Action<ThemeManager, string>? ThemeChanged;
}

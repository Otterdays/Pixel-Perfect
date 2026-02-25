using System;
using System.Collections.Generic;
using System.Windows;

namespace PixelPerfect.Services;

/// <summary>
/// Manages runtime theme switching for the WPF application.
/// Swaps the theme ResourceDictionary in Application.Resources.
/// </summary>
public static class ThemeService
{
    private const string ThemeBasePath = "pack://application:,,,/PixelPerfect;component/Themes/";

    public static IReadOnlyList<string> ThemeNames { get; } = new[]
    {
        "Dark",
        "Light",
        "Nord",
        "Dracula",
        "Retro",
        "Catppuccin"
    };

    private static readonly Dictionary<string, string> ThemeFileMap = new()
    {
        ["Dark"] = "DarkTheme.xaml",
        ["Light"] = "LightTheme.xaml",
        ["Nord"] = "NordTheme.xaml",
        ["Dracula"] = "DraculaTheme.xaml",
        ["Retro"] = "RetroTheme.xaml",
        ["Catppuccin"] = "CatppuccinTheme.xaml"
    };

    private static string _currentTheme = "Dark";

    /// <summary>
    /// Gets the currently active theme name.
    /// </summary>
    public static string CurrentTheme => _currentTheme;

    /// <summary>
    /// Raised when the theme has been changed. Subscribe to refresh UI that caches resources.
    /// </summary>
    public static event Action<string>? ThemeChanged;

    /// <summary>
    /// Applies the specified theme by swapping the theme ResourceDictionary.
    /// </summary>
    public static void ApplyTheme(string themeName)
    {
        if (!ThemeFileMap.TryGetValue(themeName, out var fileName))
            return;

        var app = Application.Current;
        if (app == null) return;

        var merged = app.Resources.MergedDictionaries;
        var themeUri = new Uri(ThemeBasePath + fileName, UriKind.Absolute);

        // Remove existing theme dictionaries (those from Themes/ folder)
        for (int i = merged.Count - 1; i >= 0; i--)
        {
            var dict = merged[i];
            if (dict.Source?.ToString().Contains("/Themes/") == true)
                merged.RemoveAt(i);
        }

        var newTheme = new ResourceDictionary { Source = themeUri };
        merged.Add(newTheme);

        _currentTheme = themeName;
        ThemeChanged?.Invoke(themeName);
    }
}

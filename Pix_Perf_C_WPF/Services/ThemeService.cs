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
    private const string CommonStylesFileName = "CommonStyles.xaml";

    public static IReadOnlyList<string> ThemeNames { get; } = new[]
    {
        "Dark",
        "Light",
        "Nord",
        "Dracula",
        "Retro",
        "Catppuccin",
        "Gruvbox",
        "Basic Grey",
        "Gemini",
        "Claude",
        "Tokyo Night",
        "Solarized Dark",
        "Solarized Light",
        "Rose Pine",
        "Monokai",
        "One Dark"
    };

    private static readonly Dictionary<string, string> ThemeFileMap = new()
    {
        ["Dark"] = "DarkTheme.xaml",
        ["Light"] = "LightTheme.xaml",
        ["Nord"] = "NordTheme.xaml",
        ["Dracula"] = "DraculaTheme.xaml",
        ["Retro"] = "RetroTheme.xaml",
        ["Catppuccin"] = "CatppuccinTheme.xaml",
        ["Gruvbox"] = "GruvboxTheme.xaml",
        ["Basic Grey"] = "BasicGreyTheme.xaml",
        ["Gemini"] = "GeminiTheme.xaml",
        ["Claude"] = "ClaudeTheme.xaml",
        ["Tokyo Night"] = "TokyoNightTheme.xaml",
        ["Solarized Dark"] = "SolarizedDarkTheme.xaml",
        ["Solarized Light"] = "SolarizedLightTheme.xaml",
        ["Rose Pine"] = "RosePineTheme.xaml",
        ["Monokai"] = "MonokaiTheme.xaml",
        ["One Dark"] = "OneDarkTheme.xaml"
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

    private static bool IsThemeDictionary(ResourceDictionary dict)
    {
        var src = dict.Source?.ToString();
        return src != null && src.Contains("/Themes/") && src.EndsWith("Theme.xaml", StringComparison.OrdinalIgnoreCase);
    }

    private static bool IsCommonStylesDictionary(ResourceDictionary dict)
    {
        var src = dict.Source?.ToString();
        return src != null && src.Contains("/Themes/") && src.EndsWith(CommonStylesFileName, StringComparison.OrdinalIgnoreCase);
    }

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

        // Remove existing theme dictionaries but keep CommonStyles.xaml.
        for (int i = merged.Count - 1; i >= 0; i--)
        {
            var dict = merged[i];
            if (IsThemeDictionary(dict))
                merged.RemoveAt(i);
        }

        // Ensure the theme dictionary is first.
        var themeUri = new Uri(ThemeBasePath + fileName, UriKind.Absolute);
        var newTheme = new ResourceDictionary { Source = themeUri };
        merged.Insert(0, newTheme);

        // Ensure CommonStyles.xaml exists and is last so it can consistently override/define shared styles.
        ResourceDictionary? common = null;
        for (int i = merged.Count - 1; i >= 0; i--)
        {
            if (IsCommonStylesDictionary(merged[i]))
            {
                common = merged[i];
                merged.RemoveAt(i);
                break;
            }
        }

        common ??= new ResourceDictionary { Source = new Uri(ThemeBasePath + CommonStylesFileName, UriKind.Absolute) };
        merged.Add(common);

        _currentTheme = themeName;
        ThemeChanged?.Invoke(themeName);
    }
}

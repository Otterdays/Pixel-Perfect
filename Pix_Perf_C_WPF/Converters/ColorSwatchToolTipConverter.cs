using System;
using System.Globalization;
using System.Windows.Data;
using PixelPerfect.Core;

namespace PixelPerfect.Converters;

/// <summary>
/// Builds structured tooltip content (title, short desc, nitty gritty) for palette color swatches.
/// </summary>
public sealed class ColorSwatchToolTipConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is not PixelColor pc)
            return new ColorSwatchToolTipContent("#------", "—", "—");

        string hex = $"#{pc.R:X2}{pc.G:X2}{pc.B:X2}";
        if (pc.A < 255) hex += pc.A.ToString("X2");
        string title = hex;
        string shortDesc = pc.A < 255
            ? "Click to use this color. Semi-transparent."
            : "Click to use this color for drawing.";
        string details = $"R: {pc.R}  G: {pc.G}  B: {pc.B}  A: {pc.A}";
        return new ColorSwatchToolTipContent(title, shortDesc, details);
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        => throw new NotImplementedException();
}

/// <summary>Structured tooltip content (title, short desc, details). Used for palette swatches and tools.</summary>
public sealed class ColorSwatchToolTipContent
{
    public string Title { get; set; } = string.Empty;
    public string ShortDescription { get; set; } = string.Empty;
    public string Details { get; set; } = string.Empty;

    public ColorSwatchToolTipContent() { }

    public ColorSwatchToolTipContent(string title, string shortDescription, string details)
    {
        Title = title ?? string.Empty;
        ShortDescription = shortDescription ?? string.Empty;
        Details = details ?? string.Empty;
    }
}

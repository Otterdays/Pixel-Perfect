using System.Collections.Generic;

namespace PixelPerfect.Core;

/// <summary>
/// Color palette for the color picker panel
/// </summary>
public static class Palette
{
    /// <summary>
    /// SNES Classic 16-color palette (RGB values, alpha 255)
    /// </summary>
    public static IReadOnlyList<PixelColor> SnesClassic { get; } = new[]
    {
        new PixelColor(0, 0, 0, 255),
        new PixelColor(255, 255, 255, 255),
        new PixelColor(128, 128, 128, 255),
        new PixelColor(255, 0, 0, 255),
        new PixelColor(0, 255, 0, 255),
        new PixelColor(0, 0, 255, 255),
        new PixelColor(255, 255, 0, 255),
        new PixelColor(255, 0, 255, 255),
        new PixelColor(0, 255, 255, 255),
        new PixelColor(128, 64, 0, 255),
        new PixelColor(255, 128, 0, 255),
        new PixelColor(128, 0, 128, 255),
        new PixelColor(0, 128, 0, 255),
        new PixelColor(0, 0, 128, 255),
        new PixelColor(128, 128, 0, 255),
        new PixelColor(192, 192, 192, 255)
    };
}

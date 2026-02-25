namespace PixelPerfect.Core;

/// <summary>
/// Represents a pixel with RGBA color values
/// </summary>
public readonly struct PixelColor
{
    public byte R { get; }
    public byte G { get; }
    public byte B { get; }
    public byte A { get; }
    
    public PixelColor(byte r, byte g, byte b, byte a = 255)
    {
        R = r;
        G = g;
        B = b;
        A = a;
    }
    
    public static PixelColor Transparent => new(0, 0, 0, 0);
    public static PixelColor Black => new(0, 0, 0, 255);
    public static PixelColor White => new(255, 255, 255, 255);
    
    public bool IsTransparent => A == 0;
    
    public uint ToUInt32() => (uint)((A << 24) | (R << 16) | (G << 8) | B);
    
    public static PixelColor FromUInt32(uint value) => new(
        (byte)((value >> 16) & 0xFF),
        (byte)((value >> 8) & 0xFF),
        (byte)(value & 0xFF),
        (byte)((value >> 24) & 0xFF)
    );
    
    public override bool Equals(object? obj) => obj is PixelColor other && this == other;
    public override int GetHashCode() => ToUInt32().GetHashCode();
    
    public static bool operator ==(PixelColor a, PixelColor b) =>
        a.R == b.R && a.G == b.G && a.B == b.B && a.A == b.A;
    
    public static bool operator !=(PixelColor a, PixelColor b) => !(a == b);

    /// <summary>Alpha-blends top over bottom (Porter-Duff Over).</summary>
    public static PixelColor BlendOver(PixelColor top, PixelColor bottom)
    {
        if (top.A == 0) return bottom;
        if (top.A == 255) return top;
        double sa = top.A / 255.0, sb = bottom.A / 255.0;
        double outA = sa + sb * (1.0 - sa);
        if (outA <= 0) return Transparent;
        double invOutA = 1.0 / outA;
        byte r = (byte)((top.R * sa + bottom.R * sb * (1.0 - sa)) * invOutA);
        byte g = (byte)((top.G * sa + bottom.G * sb * (1.0 - sa)) * invOutA);
        byte b = (byte)((top.B * sa + bottom.B * sb * (1.0 - sa)) * invOutA);
        byte a = (byte)(outA * 255);
        return new PixelColor(r, g, b, a);
    }
}

namespace PixelPerfect.Core;

/// <summary>
/// Represents a single layer in the canvas
/// </summary>
public class Layer
{
    private readonly PixelColor[,] _pixels;
    
    public string Name { get; set; }
    public int Width { get; }
    public int Height { get; }
    public bool IsVisible { get; set; } = true;
    public double Opacity { get; set; } = 1.0;
    public bool IsLocked { get; set; } = false;
    
    public Layer(string name, int width, int height)
    {
        Name = name;
        Width = width;
        Height = height;
        _pixels = new PixelColor[height, width];
        
        // Initialize with transparent pixels
        Clear();
    }
    
    public PixelColor GetPixel(int x, int y)
    {
        if (IsInBounds(x, y))
            return _pixels[y, x];
        return PixelColor.Transparent;
    }
    
    public void SetPixel(int x, int y, PixelColor color)
    {
        if (IsInBounds(x, y) && !IsLocked)
            _pixels[y, x] = color;
    }
    
    public bool IsInBounds(int x, int y) =>
        x >= 0 && x < Width && y >= 0 && y < Height;
    
    public void Clear()
    {
        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                _pixels[y, x] = PixelColor.Transparent;
    }
    
    /// <summary>
    /// Creates a deep copy of this layer
    /// </summary>
    public Layer Clone()
    {
        var clone = new Layer(Name + " Copy", Width, Height)
        {
            IsVisible = IsVisible,
            Opacity = Opacity,
            IsLocked = IsLocked
        };
        
        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                clone._pixels[y, x] = _pixels[y, x];
        
        return clone;
    }
    
    /// <summary>
    /// Gets the raw pixel array for fast rendering
    /// </summary>
    public PixelColor[,] GetPixelArray() => _pixels;
}

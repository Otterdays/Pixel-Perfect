using System;
using System.Collections.ObjectModel;

namespace PixelPerfect.Core;

/// <summary>
/// Manages the canvas state including layers and dimensions
/// </summary>
public class PixelCanvas
{
    public int Width { get; }
    public int Height { get; }
    public ObservableCollection<Layer> Layers { get; } = new();
    public int ActiveLayerIndex { get; set; } = 0;
    
    public Layer? ActiveLayer => 
        ActiveLayerIndex >= 0 && ActiveLayerIndex < Layers.Count 
            ? Layers[ActiveLayerIndex] 
            : null;
    
    public PixelCanvas(int width, int height)
    {
        Width = width;
        Height = height;
        
        // Create default layer
        AddLayer("Layer 1");
    }
    
    public Layer AddLayer(string name)
    {
        var layer = new Layer(name, Width, Height);
        Layers.Add(layer);
        ActiveLayerIndex = Layers.Count - 1;
        return layer;
    }
    
    public void RemoveLayer(int index)
    {
        if (Layers.Count > 1 && index >= 0 && index < Layers.Count)
        {
            Layers.RemoveAt(index);
            if (ActiveLayerIndex >= Layers.Count)
                ActiveLayerIndex = Layers.Count - 1;
        }
    }
    
    public void MoveLayerUp(int index)
    {
        if (index > 0 && index < Layers.Count)
        {
            (Layers[index], Layers[index - 1]) = (Layers[index - 1], Layers[index]);
            ActiveLayerIndex = index - 1;
        }
    }
    
    public void MoveLayerDown(int index)
    {
        if (index >= 0 && index < Layers.Count - 1)
        {
            (Layers[index], Layers[index + 1]) = (Layers[index + 1], Layers[index]);
            ActiveLayerIndex = index + 1;
        }
    }
    
    /// <summary>
    /// Flattens all visible layers into a single pixel array for rendering
    /// </summary>
    public PixelColor[,] FlattenLayers()
    {
        var result = new PixelColor[Height, Width];
        
        // Initialize with transparent
        for (int y = 0; y < Height; y++)
            for (int x = 0; x < Width; x++)
                result[y, x] = PixelColor.Transparent;
        
        // Blend layers from bottom to top
        foreach (var layer in Layers)
        {
            if (!layer.IsVisible) continue;
            
            var pixels = layer.GetPixelArray();
            var opacity = layer.Opacity;
            
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    var src = pixels[y, x];
                    if (src.IsTransparent) continue;
                    
                    var dst = result[y, x];
                    var srcAlpha = src.A * opacity / 255.0;
                    
                    if (srcAlpha >= 1.0 || dst.IsTransparent)
                    {
                        result[y, x] = new PixelColor(src.R, src.G, src.B, (byte)(srcAlpha * 255));
                    }
                    else
                    {
                        // Alpha blend
                        var invAlpha = 1.0 - srcAlpha;
                        result[y, x] = new PixelColor(
                            (byte)(src.R * srcAlpha + dst.R * invAlpha),
                            (byte)(src.G * srcAlpha + dst.G * invAlpha),
                            (byte)(src.B * srcAlpha + dst.B * invAlpha),
                            (byte)Math.Min(255, dst.A + srcAlpha * 255)
                        );
                    }
                }
            }
        }
        
        return result;
    }
}

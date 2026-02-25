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
    
    public event System.Action<Layer, int, int, PixelColor, PixelColor>? PixelChanged;
    
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
        layer.PixelChanged += (l, x, y, oldC, newC) => PixelChanged?.Invoke(l, x, y, oldC, newC);
        Layers.Add(layer);
        ActiveLayerIndex = Layers.Count - 1;
        return layer;
    }

    /// <summary>
    /// Inserts a layer at the given index. Used for duplicate.
    /// </summary>
    public void InsertLayer(int index, Layer layer)
    {
        layer.PixelChanged += (l, x, y, oldC, newC) => PixelChanged?.Invoke(l, x, y, oldC, newC);
        Layers.Insert(index, layer);
        ActiveLayerIndex = index;
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
    /// Merges the active layer into the layer below (alpha blend), then removes the active layer.
    /// </summary>
    /// <returns>True if merge was performed.</returns>
    public bool MergeDown(int index)
    {
        if (index <= 0 || index >= Layers.Count) return false;
        var top = Layers[index];
        var bottom = Layers[index - 1];
        if (bottom.IsLocked) return false;

        double opacity = top.Opacity;
        for (int y = 0; y < Height; y++)
        {
            for (int x = 0; x < Width; x++)
            {
                var src = top.GetPixel(x, y);
                if (src.IsTransparent) continue;
                var srcBlended = opacity < 1.0 ? new PixelColor(src.R, src.G, src.B, (byte)(src.A * opacity)) : src;
                var dst = bottom.GetPixel(x, y);
                var blended = PixelColor.BlendOver(srcBlended, dst);
                bottom.SetPixel(x, y, blended);
            }
        }
        RemoveLayer(index);
        return true;
    }
    
    /// <summary>
    /// Returns the composited color at (x,y) from all visible layers. Returns Transparent if out of bounds.
    /// </summary>
    public PixelColor GetCompositePixel(int x, int y)
    {
        if (x < 0 || x >= Width || y < 0 || y >= Height) return PixelColor.Transparent;
        PixelColor result = PixelColor.Transparent;
        foreach (var layer in Layers)
        {
            if (!layer.IsVisible) continue;
            var src = layer.GetPixel(x, y);
            if (src.IsTransparent) continue;
            result = PixelColor.BlendOver(
                new PixelColor(src.R, src.G, src.B, (byte)(src.A * layer.Opacity)),
                result);
        }
        return result;
    }

    /// <summary>
    /// Flattens all visible layers directly into a BGRA byte array (zero allocation)
    /// </summary>
    public void FlattenToBuffer(byte[] buffer)
    {
        Array.Clear(buffer, 0, buffer.Length);
        
        foreach (var layer in Layers)
        {
            if (!layer.IsVisible) continue;
            
            var pixels = layer.GetPixelArray();
            var opacity = layer.Opacity;
            
            int offset = 0;
            for (int y = 0; y < Height; y++)
            {
                for (int x = 0; x < Width; x++)
                {
                    var src = pixels[y, x];
                    if (src.IsTransparent) 
                    {
                        offset += 4;
                        continue;
                    }
                    
                    var srcAlpha = src.A * opacity / 255.0;
                    var dstA = buffer[offset + 3];
                    
                    if (srcAlpha >= 1.0 || dstA == 0)
                    {
                        buffer[offset] = src.B;
                        buffer[offset + 1] = src.G;
                        buffer[offset + 2] = src.R;
                        buffer[offset + 3] = (byte)(srcAlpha * 255);
                    }
                    else
                    {
                        // Alpha blend
                        var invAlpha = 1.0 - srcAlpha;
                        buffer[offset] = (byte)(src.B * srcAlpha + buffer[offset] * invAlpha);
                        buffer[offset + 1] = (byte)(src.G * srcAlpha + buffer[offset + 1] * invAlpha);
                        buffer[offset + 2] = (byte)(src.R * srcAlpha + buffer[offset + 2] * invAlpha);
                        buffer[offset + 3] = (byte)Math.Min(255, dstA + srcAlpha * 255);
                    }
                    offset += 4;
                }
            }
        }
    }
}

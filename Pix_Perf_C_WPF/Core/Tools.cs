using System;
using System.Collections.Generic;

namespace PixelPerfect.Core;

/// <summary>
/// Available drawing tools
/// </summary>
public enum ToolType
{
    Brush,
    Eraser,
    Fill,
    Eyedropper,
    Selection,
    Move,
    Line,
    Rectangle,
    Circle,
    Pan,
    Zoom
}

/// <summary>
/// Base interface for all tools
/// </summary>
public interface ITool
{
    ToolType Type { get; }
    string Name { get; }
    
    void OnMouseDown(Layer layer, int x, int y, PixelColor color);
    void OnMouseMove(Layer layer, int x, int y, PixelColor color);
    void OnMouseUp(Layer layer, int x, int y, PixelColor color);
}

/// <summary>
/// Brush tool for drawing pixels
/// </summary>
public class BrushTool : ITool
{
    public ToolType Type => ToolType.Brush;
    public string Name => "Brush";
    public int Size { get; set; } = 1;
    
    private bool _isDrawing;
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        DrawAt(layer, x, y, color);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isDrawing)
            DrawAt(layer, x, y, color);
    }
    
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = false;
    }
    
    private void DrawAt(Layer layer, int x, int y, PixelColor color)
    {
        if (Size == 1)
        {
            layer.SetPixel(x, y, color);
        }
        else
        {
            int halfSize = Size / 2;
            for (int dy = -halfSize; dy <= halfSize; dy++)
            {
                for (int dx = -halfSize; dx <= halfSize; dx++)
                {
                    layer.SetPixel(x + dx, y + dy, color);
                }
            }
        }
    }
}

/// <summary>
/// Eraser tool for removing pixels
/// </summary>
public class EraserTool : ITool
{
    public ToolType Type => ToolType.Eraser;
    public string Name => "Eraser";
    public int Size { get; set; } = 1;
    
    private bool _isErasing;
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isErasing = true;
        EraseAt(layer, x, y);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isErasing)
            EraseAt(layer, x, y);
    }
    
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isErasing = false;
    }
    
    private void EraseAt(Layer layer, int x, int y)
    {
        if (Size == 1)
        {
            layer.SetPixel(x, y, PixelColor.Transparent);
        }
        else
        {
            int halfSize = Size / 2;
            for (int dy = -halfSize; dy <= halfSize; dy++)
            {
                for (int dx = -halfSize; dx <= halfSize; dx++)
                {
                    layer.SetPixel(x + dx, y + dy, PixelColor.Transparent);
                }
            }
        }
    }
}

/// <summary>
/// Fill tool for flood filling areas
/// </summary>
public class FillTool : ITool
{
    public ToolType Type => ToolType.Fill;
    public string Name => "Fill";
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        if (!layer.IsInBounds(x, y)) return;
        
        var targetColor = layer.GetPixel(x, y);
        if (targetColor == color) return;
        
        FloodFill(layer, x, y, targetColor, color);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color) { }
    
    private void FloodFill(Layer layer, int x, int y, PixelColor target, PixelColor replacement)
    {
        var stack = new Stack<(int x, int y)>();
        stack.Push((x, y));
        
        while (stack.Count > 0)
        {
            var (cx, cy) = stack.Pop();
            
            if (!layer.IsInBounds(cx, cy)) continue;
            if (layer.GetPixel(cx, cy) != target) continue;
            
            // Scanline fill for better performance
            int left = cx;
            int right = cx;
            
            // Find left edge
            while (left > 0 && layer.GetPixel(left - 1, cy) == target)
                left--;
            
            // Find right edge
            while (right < layer.Width - 1 && layer.GetPixel(right + 1, cy) == target)
                right++;
            
            // Fill the line
            for (int i = left; i <= right; i++)
            {
                layer.SetPixel(i, cy, replacement);
                
                // Check above and below
                if (cy > 0 && layer.GetPixel(i, cy - 1) == target)
                    stack.Push((i, cy - 1));
                if (cy < layer.Height - 1 && layer.GetPixel(i, cy + 1) == target)
                    stack.Push((i, cy + 1));
            }
        }
    }
}

/// <summary>
/// Eyedropper tool for picking colors
/// </summary>
public class EyedropperTool : ITool
{
    public ToolType Type => ToolType.Eyedropper;
    public string Name => "Eyedropper";
    
    public event Action<PixelColor>? ColorPicked;
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        if (layer.IsInBounds(x, y))
        {
            var pickedColor = layer.GetPixel(x, y);
            ColorPicked?.Invoke(pickedColor);
        }
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color) { }
}

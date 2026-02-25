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
    Zoom,
    Spray,
    Dither,
    MagicWand,
    Edge,
    Texture
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
/// Interface for tools that support symmetric drawing
/// </summary>
public interface ISymmetricTool
{
    bool SymmetryX { get; set; }
    bool SymmetryY { get; set; }
}

public static class SymmetryExtensions
{
    public static void SetSymmetricPixel(this Layer layer, int x, int y, PixelColor color, bool symX, bool symY)
    {
        layer.SetPixel(x, y, color);
        if (symX) layer.SetPixel(layer.Width - 1 - x, y, color);
        if (symY) layer.SetPixel(x, layer.Height - 1 - y, color);
        if (symX && symY) layer.SetPixel(layer.Width - 1 - x, layer.Height - 1 - y, color);
    }

    public static void SetSymmetricPixelRaw(this Layer layer, int x, int y, PixelColor color, bool symX, bool symY)
    {
        layer.SetPixelRaw(x, y, color);
        if (symX) layer.SetPixelRaw(layer.Width - 1 - x, y, color);
        if (symY) layer.SetPixelRaw(x, layer.Height - 1 - y, color);
        if (symX && symY) layer.SetPixelRaw(layer.Width - 1 - x, layer.Height - 1 - y, color);
    }
    
    public static void SaveSymmetricPixelState(this Layer layer, int x, int y, Dictionary<(int x, int y), PixelColor> saved, bool symX, bool symY)
    {
        void Save(int px, int py)
        {
            if (layer.IsInBounds(px, py) && !saved.ContainsKey((px, py)))
                saved[(px, py)] = layer.GetPixel(px, py);
        }
        Save(x, y);
        if (symX) Save(layer.Width - 1 - x, y);
        if (symY) Save(x, layer.Height - 1 - y);
        if (symX && symY) Save(layer.Width - 1 - x, layer.Height - 1 - y);
    }
}

/// <summary>
/// Brush tool for drawing pixels
/// </summary>
public class BrushTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Brush;
    public string Name => "Brush";
    public int Size { get; set; } = 1;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }
    
    private bool _isDrawing;
    private int _lastX;
    private int _lastY;
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        _lastX = x;
        _lastY = y;
        DrawAt(layer, x, y, color);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isDrawing)
        {
            DrawLineToPoint(layer, _lastX, _lastY, x, y, color);
            _lastX = x;
            _lastY = y;
        }
    }
    
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = false;
    }
    
    private void DrawLineToPoint(Layer layer, int x0, int y0, int x1, int y1, PixelColor color)
    {
        int dx = Math.Abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
        int dy = -Math.Abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
        int err = dx + dy, e2;

        while (true)
        {
            DrawAt(layer, x0, y0, color);
            if (x0 == x1 && y0 == y1) break;
            e2 = 2 * err;
            if (e2 >= dy) { err += dy; x0 += sx; }
            if (e2 <= dx) { err += dx; y0 += sy; }
        }
    }
    
    private void DrawAt(Layer layer, int x, int y, PixelColor color)
    {
        if (Size == 1)
        {
            layer.SetSymmetricPixel(x, y, color, SymmetryX, SymmetryY);
        }
        else
        {
            int halfSize = Size / 2;
            for (int dy = -halfSize; dy <= halfSize; dy++)
            {
                for (int dx = -halfSize; dx <= halfSize; dx++)
                {
                    layer.SetSymmetricPixel(x + dx, y + dy, color, SymmetryX, SymmetryY);
                }
            }
        }
    }
}

/// <summary>
/// Eraser tool for removing pixels
/// </summary>
public class EraserTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Eraser;
    public string Name => "Eraser";
    public int Size { get; set; } = 1;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }
    
    private bool _isErasing;
    private int _lastX;
    private int _lastY;
    
    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isErasing = true;
        _lastX = x;
        _lastY = y;
        EraseAt(layer, x, y);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isErasing)
        {
            DrawLineToPoint(layer, _lastX, _lastY, x, y);
            _lastX = x;
            _lastY = y;
        }
    }
    
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isErasing = false;
    }
    
    private void DrawLineToPoint(Layer layer, int x0, int y0, int x1, int y1)
    {
        int dx = Math.Abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
        int dy = -Math.Abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
        int err = dx + dy, e2;

        while (true)
        {
            EraseAt(layer, x0, y0);
            if (x0 == x1 && y0 == y1) break;
            e2 = 2 * err;
            if (e2 >= dy) { err += dy; x0 += sx; }
            if (e2 <= dx) { err += dx; y0 += sy; }
        }
    }
    
    private void EraseAt(Layer layer, int x, int y)
    {
        if (Size == 1)
        {
            layer.SetSymmetricPixel(x, y, PixelColor.Transparent, SymmetryX, SymmetryY);
        }
        else
        {
            int halfSize = Size / 2;
            for (int dy = -halfSize; dy <= halfSize; dy++)
            {
                for (int dx = -halfSize; dx <= halfSize; dx++)
                {
                    layer.SetSymmetricPixel(x + dx, y + dy, PixelColor.Transparent, SymmetryX, SymmetryY);
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
        if (!layer.IsInBounds(x, y)) return;
        var pickedColor = layer.GetPixel(x, y);
        if (pickedColor.IsTransparent) return;
        ColorPicked?.Invoke(pickedColor);
    }
    
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color) { }
}

/// <summary>
/// Line tool using Bresenham's algorithm
/// </summary>
public class LineTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Line;
    public string Name => "Line";
    public int Size { get; set; } = 1;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }

    private int _startX, _startY;
    private bool _isDrawing;
    private Dictionary<(int x, int y), PixelColor> _savedPixels = new();

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        _startX = x;
        _startY = y;
        _savedPixels.Clear();
        DrawLine(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawLine(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;
        _isDrawing = false;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawLine(layer, _startX, _startY, x, y, color, true);
    }

    private void DrawLine(Layer layer, int x0, int y0, int x1, int y1, PixelColor color, bool isFinal)
    {
        int dx = Math.Abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
        int dy = -Math.Abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
        int err = dx + dy, e2;

        while (true)
        {
            if (layer.IsInBounds(x0, y0))
            {
                if (isFinal)
                {
                    layer.SetSymmetricPixel(x0, y0, color, SymmetryX, SymmetryY);
                }
                else
                {
                    layer.SaveSymmetricPixelState(x0, y0, _savedPixels, SymmetryX, SymmetryY);
                    layer.SetSymmetricPixelRaw(x0, y0, color, SymmetryX, SymmetryY);
                }
            }

            if (x0 == x1 && y0 == y1) break;
            e2 = 2 * err;
            if (e2 >= dy) { err += dy; x0 += sx; }
            if (e2 <= dx) { err += dx; y0 += sy; }
        }
    }
}

/// <summary>
/// Rectangle shape tool
/// </summary>
public class RectangleTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Rectangle;
    public string Name => "Rectangle";
    public bool Fill { get; set; } = false;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }

    private int _startX, _startY;
    private bool _isDrawing;
    private Dictionary<(int x, int y), PixelColor> _savedPixels = new();

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        _startX = x;
        _startY = y;
        _savedPixels.Clear();
        DrawRect(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawRect(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;
        _isDrawing = false;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawRect(layer, _startX, _startY, x, y, color, true);
    }

    private void DrawRect(Layer layer, int x0, int y0, int x1, int y1, PixelColor color, bool isFinal)
    {
        int minX = Math.Min(x0, x1);
        int maxX = Math.Max(x0, x1);
        int minY = Math.Min(y0, y1);
        int maxY = Math.Max(y0, y1);

        for (int y = minY; y <= maxY; y++)
        {
            for (int x = minX; x <= maxX; x++)
            {
                if (!Fill && !(x == minX || x == maxX || y == minY || y == maxY))
                    continue;

                if (layer.IsInBounds(x, y))
                {
                    if (isFinal)
                    {
                        layer.SetSymmetricPixel(x, y, color, SymmetryX, SymmetryY);
                    }
                    else
                    {
                        layer.SaveSymmetricPixelState(x, y, _savedPixels, SymmetryX, SymmetryY);
                        layer.SetSymmetricPixelRaw(x, y, color, SymmetryX, SymmetryY);
                    }
                }
            }
        }
    }
}

/// <summary>
/// Circle shape tool
/// </summary>
public class CircleTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Circle;
    public string Name => "Circle";
    public bool Fill { get; set; } = false;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }

    private int _startX, _startY;
    private bool _isDrawing;
    private Dictionary<(int x, int y), PixelColor> _savedPixels = new();

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        _startX = x;
        _startY = y;
        _savedPixels.Clear();
        DrawCircle(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawCircle(layer, _startX, _startY, x, y, color, false);
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isDrawing) return;
        _isDrawing = false;

        foreach (var kvp in _savedPixels)
            layer.SetPixelRaw(kvp.Key.x, kvp.Key.y, kvp.Value);
        _savedPixels.Clear();

        DrawCircle(layer, _startX, _startY, x, y, color, true);
    }

    private void DrawCircle(Layer layer, int x0, int y0, int x1, int y1, PixelColor color, bool isFinal)
    {
        int r = (int)Math.Round(Math.Sqrt(Math.Pow(x1 - x0, 2) + Math.Pow(y1 - y0, 2)));
        int x = r, y = 0;
        int err = 1 - x;
        
        HashSet<(int, int)> points = new();

        while (x >= y)
        {
            points.Add((x + x0, y + y0));
            points.Add((y + x0, x + y0));
            points.Add((-x + x0, y + y0));
            points.Add((-y + x0, x + y0));
            points.Add((-x + x0, -y + y0));
            points.Add((-y + x0, -x + y0));
            points.Add((x + x0, -y + y0));
            points.Add((y + x0, -x + y0));
            y++;
            if (err < 0)
            {
                err += 2 * y + 1;
            }
            else
            {
                x--;
                err += 2 * (y - x + 1);
            }
        }

        if (Fill && r > 0)
        {
            for (int cy = y0 - r; cy <= y0 + r; cy++)
            {
                for (int cx = x0 - r; cx <= x0 + r; cx++)
                {
                    if (Math.Pow(cx - x0, 2) + Math.Pow(cy - y0, 2) <= r * r)
                    {
                        points.Add((cx, cy));
                    }
                }
            }
        }

        foreach (var p in points)
        {
            if (layer.IsInBounds(p.Item1, p.Item2))
            {
                if (isFinal)
                {
                    layer.SetSymmetricPixel(p.Item1, p.Item2, color, SymmetryX, SymmetryY);
                }
                else
                {
                    layer.SaveSymmetricPixelState(p.Item1, p.Item2, _savedPixels, SymmetryX, SymmetryY);
                    layer.SetSymmetricPixelRaw(p.Item1, p.Item2, color, SymmetryX, SymmetryY);
                }
            }
        }
    }
}

/// <summary>
/// Pan tool - moves the canvas view. Actual pan logic is handled by the View/ViewModel.
/// </summary>
public class PanTool : ITool
{
    public ToolType Type => ToolType.Pan;
    public string Name => "Pan";

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseMove(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color) { }
}

/// <summary>
/// Rectangle selection tool
/// </summary>
public class SelectionTool : ITool
{
    public ToolType Type => ToolType.Selection;
    public string Name => "Selection";

    private int _startX, _startY;
    private bool _isSelecting;
    private int _endX, _endY;

    public Action<Layer, int, int, int, int>? OnSelectionComplete { get; set; }
    public bool IsSelecting => _isSelecting;
    public (int Left, int Top, int Width, int Height) GetCurrentRect()
    {
        int left = Math.Min(_startX, _endX);
        int top = Math.Min(_startY, _endY);
        return (left, top, Math.Abs(_endX - _startX) + 1, Math.Abs(_endY - _startY) + 1);
    }

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isSelecting = true;
        _startX = x;
        _startY = y;
        _endX = x;
        _endY = y;
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isSelecting)
        {
            _endX = x;
            _endY = y;
        }
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        if (!_isSelecting) return;
        _isSelecting = false;
        _endX = x;
        _endY = y;

        int left = Math.Min(_startX, _endX);
        int top = Math.Min(_startY, _endY);
        int width = Math.Abs(_endX - _startX) + 1;
        int height = Math.Abs(_endY - _startY) + 1;

        if (width > 0 && height > 0)
        {
            OnSelectionComplete?.Invoke(layer, left, top, width, height);
        }
    }
}

/// <summary>
/// Move selection tool - non-destructive move with background preservation
/// </summary>
public class MoveTool : ITool
{
    public ToolType Type => ToolType.Move;
    public string Name => "Move";

    private bool _isMoving;
    private int _offsetX, _offsetY;

    public Func<Layer, int, int, (bool ok, int offsetX, int offsetY)>? OnMoveStart { get; set; }
    public Action<Layer, int, int>? OnMoveUpdate { get; set; }
    public Action<Layer>? OnMoveEnd { get; set; }

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        if (OnMoveStart != null)
        {
            var result = OnMoveStart(layer, x, y);
            if (result.ok)
            {
                _isMoving = true;
                _offsetX = result.offsetX;
                _offsetY = result.offsetY;
            }
        }
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isMoving && OnMoveUpdate != null)
        {
            int newLeft = x - _offsetX;
            int newTop = y - _offsetY;
            OnMoveUpdate(layer, newLeft, newTop);
        }
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        if (_isMoving)
        {
            OnMoveEnd?.Invoke(layer);
            _isMoving = false;
        }
    }
}

/// <summary>
/// Spray tool for random droplet particle drawing
/// </summary>
public class SprayTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Spray;
    public string Name => "Spray";
    public int Size { get; set; } = 8;
    public int Density { get; set; } = 10;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }

    private bool _isSpraying;
    private int _lastX, _lastY;
    private Random _random = new();

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isSpraying = true;
        _lastX = x; _lastY = y;
        SprayAt(layer, x, y, color);
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isSpraying)
        {
            _lastX = x; _lastY = y;
            SprayAt(layer, x, y, color);
        }
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isSpraying = false;
    }

    private void SprayAt(Layer layer, int x, int y, PixelColor color)
    {
        for (int i = 0; i < Density; i++)
        {
            double angle = _random.NextDouble() * Math.PI * 2;
            double radius = _random.NextDouble() * (Size / 2.0);
            int px = x + (int)Math.Round(Math.Cos(angle) * radius);
            int py = y + (int)Math.Round(Math.Sin(angle) * radius);

            layer.SetSymmetricPixel(px, py, color, SymmetryX, SymmetryY);
        }
    }
}

/// <summary>
/// Dither tool for checkerboard pattern drawing
/// </summary>
public class DitherTool : ITool, ISymmetricTool
{
    public ToolType Type => ToolType.Dither;
    public string Name => "Dither";
    public int Size { get; set; } = 1;
    public bool SymmetryX { get; set; }
    public bool SymmetryY { get; set; }

    private bool _isDrawing;
    private int _lastX, _lastY;

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = true;
        _lastX = x;
        _lastY = y;
        DrawDither(layer, x, y, color);
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color)
    {
        if (_isDrawing)
        {
            DrawLineToPoint(layer, _lastX, _lastY, x, y, color);
            _lastX = x;
            _lastY = y;
        }
    }

    public void OnMouseUp(Layer layer, int x, int y, PixelColor color)
    {
        _isDrawing = false;
    }

    private void DrawLineToPoint(Layer layer, int x0, int y0, int x1, int y1, PixelColor color)
    {
        int dx = Math.Abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
        int dy = -Math.Abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
        int err = dx + dy, e2;

        while (true)
        {
            DrawDither(layer, x0, y0, color);
            if (x0 == x1 && y0 == y1) break;
            e2 = 2 * err;
            if (e2 >= dy) { err += dy; x0 += sx; }
            if (e2 <= dx) { err += dx; y0 += sy; }
        }
    }

    private void DrawDither(Layer layer, int x, int y, PixelColor color)
    {
        if (Size == 1)
        {
            if ((x + y) % 2 == 0) layer.SetSymmetricPixel(x, y, color, SymmetryX, SymmetryY);
        }
        else
        {
            int halfSize = Size / 2;
            for (int dy = -halfSize; dy <= halfSize; dy++)
            {
                for (int dx = -halfSize; dx <= halfSize; dx++)
                {
                    int px = x + dx;
                    int py = y + dy;
                    if ((px + py) % 2 == 0)
                        layer.SetSymmetricPixel(px, py, color, SymmetryX, SymmetryY);
                }
            }
        }
    }
}

/// <summary>
/// Magic Wand tool for selecting contiguous pixels of the same color
/// </summary>
public class MagicWandTool : ITool
{
    public ToolType Type => ToolType.MagicWand;
    public string Name => "Magic Wand";

    public Action<Layer, HashSet<(int x, int y)>>? OnSelectionComplete { get; set; }

    public void OnMouseDown(Layer layer, int x, int y, PixelColor color)
    {
        if (!layer.IsInBounds(x, y)) return;

        var targetColor = layer.GetPixel(x, y);
        var selectedPoints = new HashSet<(int x, int y)>();
        
        var stack = new Stack<(int x, int y)>();
        stack.Push((x, y));
        
        while (stack.Count > 0)
        {
            var (cx, cy) = stack.Pop();
            
            if (!layer.IsInBounds(cx, cy)) continue;
            if (selectedPoints.Contains((cx, cy))) continue;
            if (layer.GetPixel(cx, cy) != targetColor) continue;
            
            selectedPoints.Add((cx, cy));
            
            // Push neighbors
            if (cx > 0) stack.Push((cx - 1, cy));
            if (cx < layer.Width - 1) stack.Push((cx + 1, cy));
            if (cy > 0) stack.Push((cx, cy - 1));
            if (cy < layer.Height - 1) stack.Push((cx, cy + 1));
        }

        if (selectedPoints.Count > 0)
        {
            OnSelectionComplete?.Invoke(layer, selectedPoints);
        }
    }

    public void OnMouseMove(Layer layer, int x, int y, PixelColor color) { }
    public void OnMouseUp(Layer layer, int x, int y, PixelColor color) { }
}

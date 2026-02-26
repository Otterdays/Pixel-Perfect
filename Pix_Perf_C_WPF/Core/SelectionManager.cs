using System;
using System.Collections.Generic;

namespace PixelPerfect.Core;

/// <summary>
/// Manages selection state: rectangle, captured pixels, clipboard buffer.
/// </summary>
public class SelectionManager
{
    public int SelectionLeft { get; private set; }
    public int SelectionTop { get; private set; }
    public int SelectionWidth { get; private set; }
    public int SelectionHeight { get; private set; }

    public bool HasSelection { get; private set; }
    public PixelColor[,]? SelectedPixels { get; private set; }
    public PixelColor[,]? ClipboardBuffer { get; private set; }
    public int ClipboardWidth { get; private set; }
    public int ClipboardHeight { get; private set; }

    public bool IsMoving { get; private set; }
    private PixelColor[,]? _backgroundPixels;
    private int _lastDrawnLeft, _lastDrawnTop;

    public void SetSelectionRect(int left, int top, int width, int height)
    {
        SelectionLeft = left;
        SelectionTop = top;
        SelectionWidth = width;
        SelectionHeight = height;
        HasSelection = width > 0 && height > 0;
    }

    public void CaptureFromLayer(Layer layer, int left, int top, int width, int height)
    {
        left = Math.Clamp(left, 0, layer.Width);
        top = Math.Clamp(top, 0, layer.Height);
        width = Math.Min(width, layer.Width - left);
        height = Math.Min(height, layer.Height - top);

        if (width <= 0 || height <= 0)
        {
            HasSelection = false;
            return;
        }

        SelectedPixels = new PixelColor[height, width];
        for (int y = 0; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int cx = left + x;
                int cy = top + y;
                if (layer.IsInBounds(cx, cy))
                    SelectedPixels[y, x] = layer.GetPixel(cx, cy);
            }
        }

        SetSelectionRect(left, top, width, height);
    }

    public void CaptureMaskedFromLayer(Layer layer, HashSet<(int x, int y)> selectedPoints)
    {
        if (selectedPoints.Count == 0)
        {
            HasSelection = false;
            return;
        }

        int minX = int.MaxValue, minY = int.MaxValue;
        int maxX = int.MinValue, maxY = int.MinValue;

        foreach (var p in selectedPoints)
        {
            if (p.x < minX) minX = p.x;
            if (p.x > maxX) maxX = p.x;
            if (p.y < minY) minY = p.y;
            if (p.y > maxY) maxY = p.y;
        }

        int left = minX;
        int top = minY;
        int width = maxX - minX + 1;
        int height = maxY - minY + 1;

        SelectedPixels = new PixelColor[height, width];
        // Initialize all to transparent (which acts as the unselected mask)
        for (int y = 0; y < height; y++)
            for (int x = 0; x < width; x++)
                SelectedPixels[y, x] = PixelColor.Transparent;

        foreach (var p in selectedPoints)
        {
            int localX = p.x - left;
            int localY = p.y - top;
            SelectedPixels[localY, localX] = layer.GetPixel(p.x, p.y);
        }

        SetSelectionRect(left, top, width, height);
    }

    public void Copy()
    {
        if (SelectedPixels == null) return;
        ClipboardBuffer = (PixelColor[,])SelectedPixels.Clone();
        ClipboardWidth = SelectionWidth;
        ClipboardHeight = SelectionHeight;
    }

    public void ClearSelection()
    {
        HasSelection = false;
        SelectedPixels = null;
        SetSelectionRect(0, 0, 0, 0);
    }

    public void ClearClipboard()
    {
        ClipboardBuffer = null;
        ClipboardWidth = 0;
        ClipboardHeight = 0;
    }

    public bool IsPointInSelection(int x, int y)
    {
        return HasSelection &&
               x >= SelectionLeft && x < SelectionLeft + SelectionWidth &&
               y >= SelectionTop && y < SelectionTop + SelectionHeight;
    }

    public bool StartMove(Layer layer)
    {
        if (!HasSelection || SelectedPixels == null) return false;
        int left = SelectionLeft, top = SelectionTop, w = SelectionWidth, h = SelectionHeight;
        _backgroundPixels = new PixelColor[h, w];
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                int cx = left + x, cy = top + y;
                _backgroundPixels[y, x] = layer.IsInBounds(cx, cy) ? layer.GetPixel(cx, cy) : PixelColor.Transparent;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, PixelColor.Transparent);
            }
        }
        _lastDrawnLeft = left;
        _lastDrawnTop = top;
        IsMoving = true;
        return true;
    }

    public void UpdateMovePosition(Layer layer, int newLeft, int newTop)
    {
        if (!IsMoving || SelectedPixels == null || _backgroundPixels == null) return;
        int w = SelectionWidth, h = SelectionHeight;
        // Erase old preview
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, _backgroundPixels[y, x]);
            }
        }
        // Capture background at new position (reuse existing array — no allocation)
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                int cx = newLeft + x, cy = newTop + y;
                _backgroundPixels[y, x] = layer.IsInBounds(cx, cy) ? layer.GetPixel(cx, cy) : PixelColor.Transparent;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, SelectedPixels[y, x]);
            }
        }
        _lastDrawnLeft = newLeft;
        _lastDrawnTop = newTop;
        SetSelectionRect(newLeft, newTop, w, h);
    }

    public void EndMove(Layer layer)
    {
        if (!IsMoving) return;
        IsMoving = false;
        _backgroundPixels = null;
    }

    public void MirrorHorizontal(Layer layer)
    {
        if (SelectedPixels == null) return;
        
        bool wasMoving = IsMoving;
        if (wasMoving && _backgroundPixels != null)
        {
            // Erase preview
            for (int y = 0; y < SelectionHeight; y++)
                for (int x = 0; x < SelectionWidth; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, _backgroundPixels[y, x]);
                }
        }

        int w = SelectionWidth, h = SelectionHeight;
        var newPixels = new PixelColor[h, w];
        for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
                newPixels[y, x] = SelectedPixels[y, w - 1 - x];
        SelectedPixels = newPixels;
        
        if (wasMoving)
        {
            // Redraw preview
            for (int y = 0; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, SelectedPixels[y, x]);
                }
        }
    }

    public void MirrorVertical(Layer layer)
    {
        if (SelectedPixels == null) return;
        
        bool wasMoving = IsMoving;
        if (wasMoving && _backgroundPixels != null)
        {
            // Erase preview
            for (int y = 0; y < SelectionHeight; y++)
                for (int x = 0; x < SelectionWidth; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, _backgroundPixels[y, x]);
                }
        }

        int w = SelectionWidth, h = SelectionHeight;
        var newPixels = new PixelColor[h, w];
        for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
                newPixels[y, x] = SelectedPixels[h - 1 - y, x];
        SelectedPixels = newPixels;
        
        if (wasMoving)
        {
            // Redraw preview
            for (int y = 0; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, SelectedPixels[y, x]);
                }
        }
    }

    public void Rotate90(Layer layer)
    {
        if (SelectedPixels == null) return;

        bool wasMoving = IsMoving;
        if (wasMoving && _backgroundPixels != null)
        {
            for (int y = 0; y < SelectionHeight; y++)
                for (int x = 0; x < SelectionWidth; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, _backgroundPixels[y, x]);
                }
        }

        int w = SelectionWidth, h = SelectionHeight;
        var newPixels = new PixelColor[w, h]; // transposed
        for (int y = 0; y < h; y++)
            for (int x = 0; x < w; x++)
                newPixels[x, h - 1 - y] = SelectedPixels[y, x];

        SelectedPixels = newPixels;
        SetSelectionRect(_lastDrawnLeft, _lastDrawnTop, h, w); // w and h swapped

        if (wasMoving)
        {
            _backgroundPixels = new PixelColor[w, h];
            for (int y = 0; y < w; y++)
            {
                for (int x = 0; x < h; x++)
                {
                    int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                    _backgroundPixels[y, x] = layer.IsInBounds(cx, cy) ? layer.GetPixel(cx, cy) : PixelColor.Transparent;
                    if (layer.IsInBounds(cx, cy))
                        layer.SetPixel(cx, cy, SelectedPixels[y, x]);
                }
            }
        }
    }
}

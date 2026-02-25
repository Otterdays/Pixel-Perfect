using System;

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
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                int cx = _lastDrawnLeft + x, cy = _lastDrawnTop + y;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, _backgroundPixels[y, x]);
            }
        }
        _backgroundPixels = new PixelColor[h, w];
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
}

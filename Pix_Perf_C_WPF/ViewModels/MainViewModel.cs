using System;
using System.Collections.Generic;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PixelPerfect.Core;
using System.Collections.ObjectModel;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using Microsoft.Win32;
using PixelPerfect.Services;

namespace PixelPerfect.ViewModels;

/// <summary>
/// Main ViewModel for the application
/// </summary>
public partial class MainViewModel : ObservableObject
{
    [ObservableProperty]
    private PixelCanvas _canvas;
    
    [ObservableProperty]
    private PixelColor _currentColor = new(255, 100, 100, 255);
    
    [ObservableProperty]
    private ITool _currentTool;
    
    [ObservableProperty]
    private int _zoom = 16;
    
    [ObservableProperty]
    private WriteableBitmap? _canvasBitmap;
    
    [ObservableProperty]
    private string _statusText = "Ready";

    [ObservableProperty]
    private bool _showGrid = true;

    [ObservableProperty]
    private double _panOffsetX;

    [ObservableProperty]
    private double _panOffsetY;
    
    // Rendering state
    private byte[]? _renderBuffer;
    
    // Tools
    public BrushTool BrushTool { get; } = new();
    public EraserTool EraserTool { get; } = new();
    public FillTool FillTool { get; } = new();
    public EyedropperTool EyedropperTool { get; } = new();
    public LineTool LineTool { get; } = new();
    public RectangleTool RectangleTool { get; } = new();
    public CircleTool CircleTool { get; } = new();
    public PanTool PanTool { get; } = new();
    public SelectionTool SelectionTool { get; } = new();
    public MoveTool MoveTool { get; } = new();
    public SelectionManager SelectionManager { get; } = new();
    
    // Zoom levels
    public int[] ZoomLevels { get; } = { 1, 2, 4, 8, 16, 24, 32, 48, 64 };

    // Palette for color picker
    public IReadOnlyList<PixelColor> PaletteColors => Palette.SnesClassic;
    
    public UndoManager UndoManager { get; } = new();

    /// <summary>
    /// Callback to show New Canvas dialog. Set by the View. Returns (Width, Height) or null if cancelled.
    /// </summary>
    public Func<(int Width, int Height)?>? RequestNewCanvasSize { get; set; }

    public MainViewModel()
    {
        _canvas = new PixelCanvas(32, 32);
        Canvas.PixelChanged += OnCanvasPixelChanged;
        _currentTool = BrushTool;

        SelectionTool.OnSelectionComplete = (layer, left, top, width, height) =>
        {
            SelectionManager.CaptureFromLayer(layer, left, top, width, height);
        };

        MoveTool.OnMoveStart = (layer, x, y) =>
        {
            if (!SelectionManager.IsPointInSelection(x, y)) return (false, 0, 0);
            int offsetX = x - SelectionManager.SelectionLeft;
            int offsetY = y - SelectionManager.SelectionTop;
            if (!SelectionManager.StartMove(layer)) return (false, 0, 0);
            UndoManager.BeginTransaction();
            return (true, offsetX, offsetY);
        };
        MoveTool.OnMoveUpdate = (layer, newLeft, newTop) =>
        {
            SelectionManager.UpdateMovePosition(layer, newLeft, newTop);
        };
        MoveTool.OnMoveEnd = layer =>
        {
            SelectionManager.EndMove(layer);
            UndoManager.EndTransaction();
        };
        
        // Hook up eyedropper
        EyedropperTool.ColorPicked += color => CurrentColor = color;
        
        // Initial render
        UpdateBitmap();
    }
    
    [RelayCommand]
    private void SelectBrush() => CurrentTool = BrushTool;
    
    [RelayCommand]
    private void SelectEraser() => CurrentTool = EraserTool;
    
    [RelayCommand]
    private void SelectFill() => CurrentTool = FillTool;
    
    [RelayCommand]
    private void SelectEyedropper() => CurrentTool = EyedropperTool;

    [RelayCommand]
    private void SelectLine() => CurrentTool = LineTool;

    [RelayCommand]
    private void SelectRectangle() => CurrentTool = RectangleTool;

    [RelayCommand]
    private void SelectCircle() => CurrentTool = CircleTool;

    [RelayCommand]
    private void SelectPan() => CurrentTool = PanTool;

    [RelayCommand]
    private void SelectSelection() => CurrentTool = SelectionTool;

    [RelayCommand]
    private void SelectMove() => CurrentTool = MoveTool;

    [RelayCommand]
    private void Copy()
    {
        if (SelectionManager.HasSelection) SelectionManager.Copy();
    }

    [RelayCommand]
    private void Cut()
    {
        if (!SelectionManager.HasSelection) return;
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        SelectionManager.Copy();
        ClearSelectionPixels(layer);
        SelectionManager.ClearSelection();
        UpdateBitmap();
    }

    [RelayCommand]
    private void Paste()
    {
        if (SelectionManager.ClipboardBuffer == null) return;
        EnterPasteMode();
    }

    [RelayCommand]
    private void Delete()
    {
        if (!SelectionManager.HasSelection) return;
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        ClearSelectionPixels(layer);
        SelectionManager.ClearSelection();
        UpdateBitmap();
    }

    private void ClearSelectionPixels(Layer layer)
    {
        int left = SelectionManager.SelectionLeft;
        int top = SelectionManager.SelectionTop;
        int w = SelectionManager.SelectionWidth;
        int h = SelectionManager.SelectionHeight;
        for (int y = 0; y < h; y++)
        {
            for (int x = 0; x < w; x++)
            {
                int cx = left + x;
                int cy = top + y;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, PixelColor.Transparent);
            }
        }
    }

    private bool _isPasteMode;
    private int _pastePreviewX, _pastePreviewY;

    private void EnterPasteMode()
    {
        _isPasteMode = true;
        StatusText = "Click to place paste";
    }

    private void PlacePaste(int canvasX, int canvasY)
    {
        if (SelectionManager.ClipboardBuffer == null) return;
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        int cw = SelectionManager.ClipboardWidth;
        int ch = SelectionManager.ClipboardHeight;
        var buf = SelectionManager.ClipboardBuffer;
        UndoManager.BeginTransaction();
        for (int y = 0; y < ch; y++)
        {
            for (int x = 0; x < cw; x++)
            {
                var color = buf[y, x];
                if (color.IsTransparent) continue;
                int cx = canvasX + x;
                int cy = canvasY + y;
                if (layer.IsInBounds(cx, cy))
                    layer.SetPixel(cx, cy, color);
            }
        }
        UndoManager.EndTransaction();
        _isPasteMode = false;
        UpdateBitmap();
        StatusText = "Pasted";
    }

    [RelayCommand]
    private void SelectPaletteColor(PixelColor color)
    {
        CurrentColor = color;
        CurrentTool = BrushTool;
    }

    [RelayCommand]
    private void ToggleGrid()
    {
        ShowGrid = !ShowGrid;
        UpdateBitmap();
    }
    
    [RelayCommand]
    private void NewCanvas()
    {
        var size = RequestNewCanvasSize?.Invoke();
        if (!size.HasValue) return;
        CreateCanvas(size.Value.Width, size.Value.Height);
    }

    /// <summary>
    /// Creates a new canvas with the given dimensions. Called after dialog confirmation.
    /// Auto-adjusts zoom for larger canvases (e.g. 128×128 → 4x, 256×256 → 2x).
    /// </summary>
    public void CreateCanvas(int width, int height)
    {
        if (Canvas != null)
        {
            Canvas.PixelChanged -= OnCanvasPixelChanged;
        }
        Canvas = new PixelCanvas(width, height);
        Canvas.PixelChanged += OnCanvasPixelChanged;
        UndoManager.Clear();

        // Auto-zoom for larger canvases (match Python behavior)
        int maxDim = Math.Max(width, height);
        Zoom = maxDim switch
        {
            >= 256 => 2,
            >= 128 => 4,
            >= 64 => 8,
            >= 32 => 16,
            _ => 16
        };

        UpdateBitmap();
        StatusText = $"New canvas created ({width}×{height})";
    }

    [RelayCommand]
    private void Undo()
    {
        UndoManager.Undo();
        UpdateBitmap();
    }

    [RelayCommand]
    private void Redo()
    {
        UndoManager.Redo();
        UpdateBitmap();
    }

    [RelayCommand]
    private void Save()
    {
        var saveFileDialog = new SaveFileDialog
        {
            Filter = "PNG Image (*.png)|*.png|All Files (*.*)|*.*",
            DefaultExt = "png",
            Title = "Export Image"
        };

        if (saveFileDialog.ShowDialog() == true)
        {
            try
            {
                // Defaulting export scale to 1x for preview parity, we will add UI scale options later
                FileService.ExportToPng(Canvas, saveFileDialog.FileName, 1);
                StatusText = $"Saved to {System.IO.Path.GetFileName(saveFileDialog.FileName)}";
            }
            catch (System.Exception ex)
            {
                StatusText = $"Save failed: {ex.Message}";
            }
        }
    }

    private void OnCanvasPixelChanged(Layer layer, int x, int y, PixelColor oldColor, PixelColor newColor)
    {
        UndoManager.RecordPixelChange(layer, x, y, oldColor, newColor);
    }
    
    [RelayCommand]
    private void AddLayer()
    {
        Canvas.AddLayer($"Layer {Canvas.Layers.Count + 1}");
        StatusText = $"Added layer {Canvas.Layers.Count}";
    }
    
    public void HandleMouseDown(int canvasX, int canvasY)
    {
        if (_isPasteMode)
        {
            PlacePaste(canvasX, canvasY);
            return;
        }
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;

        bool isDrawingTool = CurrentTool != SelectionTool && CurrentTool != PanTool && CurrentTool != MoveTool;
        if (isDrawingTool)
            UndoManager.BeginTransaction();
        CurrentTool.OnMouseDown(layer, canvasX, canvasY, CurrentColor);
        UpdateBitmap();
    }
    
    public void HandleMouseMove(int canvasX, int canvasY, bool isPressed)
    {
        if (_isPasteMode)
        {
            _pastePreviewX = canvasX;
            _pastePreviewY = canvasY;
            UpdateBitmap();
            StatusText = $"Click to place at ({canvasX}, {canvasY})";
            return;
        }
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        
        if (isPressed)
        {
            CurrentTool.OnMouseMove(layer, canvasX, canvasY, CurrentColor);
            UpdateBitmap();
        }
        
        StatusText = $"({canvasX}, {canvasY})";
    }
    
    public void AddPanDelta(double deltaX, double deltaY)
    {
        PanOffsetX += deltaX;
        PanOffsetY += deltaY;
    }

    public void HandleMouseUp(int canvasX, int canvasY)
    {
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;

        CurrentTool.OnMouseUp(layer, canvasX, canvasY, CurrentColor);
        bool isDrawingTool = CurrentTool != SelectionTool && CurrentTool != PanTool && CurrentTool != MoveTool;
        if (isDrawingTool)
            UndoManager.EndTransaction();
        UpdateBitmap();
    }
    
    /// <summary>
    /// Renders the canvas to a WriteableBitmap for display
    /// </summary>
    public void UpdateBitmap()
    {
        int stride = Canvas.Width * 4;
        int requiredSize = Canvas.Height * stride;
        
        // Create or resize bitmap and buffer if needed
        if (CanvasBitmap == null || 
            CanvasBitmap.PixelWidth != Canvas.Width || 
            CanvasBitmap.PixelHeight != Canvas.Height ||
            _renderBuffer == null ||
            _renderBuffer.Length != requiredSize)
        {
            CanvasBitmap = new WriteableBitmap(
                Canvas.Width, Canvas.Height,
                96, 96, PixelFormats.Bgra32, null);
                
            _renderBuffer = new byte[requiredSize];
        }
        
        // Flatten layers directly into the byte array (0 allocations!)
        Canvas.FlattenToBuffer(_renderBuffer);

        // Draw grid overlay if enabled
        if (ShowGrid)
        {
            DrawGridOverlay(_renderBuffer, Canvas.Width, Canvas.Height, stride);
        }

        // Draw selection overlay
        DrawSelectionOverlay(_renderBuffer, Canvas.Width, Canvas.Height, stride);

        // Draw paste preview
        if (_isPasteMode && SelectionManager.ClipboardBuffer != null)
        {
            DrawPastePreview(_renderBuffer, Canvas.Width, Canvas.Height, stride);
        }
        
        CanvasBitmap.WritePixels(
            new System.Windows.Int32Rect(0, 0, Canvas.Width, Canvas.Height),
            _renderBuffer, stride, 0);
    }

    private static void DrawGridOverlay(byte[] buffer, int width, int height, int stride)
    {
        // Grid color: #646464 at 50% blend (BGRA) - draw at pixel boundaries
        const byte gR = 0x64, gG = 0x64, gB = 0x64;
        const double blend = 0.5;

        // Vertical lines at x=1..width-1 (boundaries between columns)
        for (int x = 1; x < width; x++)
        {
            for (int y = 0; y < height; y++)
            {
                int offset = y * stride + x * 4;
                if (offset + 3 >= buffer.Length) continue;
                BlendPixel(buffer, offset, gR, gG, gB, blend);
            }
        }
        // Horizontal lines at y=1..height-1 (boundaries between rows)
        for (int y = 1; y < height; y++)
        {
            for (int x = 0; x < width; x++)
            {
                int offset = y * stride + x * 4;
                if (offset + 3 >= buffer.Length) continue;
                BlendPixel(buffer, offset, gR, gG, gB, blend);
            }
        }
    }

    private void DrawSelectionOverlay(byte[] buffer, int width, int height, int stride)
    {
        int left, top, w, h;
        if (CurrentTool == SelectionTool && SelectionTool.IsSelecting)
        {
            var rect = SelectionTool.GetCurrentRect();
            left = rect.Left;
            top = rect.Top;
            w = rect.Width;
            h = rect.Height;
        }
        else if (SelectionManager.HasSelection || SelectionManager.IsMoving)
        {
            left = SelectionManager.SelectionLeft;
            top = SelectionManager.SelectionTop;
            w = SelectionManager.SelectionWidth;
            h = SelectionManager.SelectionHeight;
        }
        else return;

        if (w <= 0 || h <= 0) return;
        int right = Math.Min(left + w, width);
        int bottom = Math.Min(top + h, height);
        left = Math.Max(0, left);
        top = Math.Max(0, top);

        const byte white = 255;
        for (int x = left; x < right; x++)
        {
            if (top > 0) DrawPixel(buffer, (top - 1) * stride + x * 4, white);
            if (bottom < height) DrawPixel(buffer, bottom * stride + x * 4, white);
        }
        for (int y = top; y < bottom; y++)
        {
            if (left > 0) DrawPixel(buffer, y * stride + (left - 1) * 4, white);
            if (right < width) DrawPixel(buffer, y * stride + right * 4, white);
        }
    }

    private void DrawPastePreview(byte[] buffer, int width, int height, int stride)
    {
        var buf = SelectionManager.ClipboardBuffer!;
        int cw = SelectionManager.ClipboardWidth;
        int ch = SelectionManager.ClipboardHeight;
        int ox = _pastePreviewX;
        int oy = _pastePreviewY;
        for (int y = 0; y < ch; y++)
        {
            for (int x = 0; x < cw; x++)
            {
                var color = buf[y, x];
                if (color.IsTransparent) continue;
                int cx = ox + x;
                int cy = oy + y;
                if (cx < 0 || cx >= width || cy < 0 || cy >= height) continue;
                int offset = cy * stride + cx * 4;
                buffer[offset] = color.B;
                buffer[offset + 1] = color.G;
                buffer[offset + 2] = color.R;
                buffer[offset + 3] = 255;
            }
        }
    }

    private static void DrawPixel(byte[] buffer, int offset, byte value)
    {
        if (offset + 3 >= buffer.Length) return;
        buffer[offset] = value;
        buffer[offset + 1] = value;
        buffer[offset + 2] = value;
        buffer[offset + 3] = 255;
    }

    private static void BlendPixel(byte[] buffer, int offset, byte gr, byte gg, byte gb, double blend)
    {
        buffer[offset] = (byte)(buffer[offset] * (1 - blend) + gb * blend);
        buffer[offset + 1] = (byte)(buffer[offset + 1] * (1 - blend) + gg * blend);
        buffer[offset + 2] = (byte)(buffer[offset + 2] * (1 - blend) + gr * blend);
    }
}

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

    // Export scale options for PNG
    public int[] ExportScaleOptions { get; } = { 1, 2, 4, 8 };

    [ObservableProperty]
    private int _exportScale = 1;

    // Palette for color picker — load from PaletteLoader (SNES Classic + assets/palettes/*.json)
    public IReadOnlyList<PaletteLoader.PaletteEntry> AvailablePalettes { get; } = new List<PaletteLoader.PaletteEntry>(PaletteLoader.LoadAll());

    [ObservableProperty]
    [NotifyPropertyChangedFor(nameof(PaletteColors))]
    [NotifyPropertyChangedFor(nameof(PaletteSections))]
    private PaletteLoader.PaletteEntry? _selectedPalette;

    public IReadOnlyList<PixelColor> PaletteColors => SelectedPalette?.Colors ?? Palette.SnesClassic;

    /// <summary>Palette grouped by sections for UI (title + colors per section).</summary>
    public IReadOnlyList<PaletteLoader.PaletteSection> PaletteSections =>
        SelectedPalette != null
            ? SelectedPalette.Sections
            : new List<PaletteLoader.PaletteSection> { new PaletteLoader.PaletteSection("Colors", Palette.SnesClassic) };
    
    public UndoManager UndoManager { get; } = new();

    /// <summary>Grid overlay line segments for WPF binding.</summary>
    public ObservableCollection<GridLineSegment> GridOverlayLines { get; } = new();

    // Theme names for dropdown
    public IReadOnlyList<string> ThemeNames => Services.ThemeService.ThemeNames;

    [ObservableProperty]
    private string _selectedTheme = Services.ThemeService.CurrentTheme;

    [ObservableProperty]
    private bool _isDirty;

    /// <summary>Secondary color for swap (X key).</summary>
    [ObservableProperty]
    private PixelColor _secondaryColor = new(255, 255, 255, 255);

    /// <summary>Recent colors (last 8 picked).</summary>
    public ObservableCollection<PixelColor> RecentColors { get; } = new();

    [ObservableProperty]
    private int _brushSize = 1;
    partial void OnBrushSizeChanged(int value)
    {
        int size = Math.Clamp(value, 1, 32);
        BrushTool.Size = size;
        EraserTool.Size = size;
    }

    /// <summary>
    /// Callback to show New Canvas dialog. Set by the View. Returns (Width, Height) or null if cancelled.
    /// </summary>
    public Func<(int Width, int Height)?>? RequestNewCanvasSize { get; set; }

    /// <summary>Callback to confirm discarding unsaved changes. Returns true to proceed, false to cancel.</summary>
    public Func<string, string, bool>? ConfirmDiscardUnsaved { get; set; }

    /// <summary>Callback to toggle fullscreen. Set by the View.</summary>
    public Action? ToggleFullscreenRequested { get; set; }

    /// <summary>Callback to get canvas area size for Fit zoom. Set by the View.</summary>
    public Func<(double Width, double Height)>? GetCanvasAreaSize { get; set; }

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
        EyedropperTool.ColorPicked += color =>
        {
            SecondaryColor = CurrentColor;
            CurrentColor = color;
            AddToRecentColors(color);
        };
        
        // Default to first palette (SNES Classic)
        if (AvailablePalettes.Count > 0)
            SelectedPalette = AvailablePalettes[0];
        
        UndoManager.StackChanged += NotifyUndoRedoCanExecute;
        NotifyUndoRedoCanExecute();
        Canvas.ActiveLayerIndexChanged += NotifyLayerCommandsCanExecute;
        NotifyLayerCommandsCanExecute();
        
        // Initial render
        UpdateBitmap();
        RefreshGridOverlay();
    }

    partial void OnCanvasChanged(PixelCanvas value)
    {
        RefreshGridOverlay();
        if (value != null)
            value.ActiveLayerIndexChanged += NotifyLayerCommandsCanExecute;
    }

    partial void OnShowGridChanged(bool value) => RefreshGridOverlay();

    private void NotifyLayerCommandsCanExecute()
    {
        RemoveLayerCommand.NotifyCanExecuteChanged();
        MoveLayerUpCommand.NotifyCanExecuteChanged();
        MoveLayerDownCommand.NotifyCanExecuteChanged();
    }

    private void RefreshGridOverlay()
    {
        GridOverlayLines.Clear();
        if (!ShowGrid || Canvas == null) return;
        int w = Canvas.Width;
        int h = Canvas.Height;
        for (int x = 1; x < w; x++)
            GridOverlayLines.Add(new GridLineSegment(x, 0, x, h));
        for (int y = 1; y < h; y++)
            GridOverlayLines.Add(new GridLineSegment(0, y, w, y));
    }
    
    partial void OnCurrentToolChanged(ITool value) => UpdateStatusWithTool(CurrentTool);

    private void UpdateStatusWithTool(ITool tool)
    {
        if (tool == null) return;
        string key = tool == BrushTool ? "B" : tool == EraserTool ? "E" : tool == FillTool ? "F" : tool == EyedropperTool ? "I"
            : tool == LineTool ? "L" : tool == RectangleTool ? "R" : tool == CircleTool ? "C" : tool == PanTool ? "P"
            : tool == SelectionTool ? "S" : tool == MoveTool ? "M" : "";
        StatusText = string.IsNullOrEmpty(key) ? tool.Name : $"{tool.Name} ({key})";
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

    private bool CanCopy() => SelectionManager.HasSelection;
    private bool CanCut() => SelectionManager.HasSelection;
    private bool CanPaste() => SelectionManager.ClipboardBuffer != null;
    private bool CanDeleteSelection() => SelectionManager.HasSelection;

    private void NotifyClipboardCommandsCanExecute()
    {
        CopyCommand.NotifyCanExecuteChanged();
        CutCommand.NotifyCanExecuteChanged();
        PasteCommand.NotifyCanExecuteChanged();
        DeleteCommand.NotifyCanExecuteChanged();
    }

    [RelayCommand(CanExecute = nameof(CanCopy))]
    private void Copy()
    {
        if (SelectionManager.HasSelection) SelectionManager.Copy();
        PasteCommand.NotifyCanExecuteChanged();
    }

    [RelayCommand(CanExecute = nameof(CanCut))]
    private void Cut()
    {
        if (!SelectionManager.HasSelection) return;
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        SelectionManager.Copy();
        ClearSelectionPixels(layer);
        SelectionManager.ClearSelection();
        NotifyClipboardCommandsCanExecute();
        UpdateBitmap();
    }

    [RelayCommand(CanExecute = nameof(CanPaste))]
    private void Paste()
    {
        if (SelectionManager.ClipboardBuffer == null) return;
        EnterPasteMode();
    }

    [RelayCommand(CanExecute = nameof(CanDeleteSelection))]
    private void Delete()
    {
        if (!SelectionManager.HasSelection) return;
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        ClearSelectionPixels(layer);
        SelectionManager.ClearSelection();
        NotifyClipboardCommandsCanExecute();
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
        SecondaryColor = CurrentColor;
        CurrentColor = color;
        AddToRecentColors(color);
        CurrentTool = BrushTool;
    }

    private void AddToRecentColors(PixelColor color)
    {
        // Remove if already present (move to front)
        for (int i = RecentColors.Count - 1; i >= 0; i--)
        {
            if (RecentColors[i].Equals(color)) RecentColors.RemoveAt(i);
        }
        RecentColors.Insert(0, color);
        while (RecentColors.Count > 8) RecentColors.RemoveAt(RecentColors.Count - 1);
    }

    [RelayCommand]
    private void SwapColors()
    {
        (CurrentColor, SecondaryColor) = (SecondaryColor, CurrentColor);
        StatusText = "Colors swapped (X)";
    }

    [RelayCommand]
    private void SelectRecentColor(PixelColor color)
    {
        CurrentColor = color;
        CurrentTool = BrushTool;
        StatusText = $"Selected #{color.R:X2}{color.G:X2}{color.B:X2}";
    }

    [RelayCommand]
    private void BrushSizeUp()
    {
        BrushSize = Math.Min(32, BrushSize + 1);
        StatusText = $"Brush size: {BrushSize}px";
    }

    [RelayCommand]
    private void BrushSizeDown()
    {
        BrushSize = Math.Max(1, BrushSize - 1);
        StatusText = $"Brush size: {BrushSize}px";
    }

    /// <summary>Zoom in/out centered on cursor. delta &gt; 0 = zoom in.</summary>
    public void ZoomAtCursor(int delta, double cursorScreenX, double cursorScreenY)
    {
        int oldZoom = Zoom;
        int newZoom = Math.Clamp(Zoom + (delta > 0 ? 1 : -1), 1, 64);
        if (newZoom == oldZoom) return;
        double ratio = (double)newZoom / oldZoom;
        PanOffsetX = cursorScreenX * (ratio - 1) + PanOffsetX * ratio;
        PanOffsetY = cursorScreenY * (ratio - 1) + PanOffsetY * ratio;
        Zoom = newZoom;
        StatusText = $"{Zoom * 100}%";
    }

    [RelayCommand]
    private void FitToView()
    {
        var (w, h) = GetCanvasAreaSize?.Invoke() ?? (800, 600);
        if (w <= 0 || h <= 0 || Canvas == null) return;
        int cw = Canvas.Width;
        int ch = Canvas.Height;
        double scaleX = w / (double)cw;
        double scaleY = h / (double)ch;
        int fitZoom = (int)Math.Floor(Math.Min(scaleX, scaleY));
        Zoom = Math.Clamp(Math.Max(1, fitZoom), 1, 64);
        PanOffsetX = 0;
        PanOffsetY = 0;
        StatusText = $"Fit: {Zoom * 100}%";
    }

    [RelayCommand]
    private void Zoom100()
    {
        Zoom = 1;
        PanOffsetX = 0;
        PanOffsetY = 0;
        StatusText = "100%";
    }

    [RelayCommand]
    private void QuickExport()
    {
        var path = System.IO.Path.Combine(
            Environment.GetFolderPath(Environment.SpecialFolder.Desktop),
            $"Canvas {Canvas.Width}x{Canvas.Height}.png");
        try
        {
            int scale = Math.Clamp(ExportScale, 1, 8);
            FileService.ExportToPng(Canvas, path, scale);
            IsDirty = false;
            StatusText = $"Quick export {scale}× → Desktop";
        }
        catch (Exception ex)
        {
            StatusText = $"Export failed: {ex.Message}";
        }
    }

    partial void OnSelectedThemeChanged(string value)
    {
        Services.ThemeService.ApplyTheme(value);
    }

    [RelayCommand]
    private void ToggleGrid()
    {
        ShowGrid = !ShowGrid;
        RefreshGridOverlay();
    }
    
    [RelayCommand]
    private void NewCanvas()
    {
        if (IsDirty && ConfirmDiscardUnsaved != null)
        {
            if (!ConfirmDiscardUnsaved("Unsaved changes", "Discard changes and create new canvas?"))
                return;
        }
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
        IsDirty = false;

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

    private bool CanUndo() => UndoManager.CanUndo;
    private bool CanRedo() => UndoManager.CanRedo;
    private void NotifyUndoRedoCanExecute()
    {
        UndoCommand.NotifyCanExecuteChanged();
        RedoCommand.NotifyCanExecuteChanged();
    }

    [RelayCommand(CanExecute = nameof(CanUndo))]
    private void Undo()
    {
        UndoManager.Undo();
        UpdateBitmap();
    }

    [RelayCommand(CanExecute = nameof(CanRedo))]
    private void Redo()
    {
        UndoManager.Redo();
        UpdateBitmap();
    }

    [RelayCommand]
    private void Escape()
    {
        if (_isPasteMode)
        {
            _isPasteMode = false;
            StatusText = "Paste cancelled";
            UpdateBitmap();
        }
        else if (SelectionManager.HasSelection)
        {
            var layer = Canvas.ActiveLayer;
            if (layer != null) ClearSelectionPixels(layer);
            SelectionManager.ClearSelection();
            NotifyClipboardCommandsCanExecute();
            StatusText = "Selection cleared";
            UpdateBitmap();
        }
    }

    [RelayCommand]
    private void ToggleFullscreen()
    {
        ToggleFullscreenRequested?.Invoke();
    }

    [RelayCommand]
    private void Save()
    {
        var saveFileDialog = new SaveFileDialog
        {
            Filter = "PNG Image (*.png)|*.png|All Files (*.*)|*.*",
            DefaultExt = "png",
            Title = "Export Image",
            FileName = $"Canvas {Canvas.Width}x{Canvas.Height}.png"
        };

        if (saveFileDialog.ShowDialog() == true)
        {
            try
            {
                int scale = Math.Clamp(ExportScale, 1, 8);
                FileService.ExportToPng(Canvas, saveFileDialog.FileName, scale);
                IsDirty = false;
                StatusText = $"Saved {scale}× to {System.IO.Path.GetFileName(saveFileDialog.FileName)}";
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

    private bool CanRemoveLayer() => Canvas?.Layers.Count > 1;

    [RelayCommand(CanExecute = nameof(CanRemoveLayer))]
    private void RemoveLayer()
    {
        if (Canvas.Layers.Count <= 1) return;
        Canvas.RemoveLayer(Canvas.ActiveLayerIndex);
        StatusText = "Layer removed";
        UpdateBitmap();
    }

    [RelayCommand]
    private void DuplicateLayer()
    {
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        var clone = layer.Clone();
        clone.Name = $"Layer {Canvas.Layers.Count + 1} (copy)";
        Canvas.InsertLayer(Canvas.ActiveLayerIndex + 1, clone);
        StatusText = "Layer duplicated";
        UpdateBitmap();
    }

    private bool CanMoveLayerUp() => Canvas?.ActiveLayerIndex > 0;

    [RelayCommand(CanExecute = nameof(CanMoveLayerUp))]
    private void MoveLayerUp()
    {
        if (Canvas.ActiveLayerIndex <= 0) return;
        Canvas.MoveLayerUp(Canvas.ActiveLayerIndex);
        StatusText = "Layer moved up";
    }

    private bool CanMoveLayerDown() => Canvas != null && Canvas.ActiveLayerIndex >= 0 && Canvas.ActiveLayerIndex < Canvas.Layers.Count - 1;

    [RelayCommand(CanExecute = nameof(CanMoveLayerDown))]
    private void MoveLayerDown()
    {
        if (Canvas.ActiveLayerIndex >= Canvas.Layers.Count - 1) return;
        Canvas.MoveLayerDown(Canvas.ActiveLayerIndex);
        StatusText = "Layer moved down";
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
            StatusText = $"Click to place at ({canvasX}, {canvasY}) | {Zoom * 100}%";
            return;
        }
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        
        if (isPressed)
        {
            CurrentTool.OnMouseMove(layer, canvasX, canvasY, CurrentColor);
            UpdateBitmap();
        }
        
        StatusText = $"({canvasX}, {canvasY}) | {Zoom * 100}%";
    }
    
    public void AddPanDelta(double deltaX, double deltaY)
    {
        PanOffsetX += deltaX;
        PanOffsetY += deltaY;
    }

    /// <summary>Right-click eyedropper: pick composite color at canvas position.</summary>
    public void HandleRightClick(int canvasX, int canvasY)
    {
        if (Canvas == null) return;
        var color = Canvas.GetCompositePixel(canvasX, canvasY);
        if (color.IsTransparent) return;
        SecondaryColor = CurrentColor;
        CurrentColor = color;
        AddToRecentColors(color);
        StatusText = $"Picked #{color.R:X2}{color.G:X2}{color.B:X2}";
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

        // Grid drawn as WPF overlay, not in pixel buffer

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

/// <summary>Line segment for grid overlay binding.</summary>
public record GridLineSegment(double X1, double Y1, double X2, double Y2);

using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PixelPerfect.Core;
using System.Collections.ObjectModel;
using System.Windows.Media;
using System.Windows.Media.Imaging;

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
    
    // Tools
    public BrushTool BrushTool { get; } = new();
    public EraserTool EraserTool { get; } = new();
    public FillTool FillTool { get; } = new();
    public EyedropperTool EyedropperTool { get; } = new();
    
    // Zoom levels
    public int[] ZoomLevels { get; } = { 1, 2, 4, 8, 16, 24, 32, 48, 64 };
    
    public MainViewModel()
    {
        _canvas = new PixelCanvas(32, 32);
        _currentTool = BrushTool;
        
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
    private void NewCanvas()
    {
        Canvas = new PixelCanvas(32, 32);
        UpdateBitmap();
        StatusText = "New canvas created";
    }
    
    [RelayCommand]
    private void AddLayer()
    {
        Canvas.AddLayer($"Layer {Canvas.Layers.Count + 1}");
        StatusText = $"Added layer {Canvas.Layers.Count}";
    }
    
    public void HandleMouseDown(int canvasX, int canvasY)
    {
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        
        CurrentTool.OnMouseDown(layer, canvasX, canvasY, CurrentColor);
        UpdateBitmap();
    }
    
    public void HandleMouseMove(int canvasX, int canvasY, bool isPressed)
    {
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        
        if (isPressed)
        {
            CurrentTool.OnMouseMove(layer, canvasX, canvasY, CurrentColor);
            UpdateBitmap();
        }
        
        StatusText = $"({canvasX}, {canvasY})";
    }
    
    public void HandleMouseUp(int canvasX, int canvasY)
    {
        var layer = Canvas.ActiveLayer;
        if (layer == null) return;
        
        CurrentTool.OnMouseUp(layer, canvasX, canvasY, CurrentColor);
    }
    
    /// <summary>
    /// Renders the canvas to a WriteableBitmap for display
    /// </summary>
    public void UpdateBitmap()
    {
        var flattened = Canvas.FlattenLayers();
        
        // Create or resize bitmap if needed
        if (CanvasBitmap == null || 
            CanvasBitmap.PixelWidth != Canvas.Width || 
            CanvasBitmap.PixelHeight != Canvas.Height)
        {
            CanvasBitmap = new WriteableBitmap(
                Canvas.Width, Canvas.Height,
                96, 96, PixelFormats.Bgra32, null);
        }
        
        // Write pixels to bitmap
        int stride = Canvas.Width * 4;
        byte[] pixels = new byte[Canvas.Height * stride];
        
        for (int y = 0; y < Canvas.Height; y++)
        {
            for (int x = 0; x < Canvas.Width; x++)
            {
                var color = flattened[y, x];
                int offset = y * stride + x * 4;
                pixels[offset] = color.B;     // Blue
                pixels[offset + 1] = color.G; // Green
                pixels[offset + 2] = color.R; // Red
                pixels[offset + 3] = color.A; // Alpha
            }
        }
        
        CanvasBitmap.WritePixels(
            new System.Windows.Int32Rect(0, 0, Canvas.Width, Canvas.Height),
            pixels, stride, 0);
    }
}

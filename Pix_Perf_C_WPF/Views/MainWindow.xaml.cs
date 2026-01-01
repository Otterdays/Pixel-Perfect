using System.Windows;
using System.Windows.Input;
using PixelPerfect.ViewModels;

namespace PixelPerfect.Views;

/// <summary>
/// Main window code-behind for canvas mouse handling
/// </summary>
public partial class MainWindow : Window
{
    private MainViewModel ViewModel => (MainViewModel)DataContext;
    private bool _isMouseDown;
    
    public MainWindow()
    {
        InitializeComponent();
    }
    
    private void CanvasImage_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (e.LeftButton == MouseButtonState.Pressed)
        {
            _isMouseDown = true;
            var pos = GetCanvasPosition(e);
            if (pos.HasValue)
            {
                ViewModel.HandleMouseDown(pos.Value.x, pos.Value.y);
            }
            
            // Capture mouse for drawing outside bounds
            CanvasImage.CaptureMouse();
        }
    }
    
    private void CanvasImage_MouseMove(object sender, MouseEventArgs e)
    {
        var pos = GetCanvasPosition(e);
        if (pos.HasValue)
        {
            ViewModel.HandleMouseMove(pos.Value.x, pos.Value.y, _isMouseDown);
        }
    }
    
    private void CanvasImage_MouseUp(object sender, MouseButtonEventArgs e)
    {
        if (_isMouseDown)
        {
            _isMouseDown = false;
            var pos = GetCanvasPosition(e);
            if (pos.HasValue)
            {
                ViewModel.HandleMouseUp(pos.Value.x, pos.Value.y);
            }
            
            CanvasImage.ReleaseMouseCapture();
        }
    }
    
    /// <summary>
    /// Converts screen position to canvas pixel coordinates
    /// </summary>
    private (int x, int y)? GetCanvasPosition(MouseEventArgs e)
    {
        var point = e.GetPosition(CanvasImage);
        
        // Account for zoom scaling
        int x = (int)(point.X / ViewModel.Zoom);
        int y = (int)(point.Y / ViewModel.Zoom);
        
        // Bounds check
        if (x >= 0 && x < ViewModel.Canvas.Width && 
            y >= 0 && y < ViewModel.Canvas.Height)
        {
            return (x, y);
        }
        
        return null;
    }
}

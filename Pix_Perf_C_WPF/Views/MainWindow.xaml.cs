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
    private bool _isPanning;
    private Point _panStartPoint;
    
    public MainWindow()
    {
        InitializeComponent();
        var vm = new MainViewModel();
        vm.RequestNewCanvasSize = () =>
        {
            var dialog = new NewCanvasDialog();
            return dialog.ShowDialog() == true ? (dialog.CanvasWidth, dialog.CanvasHeight) : null;
        };
        DataContext = vm;
    }
    
    private void CanvasImage_MouseDown(object sender, MouseButtonEventArgs e)
    {
        if (e.MiddleButton == MouseButtonState.Pressed)
        {
            StartPan(e);
            return;
        }
        if (e.LeftButton == MouseButtonState.Pressed)
        {
            if (Keyboard.Modifiers == ModifierKeys.None && ViewModel.CurrentTool == ViewModel.PanTool)
            {
                StartPan(e);
                return;
            }
            if (Keyboard.IsKeyDown(Key.Space))
            {
                StartPan(e);
                return;
            }
            _isMouseDown = true;
            var pos = GetCanvasPosition(e);
            if (pos.HasValue)
            {
                ViewModel.HandleMouseDown(pos.Value.x, pos.Value.y);
            }
            CanvasImage.CaptureMouse();
        }
    }
    
    private void CanvasImage_MouseMove(object sender, MouseEventArgs e)
    {
        if (_isPanning)
        {
            var current = e.GetPosition(CanvasImage);
            var deltaX = current.X - _panStartPoint.X;
            var deltaY = current.Y - _panStartPoint.Y;
            ViewModel.AddPanDelta(deltaX, deltaY);
            _panStartPoint = current;
            return;
        }
        if (Keyboard.IsKeyDown(Key.Space) && e.LeftButton == MouseButtonState.Pressed && !_isMouseDown)
        {
            StartPan(e);
            return;
        }
        var pos = GetCanvasPosition(e);
        if (pos.HasValue)
        {
            ViewModel.HandleMouseMove(pos.Value.x, pos.Value.y, _isMouseDown);
        }
    }
    
    private void CanvasImage_MouseUp(object sender, MouseButtonEventArgs e)
    {
        if (_isPanning && (e.ChangedButton == MouseButton.Middle || e.ChangedButton == MouseButton.Left))
        {
            _isPanning = false;
            CanvasImage.ReleaseMouseCapture();
            return;
        }
        if (_isMouseDown && e.LeftButton == MouseButtonState.Released)
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

    private void StartPan(MouseEventArgs e)
    {
        _isPanning = true;
        _panStartPoint = e.GetPosition(CanvasImage);
        CanvasImage.CaptureMouse();
    }
    
    /// <summary>
    /// Converts screen position to canvas pixel coordinates
    /// </summary>
    private (int x, int y)? GetCanvasPosition(MouseEventArgs e)
    {
        var point = e.GetPosition(CanvasImage);
        
        // Account for zoom scaling properly using floor to avoid integer division clipping near zero
        int x = (int)System.Math.Floor(point.X / ViewModel.Zoom);
        int y = (int)System.Math.Floor(point.Y / ViewModel.Zoom);
        
        // We no longer abort for out-of-bounds. We want the coordinates passed back
        // so tools like Brush/Eraser can perform flawless Bresenham-line interpolations
        // even if the user swiftly drags the mouse outside the canvas and curves back in.
        return (x, y);
    }
}

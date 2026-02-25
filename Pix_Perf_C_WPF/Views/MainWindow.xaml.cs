using System;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;
using PixelPerfect.Services;
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
    private bool _isRightPanning;
    private Point _panStartPoint;
    private Point _rightButtonDownPoint;
    
    public MainWindow()
    {
        InitializeComponent();
        var vm = new MainViewModel();
        vm.RequestNewCanvasSize = () =>
        {
            var dialog = new NewCanvasDialog();
            return dialog.ShowDialog() == true ? (dialog.CanvasWidth, dialog.CanvasHeight) : null;
        };
        vm.ToggleFullscreenRequested = () =>
        {
            WindowState = WindowState == WindowState.Maximized ? WindowState.Normal : WindowState.Maximized;
        };
        vm.GetCanvasAreaSize = () =>
        {
            var area = CanvasArea;
            return area != null ? (area.ActualWidth, area.ActualHeight) : (0.0, 0.0);
        };
        vm.ConfirmDiscardUnsaved = (title, message) =>
            MessageBox.Show(message, title, MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.Yes;
        DataContext = vm;
    }
    
    private void CanvasImage_MouseRightButtonDown(object sender, MouseButtonEventArgs e)
    {
        _rightButtonDownPoint = e.GetPosition(CanvasImage);
    }

    private void CanvasImage_MouseRightButtonUp(object sender, MouseButtonEventArgs e)
    {
        if (_isRightPanning)
        {
            e.Handled = true;
            _isRightPanning = false;
        }
        else
        {
            // Right-click without drag = eyedropper. Shift+Right-click = context menu.
            if (Keyboard.Modifiers != ModifierKeys.Shift)
            {
                var pos = GetCanvasPosition(e);
                if (pos.HasValue)
                {
                    ViewModel.HandleRightClick(pos.Value.x, pos.Value.y);
                    e.Handled = true;
                }
            }
        }
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
        if (e.RightButton == MouseButtonState.Pressed && !_isRightPanning && !_isPanning)
        {
            var current = e.GetPosition(CanvasImage);
            var dx = current.X - _rightButtonDownPoint.X;
            var dy = current.Y - _rightButtonDownPoint.Y;
            if (Math.Abs(dx) > 5 || Math.Abs(dy) > 5)
            {
                _isRightPanning = true;
                StartPan(e);
                return;
            }
        }
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
        if (_isPanning && (e.ChangedButton == MouseButton.Middle || e.ChangedButton == MouseButton.Left || e.ChangedButton == MouseButton.Right))
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

    private void CanvasArea_PreviewMouseWheel(object sender, MouseWheelEventArgs e)
    {
        if (Keyboard.Modifiers != ModifierKeys.Control) return;
        e.Handled = true;
        var pos = e.GetPosition(CanvasArea);
        double centerX = CanvasArea.ActualWidth / 2;
        double centerY = CanvasArea.ActualHeight / 2;
        ViewModel.Zoom += e.Delta > 0 ? 1 : -1;
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
        
        // GetPosition already handles inverse scaling and panning due to LayoutTransform
        int x = (int)System.Math.Floor(point.X);
        int y = (int)System.Math.Floor(point.Y);
        
        // We no longer abort for out-of-bounds. We want the coordinates passed back
        // so tools like Brush/Eraser can perform flawless Bresenham-line interpolations
        // even if the user swiftly drags the mouse outside the canvas and curves back in.
        return (x, y);
    }

}

using System;
using System.Collections.Generic;
using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Media3D;
using System.Windows.Threading;
using PixelPerfect.Core;

namespace PixelPerfect.Views
{
    public partial class TokenPreviewWindow : Window
    {
        private PixelCanvas _canvas;
        private double _thickness = 1.0;
        private DispatcherTimer _timer;
        private Point _lastMousePosition;
        private bool _isDragging;

        public TokenPreviewWindow(PixelCanvas canvas)
        {
            InitializeComponent();
            _canvas = canvas;

            _timer = new DispatcherTimer();
            _timer.Interval = TimeSpan.FromMilliseconds(16);
            _timer.Tick += Timer_Tick;
            _timer.Start();
        }

        private void Window_Loaded(object sender, RoutedEventArgs e)
        {
            BuildModel();
        }

        private void BuildModel()
        {
            VoxelModelGroup.Children.Clear();
            int w = _canvas.Width;
            int h = _canvas.Height;
            byte[] flattened = new byte[w * h * 4];
            _canvas.FlattenToBuffer(flattened);

            // Group by color to reduce Memory and Draw calls
            var colorMeshes = new Dictionary<Color, MeshGeometry3D>();

            for (int y = 0; y < h; y++)
            {
                for (int x = 0; x < w; x++)
                {
                    int index = (y * w + x) * 4;
                    byte a = flattened[index + 3];
                    if (a > 0)
                    {
                        byte b = flattened[index + 0];
                        byte g = flattened[index + 1];
                        byte r = flattened[index + 2];
                        Color color = Color.FromArgb(a, r, g, b);

                        if (!colorMeshes.ContainsKey(color))
                        {
                            colorMeshes[color] = new MeshGeometry3D();
                        }

                        // Center the model
                        double px = x - w / 2.0;
                        double py = (h - y) - h / 2.0; // Invert Y for 3D
                        AddCube(colorMeshes[color], px, py, 0, 1.0, 1.0, _thickness);
                    }
                }
            }

            foreach (var kvp in colorMeshes)
            {
                var material = new DiffuseMaterial(new SolidColorBrush(kvp.Key));
                var geometryModel = new GeometryModel3D(kvp.Value, material);
                VoxelModelGroup.Children.Add(geometryModel);
            }

            // Adjust camera position based on resolution
            MainCamera.Position = new Point3D(0, 0, Math.Max(w, h) * 1.5);
        }

        private void AddCube(MeshGeometry3D mesh, double x, double y, double z, double sx, double sy, double sz)
        {
            double halfX = sx / 2;
            double halfY = sy / 2;
            double halfZ = sz / 2;

            int startIndex = mesh.Positions.Count;

            Point3D p0 = new Point3D(x - halfX, y - halfY, z + halfZ);
            Point3D p1 = new Point3D(x + halfX, y - halfY, z + halfZ);
            Point3D p2 = new Point3D(x + halfX, y + halfY, z + halfZ);
            Point3D p3 = new Point3D(x - halfX, y + halfY, z + halfZ);
            Point3D p4 = new Point3D(x - halfX, y - halfY, z - halfZ);
            Point3D p5 = new Point3D(x + halfX, y - halfY, z - halfZ);
            Point3D p6 = new Point3D(x + halfX, y + halfY, z - halfZ);
            Point3D p7 = new Point3D(x - halfX, y + halfY, z - halfZ);

            mesh.Positions.Add(p0); mesh.Positions.Add(p1); mesh.Positions.Add(p2); mesh.Positions.Add(p3);
            mesh.Positions.Add(p4); mesh.Positions.Add(p5); mesh.Positions.Add(p6); mesh.Positions.Add(p7);

            // Front (0,1,2,3)
            AddFaceIndices(mesh, startIndex, 0, 1, 2, 3);
            // Back (5,4,7,6)
            AddFaceIndices(mesh, startIndex, 5, 4, 7, 6);
            // Top (3,2,6,7)
            AddFaceIndices(mesh, startIndex, 3, 2, 6, 7);
            // Bottom (4,5,1,0)
            AddFaceIndices(mesh, startIndex, 4, 5, 1, 0);
            // Left (4,0,3,7)
            AddFaceIndices(mesh, startIndex, 4, 0, 3, 7);
            // Right (1,5,6,2)
            AddFaceIndices(mesh, startIndex, 1, 5, 6, 2);
        }

        private void AddFaceIndices(MeshGeometry3D mesh, int start, int a, int b, int c, int d)
        {
            mesh.TriangleIndices.Add(start + a);
            mesh.TriangleIndices.Add(start + b);
            mesh.TriangleIndices.Add(start + c);
            mesh.TriangleIndices.Add(start + a);
            mesh.TriangleIndices.Add(start + c);
            mesh.TriangleIndices.Add(start + d);
        }

        private void Controls_ValueChanged(object sender, RoutedPropertyChangedEventArgs<double> e)
        {
            if (VoxelModelGroup == null) return;
            _thickness = ThicknessSlider.Value;
            BuildModel();
            
            // Reapply rotations
            ModelRotationX.Angle = _lastRotX;
            ModelRotationY.Angle = _lastRotY;
        }

        private double _lastRotX = 0;
        private double _lastRotY = 0;

        private void AutoSpin_Checked(object sender, RoutedEventArgs e)
        {
            if (_timer != null) _timer.Start();
        }

        private void AutoSpin_Unchecked(object sender, RoutedEventArgs e)
        {
             // Do not stop timer immediately if we only skip logic, but stopping is safer for CPU
        }

        private void Timer_Tick(object? sender, EventArgs e)
        {
            if (AutoSpinCheck.IsChecked == true && !_isDragging)
            {
                ModelRotationY.Angle += 1;
                if (ModelRotationY.Angle >= 360) ModelRotationY.Angle -= 360;
                _lastRotY = ModelRotationY.Angle;
                _lastRotX = ModelRotationX.Angle;
            }
        }

        private void Viewport_MouseDown(object sender, MouseButtonEventArgs e)
        {
            _isDragging = true;
            _lastMousePosition = e.GetPosition(this);
            Viewport.CaptureMouse();
        }

        private void Viewport_MouseMove(object sender, MouseEventArgs e)
        {
            if (_isDragging)
            {
                Point currentPos = e.GetPosition(this);
                double deltaX = currentPos.X - _lastMousePosition.X;
                double deltaY = currentPos.Y - _lastMousePosition.Y;
                
                ModelRotationY.Angle += deltaX * 0.5;
                ModelRotationX.Angle += deltaY * 0.5;

                _lastRotX = ModelRotationX.Angle;
                _lastRotY = ModelRotationY.Angle;

                _lastMousePosition = currentPos;
            }
        }

        private void Viewport_MouseUp(object sender, MouseButtonEventArgs e)
        {
            _isDragging = false;
            Viewport.ReleaseMouseCapture();
        }

        private void Viewport_MouseWheel(object sender, MouseWheelEventArgs e)
        {
            double scale = e.Delta > 0 ? 0.9 : 1.1;
            MainCamera.Position = new Point3D(MainCamera.Position.X, MainCamera.Position.Y, MainCamera.Position.Z * scale);
        }

        private void ResetView_Click(object sender, RoutedEventArgs e)
        {
            ModelRotationX.Angle = 0;
            ModelRotationY.Angle = 0;
            _lastRotX = 0;
            _lastRotY = 0;

            int w = _canvas.Width;
            int h = _canvas.Height;
            MainCamera.Position = new Point3D(0, 0, Math.Max(w, h) * 1.5);
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            this.Close();
        }
    }
}

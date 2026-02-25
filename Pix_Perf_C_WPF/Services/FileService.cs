using System;
using System.IO;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using PixelPerfect.Core;

namespace PixelPerfect.Services;

/// <summary>
/// Handles exporting, saving, and importing projects
/// </summary>
public static class FileService
{
    private const int MaxImportDimension = 512;

    /// <summary>
    /// Imports a PNG file into a new PixelCanvas. Scales down if larger than MaxImportDimension.
    /// </summary>
    public static PixelCanvas? ImportFromPng(string filePath)
    {
        try
        {
            var bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.UriSource = new Uri(System.IO.Path.GetFullPath(filePath), UriKind.Absolute);
            bitmap.CacheOption = BitmapCacheOption.OnLoad;
            bitmap.EndInit();
            bitmap.Freeze();

            int w = bitmap.PixelWidth;
            int h = bitmap.PixelHeight;
            if (w <= 0 || h <= 0) return null;

            int scale = 1;
            while (w / scale > MaxImportDimension || h / scale > MaxImportDimension)
                scale *= 2;

            int outW = w / scale;
            int outH = h / scale;

            var canvas = new PixelCanvas(outW, outH);
            var layer = canvas.ActiveLayer;
            if (layer == null) return null;

            var source = bitmap.Format == PixelFormats.Bgra32 || bitmap.Format == PixelFormats.Bgr32
                ? bitmap
                : (BitmapSource)new FormatConvertedBitmap(bitmap, PixelFormats.Bgra32, null, 0);
            CopyPixelsToLayer(source, layer, scale);

            return canvas;
        }
        catch
        {
            return null;
        }
    }

    private static void CopyPixelsToLayer(BitmapSource source, Layer layer, int scale)
    {
        int w = source.PixelWidth;
        int h = source.PixelHeight;
        int stride = w * 4;
        var buffer = new byte[h * stride];
        source.CopyPixels(buffer, stride, 0);

        for (int y = 0; y < layer.Height; y++)
        {
            for (int x = 0; x < layer.Width; x++)
            {
                int srcX = x * scale;
                int srcY = y * scale;
                if (srcX >= w || srcY >= h) continue;
                int offset = (srcY * w + srcX) * 4;
                byte b = buffer[offset];
                byte g = buffer[offset + 1];
                byte r = buffer[offset + 2];
                byte a = buffer[offset + 3];
                layer.SetPixel(x, y, new PixelColor(r, g, b, a));
            }
        }
    }

    /// <summary>
    /// Exports a pixel canvas to a PNG file with an optional scale factor.
    /// Uses NearestNeighbor scaling to preserve crisp pixel edges.
    /// </summary>
    public static void ExportToPng(PixelCanvas canvas, string filePath, int scale = 1)
    {
        if (scale < 1) scale = 1;

        int width = canvas.Width;
        int height = canvas.Height;
        int scaledWidth = width * scale;
        int scaledHeight = height * scale;

        // Flatten the image to get pixel data
        byte[] buffer = new byte[width * height * 4];
        canvas.FlattenToBuffer(buffer);

        // Create the base unscaled bitmap
        var writeableBitmap = new WriteableBitmap(
            width, height, 96, 96, PixelFormats.Bgra32, null);
        
        writeableBitmap.WritePixels(
            new System.Windows.Int32Rect(0, 0, width, height),
            buffer, width * 4, 0);

        BitmapSource finalSource = writeableBitmap;

        // Scale if needed
        if (scale > 1)
        {
            var scaleTransform = new ScaleTransform(scale, scale);
            // NearestNeighbor logic is guaranteed by TransformedBitmap when using RenderOptions, but we can also do:
            finalSource = new TransformedBitmap(writeableBitmap, scaleTransform);
            
            // Note: TransformedBitmap might antialias depending on WPF internals if we aren't careful, 
            // but the safest approach for pixel art scale up is writing an explicit scaled buffer:
            byte[] scaledBuffer = new byte[scaledWidth * scaledHeight * 4];
            for (int y = 0; y < scaledHeight; y++)
            {
                int srcY = y / scale;
                for (int x = 0; x < scaledWidth; x++)
                {
                    int srcX = x / scale;
                    int srcOffset = (srcY * width + srcX) * 4;
                    int dstOffset = (y * scaledWidth + x) * 4;
                    
                    scaledBuffer[dstOffset] = buffer[srcOffset];
                    scaledBuffer[dstOffset + 1] = buffer[srcOffset + 1];
                    scaledBuffer[dstOffset + 2] = buffer[srcOffset + 2];
                    scaledBuffer[dstOffset + 3] = buffer[srcOffset + 3];
                }
            }

            var scaledBitmap = new WriteableBitmap(
                scaledWidth, scaledHeight, 96, 96, PixelFormats.Bgra32, null);
            
            scaledBitmap.WritePixels(
                new System.Windows.Int32Rect(0, 0, scaledWidth, scaledHeight),
                scaledBuffer, scaledWidth * 4, 0);
            
            finalSource = scaledBitmap;
        }

        // Encode to PNG
        var encoder = new PngBitmapEncoder();
        encoder.Frames.Add(BitmapFrame.Create(finalSource));

        using var stream = new FileStream(filePath, FileMode.Create);
        encoder.Save(stream);
    }
}

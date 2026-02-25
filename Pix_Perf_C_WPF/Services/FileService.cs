using System;
using System.IO;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using PixelPerfect.Core;

namespace PixelPerfect.Services;

/// <summary>
/// Handles exporting and saving projects
/// </summary>
public static class FileService
{
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

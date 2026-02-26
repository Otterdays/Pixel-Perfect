using System;
using System.Globalization;
using System.Windows.Data;

namespace PixelPerfect.Converters;

/// <summary>
/// Converts zoom level to 1/zoom so that grid line thickness stays ~1 pixel after scale transform.
/// </summary>
public class InverseZoomConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is int zoom && zoom > 0)
            return 1.0 / zoom;
        return 1.0;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
        => throw new NotImplementedException();
}

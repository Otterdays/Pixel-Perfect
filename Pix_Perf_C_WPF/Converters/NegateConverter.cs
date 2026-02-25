using System;
using System.Globalization;
using System.Windows.Data;

namespace PixelPerfect.Converters;

public class NegateConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is double d)
            return -d;
        return 0.0;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is double d)
            return -d;
        return 0.0;
    }
}

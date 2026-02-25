using System;
using System.Globalization;
using System.Windows.Data;
using System.Windows.Media;
using PixelPerfect.Core;

namespace PixelPerfect.Converters;

public class PixelColorToBrushConverter : IValueConverter
{
    public object Convert(object value, Type targetType, object parameter, CultureInfo culture)
    {
        if (value is PixelColor pc)
        {
            return new SolidColorBrush(Color.FromArgb(pc.A, pc.R, pc.G, pc.B));
        }
        return Brushes.Transparent;
    }

    public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture)
    {
        throw new NotImplementedException();
    }
}

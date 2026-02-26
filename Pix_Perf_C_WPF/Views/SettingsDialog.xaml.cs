using System.Windows;
using System.Windows.Input;
using System.Windows.Media;
using PixelPerfect.ViewModels;

namespace PixelPerfect.Views;

public partial class SettingsDialog : Window
{
    private MainViewModel VM => (MainViewModel)DataContext;

    public SettingsDialog()
    {
        InitializeComponent();
    }

    private void PresetDark_Click(object sender, RoutedEventArgs e)
    {
        VM.GridColor = Color.FromRgb(0x40, 0x40, 0x40);
        VM.CheckerboardColor1 = Color.FromRgb(0x40, 0x40, 0x40);
        VM.CheckerboardColor2 = Color.FromRgb(0x50, 0x50, 0x50);
    }

    private void PresetLight_Click(object sender, RoutedEventArgs e)
    {
        VM.GridColor = Color.FromRgb(0x80, 0x80, 0x80);
        VM.CheckerboardColor1 = Color.FromRgb(0xc0, 0xc0, 0xc0);
        VM.CheckerboardColor2 = Color.FromRgb(0xd0, 0xd0, 0xd0);
    }

    private void PresetHighContrast_Click(object sender, RoutedEventArgs e)
    {
        VM.GridColor = Color.FromRgb(0x20, 0x20, 0x20);
        VM.CheckerboardColor1 = Color.FromRgb(0x30, 0x30, 0x30);
        VM.CheckerboardColor2 = Color.FromRgb(0x60, 0x60, 0x60);
    }

    private void OkButton_Click(object sender, RoutedEventArgs e)
    {
        DialogResult = true;
        Close();
    }
}

using System.Windows;
using System.Windows.Controls;

namespace PixelPerfect.Views;

public partial class NewCanvasDialog : Window
{
    private const string CustomPreset = "Custom...";
    
    public int CanvasWidth { get; private set; } = 32;
    public int CanvasHeight { get; private set; } = 32;
    
    private static readonly (int W, int H)[] Presets =
    {
        (8, 8), (16, 16), (32, 32), (16, 32), (32, 64), (64, 64), (128, 128), (256, 256)
    };
    
    public NewCanvasDialog()
    {
        InitializeComponent();
        Owner = Application.Current.MainWindow;
        
        PresetCombo.Items.Add("8×8 (Tiny)");
        PresetCombo.Items.Add("16×16 (Small)");
        PresetCombo.Items.Add("32×32 (Medium)");
        PresetCombo.Items.Add("16×32 (Wide)");
        PresetCombo.Items.Add("32×64 (Large)");
        PresetCombo.Items.Add("64×64 (Extra Large)");
        PresetCombo.Items.Add("128×128 (Huge)");
        PresetCombo.Items.Add("256×256 (Massive)");
        PresetCombo.Items.Add(CustomPreset);
        
        PresetCombo.SelectedIndex = 2;
    }
    
    private void PresetCombo_SelectionChanged(object sender, SelectionChangedEventArgs e)
    {
        if (PresetCombo.SelectedItem is string s && s == CustomPreset)
        {
            CustomSizePanel.Visibility = Visibility.Visible;
            WidthBox.Text = "32";
            HeightBox.Text = "32";
            WidthBox.Focus();
        }
        else
        {
            CustomSizePanel.Visibility = Visibility.Collapsed;
            if (PresetCombo.SelectedIndex >= 0 && PresetCombo.SelectedIndex < Presets.Length)
            {
                var (w, h) = Presets[PresetCombo.SelectedIndex];
                CanvasWidth = w;
                CanvasHeight = h;
            }
        }
    }
    
    private void OkButton_Click(object sender, RoutedEventArgs e)
    {
        if (CustomSizePanel.Visibility == Visibility.Visible)
        {
            if (!int.TryParse(WidthBox.Text, out int w) || !int.TryParse(HeightBox.Text, out int h))
            {
                MessageBox.Show("Please enter valid width and height (1-512).", "Invalid Size",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            if (w < 1 || w > 512 || h < 1 || h > 512)
            {
                MessageBox.Show("Width and height must be between 1 and 512.", "Invalid Size",
                    MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }
            CanvasWidth = w;
            CanvasHeight = h;
        }
        
        DialogResult = true;
        Close();
    }
}

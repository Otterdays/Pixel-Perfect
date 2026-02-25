using System;
using System.Windows;
using System.Windows.Threading;

namespace PixelPerfect;

/// <summary>
/// Application entry point
/// </summary>
public partial class App : Application
{
    protected override void OnStartup(StartupEventArgs e)
    {
        base.OnStartup(e);
        DispatcherUnhandledException += OnDispatcherUnhandledException;
        AppDomain.CurrentDomain.UnhandledException += OnUnhandledException;
    }

    private void OnDispatcherUnhandledException(object sender, DispatcherUnhandledExceptionEventArgs e)
    {
        var msg = FormatExceptionMessage(e.Exception);
        System.Diagnostics.Debug.WriteLine($"DispatcherUnhandledException: {e.Exception}");
        MessageBox.Show(msg, "Pixel Perfect - Error", MessageBoxButton.OK, MessageBoxImage.Error);
        e.Handled = true;
    }

    private void OnUnhandledException(object sender, UnhandledExceptionEventArgs e)
    {
        var ex = e.ExceptionObject as Exception;
        var msg = FormatExceptionMessage(ex) ?? e.ExceptionObject?.ToString() ?? "Unknown error";
        System.Diagnostics.Debug.WriteLine($"UnhandledException: {msg}");
        MessageBox.Show(msg, "Pixel Perfect - Error", MessageBoxButton.OK, MessageBoxImage.Error);
    }

    private static string FormatExceptionMessage(Exception? ex)
    {
        if (ex == null) return "An unknown error occurred.";
        var inner = ex.InnerException;
        var main = ex is System.Windows.Markup.XamlParseException && inner != null ? inner.Message : ex.Message;
        var stack = ex is System.Windows.Markup.XamlParseException && inner != null ? inner.StackTrace : ex.StackTrace;
        return $"An error occurred:\n\n{main}\n\n{stack}";
    }
}

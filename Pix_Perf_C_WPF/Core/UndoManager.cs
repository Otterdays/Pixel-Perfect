using System.Collections.Generic;

namespace PixelPerfect.Core;

public struct PixelDelta
{
    public Layer Layer { get; }
    public int X { get; }
    public int Y { get; }
    public PixelColor OldColor { get; }
    public PixelColor NewColor { get; set; }

    public PixelDelta(Layer layer, int x, int y, PixelColor oldColor, PixelColor newColor)
    {
        Layer = layer;
        X = x;
        Y = y;
        OldColor = oldColor;
        NewColor = newColor;
    }
}

public class UndoTransaction
{
    private readonly Dictionary<(Layer, int, int), PixelDelta> _deltas = new();

    public void AddDelta(Layer layer, int x, int y, PixelColor oldColor, PixelColor newColor)
    {
        var key = (layer, x, y);
        if (_deltas.TryGetValue(key, out var delta))
        {
            // Update the new color, keep the original old color
            delta.NewColor = newColor;
            _deltas[key] = delta;
        }
        else
        {
            _deltas[key] = new PixelDelta(layer, x, y, oldColor, newColor);
        }
    }

    public void Undo()
    {
        foreach (var delta in _deltas.Values)
        {
            delta.Layer.SetPixelRaw(delta.X, delta.Y, delta.OldColor);
        }
    }

    public void Redo()
    {
        foreach (var delta in _deltas.Values)
        {
            delta.Layer.SetPixelRaw(delta.X, delta.Y, delta.NewColor);
        }
    }

    public bool HasChanges => _deltas.Count > 0;
}

public class UndoManager
{
    private readonly List<UndoTransaction> _undoStack = new();
    private readonly Stack<UndoTransaction> _redoStack = new();
    private UndoTransaction? _currentTransaction;

    /// <summary>Max undo steps. Excess oldest entries are dropped. Default 100.</summary>
    public int MaxHistoryLimit { get; set; } = 100;

    /// <summary>Fired when undo/redo stacks change. Use to refresh command CanExecute.</summary>
    public event System.Action? StackChanged;

    public void BeginTransaction()
    {
        _currentTransaction = new UndoTransaction();
    }

    public void EndTransaction()
    {
        if (_currentTransaction != null && _currentTransaction.HasChanges)
        {
            _undoStack.Insert(0, _currentTransaction);
            while (_undoStack.Count > MaxHistoryLimit)
                _undoStack.RemoveAt(_undoStack.Count - 1);
            _redoStack.Clear();
            StackChanged?.Invoke();
        }
        _currentTransaction = null;
    }

    public void RecordPixelChange(Layer layer, int x, int y, PixelColor oldColor, PixelColor newColor)
    {
        _currentTransaction?.AddDelta(layer, x, y, oldColor, newColor);
    }

    public bool CanUndo => _undoStack.Count > 0;
    public bool CanRedo => _redoStack.Count > 0;

    public void Undo()
    {
        if (CanUndo)
        {
            var tx = _undoStack[0];
            _undoStack.RemoveAt(0);
            tx.Undo();
            _redoStack.Push(tx);
            StackChanged?.Invoke();
        }
    }

    public void Redo()
    {
        if (CanRedo)
        {
            var tx = _redoStack.Pop();
            tx.Redo();
            _undoStack.Insert(0, tx);
            StackChanged?.Invoke();
        }
    }

    public void Clear()
    {
        _undoStack.Clear();
        _redoStack.Clear();
        _currentTransaction = null;
        StackChanged?.Invoke();
    }
}

"""
Undo/redo system for Pixel Perfect
Manages state history for drawing operations
"""

import copy
from typing import List, Optional, Callable
import numpy as np

class UndoState:
    """Represents a state that can be undone"""
    
    def __init__(self, pixels: np.ndarray, layer_index: int):
        self.pixels = copy.deepcopy(pixels)
        self.layer_index = layer_index
        self.timestamp = None  # Could be used for auto-save timing

class UndoManager:
    """Manages undo/redo functionality"""
    
    def __init__(self, max_states: int = 50):
        self.max_states = max_states
        self.undo_stack: List[UndoState] = []
        self.redo_stack: List[UndoState] = []
        self.on_state_changed: Optional[Callable] = None
    
    def save_state(self, pixels: np.ndarray, layer_index: int):
        """Save current state for undo"""
        # Clear redo stack when new action is performed
        self.redo_stack.clear()
        
        # Create new state
        state = UndoState(pixels, layer_index)
        self.undo_stack.append(state)
        
        # Limit stack size
        if len(self.undo_stack) > self.max_states:
            self.undo_stack.pop(0)
        
        # Notify UI of state change
        if self.on_state_changed:
            self.on_state_changed()
    
    def undo(self, current_pixels: np.ndarray = None, current_layer_index: int = None) -> Optional[UndoState]:
        """Undo the last action"""
        if not self.undo_stack:
            return None
        
        # Save current state for redo if provided
        if current_pixels is not None and current_layer_index is not None:
            current_state = UndoState(current_pixels, current_layer_index)
            self.redo_stack.append(current_state)
        
        # Get the state to restore (previous state)
        state = self.undo_stack.pop()
        
        # Notify UI of state change
        if self.on_state_changed:
            self.on_state_changed()
        
        return state
    
    def redo(self, current_pixels: np.ndarray = None, current_layer_index: int = None) -> Optional[UndoState]:
        """Redo the last undone action"""
        if not self.redo_stack:
            return None
        
        # Save current state for undo if provided
        if current_pixels is not None and current_layer_index is not None:
            current_state = UndoState(current_pixels, current_layer_index)
            self.undo_stack.append(current_state)
        
        # Get the state to restore (the state we undid)
        state = self.redo_stack.pop()
        
        # Notify UI of state change
        if self.on_state_changed:
            self.on_state_changed()
        
        return state
    
    def can_undo(self) -> bool:
        """Check if undo is possible"""
        return len(self.undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is possible"""
        return len(self.redo_stack) > 0
    
    def clear(self):
        """Clear all undo/redo history"""
        self.undo_stack.clear()
        self.redo_stack.clear()
        
        if self.on_state_changed:
            self.on_state_changed()
    
    def get_undo_count(self) -> int:
        """Get number of available undo states"""
        return len(self.undo_stack)
    
    def get_redo_count(self) -> int:
        """Get number of available redo states"""
        return len(self.redo_stack)

"""
Event Throttling Utilities for Pixel Perfect
Provides throttling and debouncing for high-frequency events

OPTIMIZATION: Reduces CPU overhead from rapid mouse movements and
other high-frequency events by limiting how often handlers execute.
"""

import time
from typing import Callable, Optional, Any
from functools import wraps


class EventThrottler:
    """
    Throttles function calls to execute at most once per interval.
    
    Unlike debouncing (which waits for quiet period), throttling
    ensures the function executes immediately on first call, then
    limits subsequent calls to the specified interval.
    """
    
    def __init__(self, interval_ms: float = 16.0):
        """
        Args:
            interval_ms: Minimum time between executions in milliseconds.
                         Default 16ms (~60 FPS) for smooth visual updates.
        """
        self.interval_s = interval_ms / 1000.0
        self.last_call_time: float = 0.0
        self.pending_args: Optional[tuple] = None
        self.pending_kwargs: Optional[dict] = None
    
    def should_execute(self) -> bool:
        """Check if enough time has passed to execute again."""
        current_time = time.perf_counter()
        if current_time - self.last_call_time >= self.interval_s:
            self.last_call_time = current_time
            return True
        return False
    
    def throttle(self, func: Callable) -> Callable:
        """
        Decorator to throttle a function.
        
        Usage:
            throttler = EventThrottler(16)  # 60 FPS
            
            @throttler.throttle
            def on_mouse_move(x, y):
                # This will run at most 60 times per second
                update_preview(x, y)
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.should_execute():
                return func(*args, **kwargs)
            else:
                # Store pending call for potential later execution
                self.pending_args = args
                self.pending_kwargs = kwargs
                return None
        return wrapper
    
    def execute_pending(self, func: Callable) -> Any:
        """Execute any pending call that was throttled."""
        if self.pending_args is not None:
            result = func(*self.pending_args, **(self.pending_kwargs or {}))
            self.pending_args = None
            self.pending_kwargs = None
            return result
        return None


class RateLimiter:
    """
    Rate limiter for functions that shouldn't be called too frequently.
    
    Differs from throttler in that it tracks calls over a window
    rather than just the time since last call.
    """
    
    def __init__(self, max_calls: int, window_ms: float):
        """
        Args:
            max_calls: Maximum number of calls allowed in the window
            window_ms: Time window in milliseconds
        """
        self.max_calls = max_calls
        self.window_s = window_ms / 1000.0
        self.call_times: list = []
    
    def can_execute(self) -> bool:
        """Check if we're within rate limit."""
        current_time = time.perf_counter()
        
        # Remove old calls outside the window
        cutoff = current_time - self.window_s
        self.call_times = [t for t in self.call_times if t > cutoff]
        
        return len(self.call_times) < self.max_calls
    
    def record_call(self):
        """Record that a call was made."""
        self.call_times.append(time.perf_counter())
    
    def limit(self, func: Callable) -> Callable:
        """Decorator to rate-limit a function."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.can_execute():
                self.record_call()
                return func(*args, **kwargs)
            return None
        return wrapper


class CanvasEventOptimizer:
    """
    Optimized event handling specifically for canvas operations.
    
    Combines multiple optimization strategies:
    - Throttling for mouse move events
    - Pixel-position deduplication (don't redraw same pixel)
    - Batch update scheduling
    """
    
    def __init__(self, throttle_ms: float = 8.0):
        """
        Args:
            throttle_ms: Throttle interval for mouse events.
                         Default 8ms (~120 FPS) for responsive feel.
        """
        self.throttler = EventThrottler(throttle_ms)
        self.last_pixel_pos: Optional[tuple] = None
        self.pending_update: bool = False
        self._update_callback: Optional[Callable] = None
    
    def set_update_callback(self, callback: Callable):
        """Set the callback for batched updates."""
        self._update_callback = callback
    
    def should_process_move(self, pixel_x: int, pixel_y: int) -> bool:
        """
        Check if mouse move should be processed.
        
        Returns False if:
        - We're within the throttle interval AND
        - The pixel position hasn't changed
        """
        current_pos = (pixel_x, pixel_y)
        
        # Always process if position changed
        if current_pos != self.last_pixel_pos:
            self.last_pixel_pos = current_pos
            return True
        
        # Position same, check throttle
        return self.throttler.should_execute()
    
    def reset_position(self):
        """Reset tracked position (e.g., when mouse leaves canvas)."""
        self.last_pixel_pos = None
    
    def schedule_update(self, root, delay_ms: int = 16):
        """
        Schedule a batched update if one isn't already pending.
        
        This allows multiple rapid changes to be consolidated into
        a single redraw operation.
        """
        if not self.pending_update and self._update_callback:
            self.pending_update = True
            root.after(delay_ms, self._execute_update)
    
    def _execute_update(self):
        """Execute the pending update."""
        self.pending_update = False
        if self._update_callback:
            self._update_callback()


def throttle(interval_ms: float = 16.0):
    """
    Simple decorator factory for throttling functions.
    
    Usage:
        @throttle(33)  # 30 FPS
        def expensive_operation():
            ...
    """
    def decorator(func: Callable) -> Callable:
        last_call = [0.0]  # Use list to allow mutation in closure
        interval_s = interval_ms / 1000.0
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            current = time.perf_counter()
            if current - last_call[0] >= interval_s:
                last_call[0] = current
                return func(*args, **kwargs)
            return None
        return wrapper
    return decorator


def debounce(delay_ms: float, root=None):
    """
    Decorator factory for debouncing functions.
    
    Debouncing delays execution until no calls have been made
    for the specified duration. Useful for operations that should
    only happen after user stops an action (like typing).
    
    Usage:
        @debounce(300, root=tk_root)
        def save_draft():
            ...
    
    Note: Requires a tkinter root for scheduling.
    """
    def decorator(func: Callable) -> Callable:
        timer_id = [None]
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cancel pending execution
            if timer_id[0] is not None and root:
                root.after_cancel(timer_id[0])
            
            # Schedule new execution
            def execute():
                timer_id[0] = None
                func(*args, **kwargs)
            
            if root:
                timer_id[0] = root.after(int(delay_ms), execute)
            else:
                # No root provided, execute immediately
                func(*args, **kwargs)
        
        return wrapper
    return decorator

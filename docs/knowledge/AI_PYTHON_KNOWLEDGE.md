# Python Knowledge for AI Agents
**A Comprehensive Guide for AI Assistants Working with Python Code**

---

## 📚 Table of Contents
1. [Understanding AI Agents in Cursor](#understanding-ai-agents-in-cursor)
2. [How to Read Python Code Effectively](#how-to-read-python-code-effectively)
3. [Python Core Concepts & Gotchas](#python-core-concepts--gotchas)
4. [Best Practices for AI-Assisted Development](#best-practices-for-ai-assisted-development)
5. [Common Python Pitfalls](#common-python-pitfalls)
6. [Architectural Patterns](#architectural-patterns)
7. [Refactoring Strategies](#refactoring-strategies)
8. [Tool Usage & File Operations](#tool-usage--file-operations)
9. [Debugging Techniques](#debugging-techniques)
10. [Project-Specific Patterns](#project-specific-patterns)

---

## 🤖 Understanding AI Agents in Cursor

### What is Cursor?
Cursor is an AI-powered code editor that integrates large language models (LLMs) to assist with code understanding, generation, and refactoring. AI agents in Cursor have two primary modes:

1. **Ask Mode (Read-Only)**: Agent can read files, search codebase, and provide suggestions but cannot modify files
2. **Agent Mode (Full Access)**: Agent can read, write, edit files, run commands, and execute changes

### How AI Agents Work
- **Context Window**: Agents have a large context (up to 1M tokens), allowing them to read extensive codebases
- **Tool Access**: Agents use specialized tools (`read_file`, `search_replace`, `grep`, `codebase_search`, `run_terminal_cmd`)
- **Incremental Understanding**: Agents build understanding by reading documentation first (SUMMARY.md, ARCHITECTURE.md, README.md)
- **Pattern Recognition**: Agents learn project patterns from existing code and apply them consistently

### Agent-Human Collaboration
- **Humans provide intent**: "I want X feature" or "Fix Y bug"
- **Agents provide implementation**: Code changes, refactoring, optimization
- **Agents follow project conventions**: Naming, structure, documentation patterns
- **Agents ask when uncertain**: Better to clarify than assume incorrectly

---

## 📖 How to Read Python Code Effectively

### Step 1: Start with Documentation
**Always read these files first** (in order):
1. `README.md` - Project overview, tech stack, quick start
2. `docs/SUMMARY.md` - Current status, features, recent updates
3. `docs/ARCHITECTURE.md` - System design, component relationships
4. `docs/REQUIREMENTS.md` - Functional requirements, specifications
5. `docs/SCRATCHPAD.md` - Development history, version notes
6. `docs/SBOM.md` - Dependencies, security tracking

**Why?** Understanding the project context prevents misguided changes.

### Step 2: Understand Module Structure
```
project/
├── main.py              # Entry point (read first)
├── requirements.txt     # Dependencies (check versions)
├── src/
│   ├── core/           # Business logic, data models
│   ├── ui/             # User interface components
│   ├── tools/          # Specialized tools/utilities
│   ├── utils/          # Helper functions
│   └── animation/      # Feature-specific modules
```

**Pattern Recognition**:
- `core/` = Critical system components
- `ui/` = Presentation layer (CustomTkinter, Tkinter)
- `tools/` = Modular, pluggable functionality
- `utils/` = Stateless helper functions

### Step 3: Read Files Top-to-Bottom
```python
# 1. IMPORTS - Tell you what dependencies exist
import tkinter as tk
from PIL import Image
import numpy as np

# 2. CONSTANTS - Configuration values
MAX_CANVAS_SIZE = 512
DEFAULT_ZOOM = 8

# 3. CLASSES - Main logic containers
class Canvas:
    def __init__(self):
        # 4. Instance variables - Object state
        self.width = 32
        self.pixels = []
    
    def draw_pixel(self, x, y, color):
        # 5. Methods - Object behaviors
        pass

# 6. FUNCTIONS - Standalone utilities
def calculate_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

# 7. MAIN EXECUTION - Entry point
if __name__ == "__main__":
    app = Application()
    app.run()
```

### Step 4: Understand Data Flow
```python
# INPUT → PROCESSING → OUTPUT

# Example: Mouse click handling
def on_mouse_click(event):           # INPUT: Mouse event
    x, y = convert_coords(event.x, event.y)  # PROCESSING: Coordinate conversion
    canvas.set_pixel(x, y, color)    # PROCESSING: Data modification
    canvas.redraw()                   # OUTPUT: Visual update
```

**Key Questions to Ask:**
1. Where does data come from? (User input, file, network)
2. How is data transformed? (Functions, methods)
3. Where does data go? (UI update, file save, network send)

---

## 🐍 Python Core Concepts & Gotchas

### 1. Indentation (CRITICAL!)
```python
# Python uses indentation for code blocks (4 SPACES standard)

# CORRECT
def my_function():
    if condition:
        do_something()
        do_another_thing()
    return result

# WRONG (syntax error)
def my_function():
  if condition:    # 2 spaces
      do_something()  # 4 spaces - INCONSISTENT!
```

**AI Agent Rule**: Always preserve existing indentation style. Use 4 spaces unless project uses tabs.

### 2. Mutable Default Arguments (DANGEROUS!)
```python
# ❌ WRONG - List is created ONCE at function definition
def add_item(item, my_list=[]):
    my_list.append(item)
    return my_list

result1 = add_item(1)  # [1]
result2 = add_item(2)  # [1, 2] - NOT [2]! Same list!

# ✅ CORRECT - New list created each call
def add_item(item, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(item)
    return my_list
```

**Why It Matters**: Mutable defaults (lists, dicts, sets) are shared across all function calls!

### 3. Variable Scope & Binding
```python
# Variables in nested functions can be tricky
x = 10  # Global scope

def outer():
    x = 20  # outer() scope
    
    def inner():
        # x = 30  # inner() scope (if uncommented)
        print(x)  # Prints 20 (from outer scope)
    
    inner()

outer()

# Using nonlocal and global
count = 0  # Global

def increment():
    global count  # Tell Python to modify global variable
    count += 1

def outer():
    x = 0
    def inner():
        nonlocal x  # Tell Python to modify outer's variable
        x += 1
```

**AI Agent Rule**: When modifying variables from outer scopes, check if `global` or `nonlocal` is needed.

### 4. List Comprehensions vs Loops
```python
# Traditional loop
squares = []
for i in range(10):
    squares.append(i ** 2)

# List comprehension (more Pythonic)
squares = [i ** 2 for i in range(10)]

# With condition
even_squares = [i ** 2 for i in range(10) if i % 2 == 0]

# Nested loops
matrix = [[i*j for j in range(5)] for i in range(5)]
```

**AI Agent Rule**: Use comprehensions for simple transformations. Use loops for complex logic.

### 5. String Formatting
```python
name = "Alice"
age = 30

# Old style (avoid)
message = "Hello, %s. You are %d years old." % (name, age)

# .format() (acceptable)
message = "Hello, {}. You are {} years old.".format(name, age)

# f-strings (BEST - Python 3.6+)
message = f"Hello, {name}. You are {age} years old."
message = f"Next year: {age + 1}"  # Can include expressions
```

### 6. Context Managers (with statement)
```python
# ❌ BAD - Must manually close file
file = open("data.txt", "r")
data = file.read()
file.close()  # Easy to forget!

# ✅ GOOD - Automatically closes file
with open("data.txt", "r") as file:
    data = file.read()
# File is automatically closed here

# Multiple context managers
with open("input.txt", "r") as infile, open("output.txt", "w") as outfile:
    data = infile.read()
    outfile.write(data.upper())
```

### 7. Import Patterns
```python
# Standard library
import os
import sys
from pathlib import Path

# Third-party packages
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageDraw

# Local application imports
from .core.canvas import Canvas
from .tools.brush import BrushTool
from .utils.export import export_png
```

**Order**: Standard library → Third-party → Local (separated by blank lines)

### 8. Class Structure
```python
class MyClass:
    # Class variable (shared by all instances)
    class_var = 0
    
    def __init__(self, value):
        # Instance variables (unique to each instance)
        self.value = value
        self.data = []
    
    def instance_method(self):
        # Can access self (instance) and class variables
        return self.value + MyClass.class_var
    
    @classmethod
    def class_method(cls):
        # Can access class variables, not instance variables
        return cls.class_var
    
    @staticmethod
    def static_method(x, y):
        # Can't access class or instance variables
        return x + y
```

### 9. Error Handling
```python
# ❌ BAD - Catches everything (even KeyboardInterrupt!)
try:
    risky_operation()
except:
    print("Something went wrong")

# ✅ GOOD - Specific exceptions
try:
    risky_operation()
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid value: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
    raise  # Re-raise if you can't handle it

# With cleanup
try:
    resource = acquire_resource()
    use_resource(resource)
except Exception as e:
    handle_error(e)
finally:
    release_resource(resource)  # Always runs
```

### 10. None vs Empty Values
```python
# None is a singleton object (only one None exists)
x = None
if x is None:  # Use 'is', not '=='
    print("x is None")

# Empty string
s = ""
if not s:  # Empty strings are "falsy"
    print("String is empty")

# Empty list
items = []
if not items:  # Empty lists are "falsy"
    print("No items")

# Explicit checks
if items == []:  # Also works, but 'not items' is more Pythonic
    print("List is empty")
```

---

## 🎯 Best Practices for AI-Assisted Development

### 1. Read Before Writing
```python
# ❌ BAD AGENT BEHAVIOR:
# - User: "Add a new canvas size option"
# - Agent: *immediately writes code without checking existing patterns*

# ✅ GOOD AGENT BEHAVIOR:
# 1. Read docs/ARCHITECTURE.md to understand canvas system
# 2. Search for existing canvas size handling: grep "canvas.*size"
# 3. Read the file that handles canvas sizes
# 4. Understand the pattern (dropdown, constants, validation)
# 5. Apply the same pattern consistently
```

### 2. Small, Focused Changes
```python
# ❌ BAD - Massive change affecting 20 files at once
# Risk: Breaking things, hard to debug, overwhelming user

# ✅ GOOD - Incremental changes
# 1. Add new feature in one module
# 2. Test that it works
# 3. Integrate with one other component
# 4. Test integration
# 5. Document changes
```

### 3. Preserve Project Patterns
```python
# If project uses this pattern for buttons:
btn = ctk.CTkButton(
    parent,
    text="Save",
    command=self.save_file,
    width=100,
    height=28,
    font=("Arial", 12)
)

# DON'T introduce a new pattern:
# btn = ctk.CTkButton(parent, text="Save", command=lambda: self.save_file())  # Different style!

# DO use the existing pattern consistently:
btn = ctk.CTkButton(
    parent,
    text="Load",
    command=self.load_file,
    width=100,
    height=28,
    font=("Arial", 12)
)
```

### 4. Document Changes
```python
# After making changes, update:
# 1. docs/SCRATCHPAD.md - Development notes
# 2. docs/CHANGELOG.md - User-facing changes
# 3. docs/SUMMARY.md - Current status
# 4. Code comments - Explain WHY, not WHAT

# Example comment:
# ✅ GOOD
def validate_size(width, height):
    # Limit canvas to 512x512 to prevent memory issues on low-end systems
    # Based on testing: 1024x1024 = 4MB per layer, too much for 4GB RAM machines
    if width > 512 or height > 512:
        raise ValueError("Canvas too large")

# ❌ BAD
def validate_size(width, height):
    # Check if width and height are greater than 512
    if width > 512 or height > 512:  # This comment just repeats the code
        raise ValueError("Canvas too large")
```

### 5. Split Large Files
```python
# Rule: If file > 500 lines, consider splitting

# ❌ BAD - 5000 line main_window.py with everything
class MainWindow:
    def __init__(self):
        self.create_ui()
        self.setup_tools()
        self.setup_palette()
        self.setup_layers()
        self.setup_animation()
    
    # ... 5000 lines of methods ...

# ✅ GOOD - Split into modules
# main_window.py (orchestrator, ~300 lines)
class MainWindow:
    def __init__(self):
        self.event_dispatcher = EventDispatcher(self)
        self.ui_builder = UIBuilder(self)
        self.palette_manager = PaletteManager(self)

# event_dispatcher.py (~400 lines)
class EventDispatcher:
    def handle_mouse_click(self, event):
        pass

# ui_builder.py (~350 lines)
class UIBuilder:
    def create_toolbar(self):
        pass
```

### 6. Use Type Hints (When Helpful)
```python
# Type hints improve code clarity and enable better IDE support
from typing import List, Dict, Optional, Tuple

def process_pixels(
    canvas: 'Canvas',
    coordinates: List[Tuple[int, int]],
    color: Tuple[int, int, int, int]
) -> None:
    """
    Process pixels on canvas at given coordinates.
    
    Args:
        canvas: The canvas object to draw on
        coordinates: List of (x, y) pixel positions
        color: RGBA color tuple (0-255 each)
    """
    for x, y in coordinates:
        canvas.set_pixel(x, y, color)

# Optional type (can be None)
def find_layer(name: str) -> Optional['Layer']:
    # Returns Layer or None
    pass
```

### 7. Keep Functions Pure (When Possible)
```python
# ❌ BAD - Function has side effects
total = 0
def add_to_total(value):
    global total
    total += value  # Modifies global state (side effect)
    return total

# ✅ GOOD - Pure function (no side effects)
def calculate_total(current_total, value):
    return current_total + value  # Returns new value, doesn't modify state

# Usage:
total = 0
total = calculate_total(total, 10)
total = calculate_total(total, 20)
```

---

## ⚠️ Common Python Pitfalls

### 1. Late Binding in Closures
```python
# ❌ WRONG - All functions will use i=4 (final value)
functions = []
for i in range(5):
    functions.append(lambda: i * 2)

print([f() for f in functions])  # [8, 8, 8, 8, 8] - NOT [0, 2, 4, 6, 8]

# ✅ CORRECT - Use default argument to capture current value
functions = []
for i in range(5):
    functions.append(lambda x=i: x * 2)

print([f() for f in functions])  # [0, 2, 4, 6, 8]
```

### 2. Modifying List While Iterating
```python
# ❌ WRONG - Skips elements!
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # Modifying list while iterating!

# ✅ CORRECT - Create new list
items = [1, 2, 3, 4, 5]
items = [item for item in items if item % 2 != 0]

# ✅ ALSO CORRECT - Iterate over copy
items = [1, 2, 3, 4, 5]
for item in items[:]:  # [:] creates a copy
    if item % 2 == 0:
        items.remove(item)
```

### 3. Using == for Identity Checks
```python
# ❌ WRONG - == checks VALUE equality
if my_var == None:  # Works, but not idiomatic
    pass

# ✅ CORRECT - 'is' checks IDENTITY (same object)
if my_var is None:
    pass

# Same for True/False
if flag is True:  # Better than flag == True
    pass

# But for most cases, just use truthiness:
if flag:  # Best for booleans
    pass
```

### 4. Dictionary Key Ordering (Pre-Python 3.7)
```python
# Python 3.7+: Dictionaries maintain insertion order
data = {"a": 1, "b": 2, "c": 3}
# Guaranteed to iterate in order: a, b, c

# Python 3.6 and earlier: Order not guaranteed
# If order matters in older versions, use OrderedDict
from collections import OrderedDict
data = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
```

### 5. Floating Point Precision
```python
# ❌ PROBLEM - Binary floating point can't represent 0.1 exactly
result = 0.1 + 0.2
print(result)  # 0.30000000000000004

# ✅ SOLUTION 1 - Use Decimal for exact arithmetic
from decimal import Decimal
result = Decimal("0.1") + Decimal("0.2")
print(result)  # 0.3

# ✅ SOLUTION 2 - Round for display
result = round(0.1 + 0.2, 2)
print(result)  # 0.3

# ✅ SOLUTION 3 - Use epsilon for comparisons
def almost_equal(a, b, epsilon=1e-9):
    return abs(a - b) < epsilon

if almost_equal(0.1 + 0.2, 0.3):
    print("Equal!")
```

### 6. Copy vs Deepcopy
```python
import copy

# Shallow copy - copies top level only
original = [[1, 2], [3, 4]]
shallow = original.copy()  # or original[:]
shallow[0][0] = 999

print(original)  # [[999, 2], [3, 4]] - MODIFIED!
print(shallow)   # [[999, 2], [3, 4]]

# Deep copy - copies everything recursively
original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)
deep[0][0] = 999

print(original)  # [[1, 2], [3, 4]] - NOT modified
print(deep)      # [[999, 2], [3, 4]]
```

### 7. String Concatenation in Loops
```python
# ❌ SLOW - Creates new string object each iteration (O(n²))
result = ""
for item in large_list:
    result += str(item) + ","

# ✅ FAST - Uses list + join (O(n))
parts = []
for item in large_list:
    parts.append(str(item))
result = ",".join(parts)

# ✅ EVEN BETTER - List comprehension + join
result = ",".join(str(item) for item in large_list)
```

---

## 🏗️ Architectural Patterns

### 1. Model-View-Controller (MVC)
```python
# Model - Data and business logic
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None] * width for _ in range(height)]
    
    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color

# View - User interface
class CanvasView:
    def __init__(self, canvas):
        self.canvas = canvas
        self.tk_canvas = tk.Canvas()
    
    def render(self):
        for y in range(self.canvas.height):
            for x in range(self.canvas.width):
                color = self.canvas.pixels[y][x]
                self.draw_pixel(x, y, color)

# Controller - Handles user input
class CanvasController:
    def __init__(self, canvas, view):
        self.canvas = canvas
        self.view = view
    
    def on_mouse_click(self, x, y, color):
        self.canvas.set_pixel(x, y, color)
        self.view.render()
```

### 2. Observer Pattern (Event System)
```python
class EventDispatcher:
    def __init__(self):
        self.listeners = {}
    
    def subscribe(self, event_type, callback):
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)
    
    def emit(self, event_type, data=None):
        if event_type in self.listeners:
            for callback in self.listeners[event_type]:
                callback(data)

# Usage
dispatcher = EventDispatcher()

def on_color_changed(color):
    print(f"Color changed to {color}")

dispatcher.subscribe("color_changed", on_color_changed)
dispatcher.emit("color_changed", (255, 0, 0))
```

### 3. Strategy Pattern (Tool System)
```python
from abc import ABC, abstractmethod

# Abstract base class defines interface
class Tool(ABC):
    @abstractmethod
    def on_mouse_down(self, x, y):
        pass
    
    @abstractmethod
    def on_mouse_up(self, x, y):
        pass

# Concrete implementations
class BrushTool(Tool):
    def on_mouse_down(self, x, y):
        print(f"Drawing at {x}, {y}")
    
    def on_mouse_up(self, x, y):
        print("Brush released")

class EraserTool(Tool):
    def on_mouse_down(self, x, y):
        print(f"Erasing at {x}, {y}")
    
    def on_mouse_up(self, x, y):
        print("Eraser released")

# Context uses strategy
class DrawingContext:
    def __init__(self):
        self.current_tool = BrushTool()
    
    def set_tool(self, tool):
        self.current_tool = tool
    
    def handle_click(self, x, y):
        self.current_tool.on_mouse_down(x, y)
```

### 4. Singleton Pattern
```python
class ThemeManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.theme = "dark"
        return cls._instance

# Usage - always returns same instance
theme1 = ThemeManager()
theme2 = ThemeManager()
print(theme1 is theme2)  # True
```

### 5. Factory Pattern
```python
class ToolFactory:
    @staticmethod
    def create_tool(tool_type):
        if tool_type == "brush":
            return BrushTool()
        elif tool_type == "eraser":
            return EraserTool()
        elif tool_type == "fill":
            return FillTool()
        else:
            raise ValueError(f"Unknown tool: {tool_type}")

# Usage
tool = ToolFactory.create_tool("brush")
```

---

## 🔄 Refactoring Strategies

### 1. Extract Method
```python
# ❌ BEFORE - Long method with multiple responsibilities
def process_order(order):
    # Validate order
    if not order.items:
        raise ValueError("No items")
    if order.total < 0:
        raise ValueError("Invalid total")
    
    # Calculate tax
    tax_rate = 0.08
    tax = order.total * tax_rate
    
    # Apply discount
    if order.total > 100:
        discount = order.total * 0.1
    else:
        discount = 0
    
    # Final calculation
    final_total = order.total + tax - discount
    return final_total

# ✅ AFTER - Extracted methods with single responsibilities
def process_order(order):
    validate_order(order)
    tax = calculate_tax(order.total)
    discount = calculate_discount(order.total)
    return order.total + tax - discount

def validate_order(order):
    if not order.items:
        raise ValueError("No items")
    if order.total < 0:
        raise ValueError("Invalid total")

def calculate_tax(total):
    tax_rate = 0.08
    return total * tax_rate

def calculate_discount(total):
    if total > 100:
        return total * 0.1
    return 0
```

### 2. Extract Class
```python
# ❌ BEFORE - God class with too many responsibilities
class MainWindow:
    def __init__(self):
        self.canvas_width = 32
        self.canvas_height = 32
        self.pixels = []
        self.current_color = (255, 0, 0)
        self.palette = []
        self.layers = []
        self.animation_frames = []
        # ... 50 more attributes ...
    
    def draw_pixel(self, x, y):
        pass
    
    def change_color(self, color):
        pass
    
    def add_layer(self):
        pass
    
    # ... 100 more methods ...

# ✅ AFTER - Extracted specialized classes
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = []
    
    def draw_pixel(self, x, y, color):
        pass

class PaletteManager:
    def __init__(self):
        self.palette = []
        self.current_color = (255, 0, 0)
    
    def change_color(self, color):
        pass

class LayerManager:
    def __init__(self):
        self.layers = []
    
    def add_layer(self):
        pass

class MainWindow:
    def __init__(self):
        self.canvas = Canvas(32, 32)
        self.palette_manager = PaletteManager()
        self.layer_manager = LayerManager()
```

### 3. Replace Magic Numbers with Constants
```python
# ❌ BEFORE - Magic numbers everywhere
def resize_canvas(self, width, height):
    if width > 512 or height > 512:
        raise ValueError("Too large")
    if width < 1 or height < 1:
        raise ValueError("Too small")

def calculate_zoom(self, canvas_size):
    if canvas_size <= 16:
        return 16
    elif canvas_size <= 32:
        return 8
    else:
        return 4

# ✅ AFTER - Named constants
MAX_CANVAS_SIZE = 512
MIN_CANVAS_SIZE = 1
ZOOM_LARGE = 16
ZOOM_MEDIUM = 8
ZOOM_SMALL = 4
SMALL_CANVAS_THRESHOLD = 16
MEDIUM_CANVAS_THRESHOLD = 32

def resize_canvas(self, width, height):
    if width > MAX_CANVAS_SIZE or height > MAX_CANVAS_SIZE:
        raise ValueError(f"Canvas cannot exceed {MAX_CANVAS_SIZE}x{MAX_CANVAS_SIZE}")
    if width < MIN_CANVAS_SIZE or height < MIN_CANVAS_SIZE:
        raise ValueError(f"Canvas must be at least {MIN_CANVAS_SIZE}x{MIN_CANVAS_SIZE}")

def calculate_zoom(self, canvas_size):
    if canvas_size <= SMALL_CANVAS_THRESHOLD:
        return ZOOM_LARGE
    elif canvas_size <= MEDIUM_CANVAS_THRESHOLD:
        return ZOOM_MEDIUM
    else:
        return ZOOM_SMALL
```

### 4. Simplify Conditional Logic
```python
# ❌ BEFORE - Complex nested conditionals
def get_status(user):
    if user.is_active:
        if user.subscription:
            if user.subscription.is_valid():
                if user.subscription.plan == "premium":
                    return "Premium Active"
                else:
                    return "Standard Active"
            else:
                return "Expired"
        else:
            return "No Subscription"
    else:
        return "Inactive"

# ✅ AFTER - Guard clauses (early returns)
def get_status(user):
    if not user.is_active:
        return "Inactive"
    
    if not user.subscription:
        return "No Subscription"
    
    if not user.subscription.is_valid():
        return "Expired"
    
    if user.subscription.plan == "premium":
        return "Premium Active"
    
    return "Standard Active"
```

---

## 🛠️ Tool Usage & File Operations

### Reading Files Efficiently
```python
# For AI agents using read_file tool:

# ✅ GOOD - Read specific sections
read_file("large_file.py", offset=100, limit=50)  # Lines 100-150

# ❌ BAD - Reading entire 5000-line file when you only need a method
read_file("main_window.py")  # Wastes tokens

# Better approach:
# 1. Use grep to find method location: grep -n "def my_method" main_window.py
# 2. Read only that section: read_file("main_window.py", offset=200, limit=30)
```

### Using grep Effectively
```python
# Find all class definitions
grep("^class ", path="src/")

# Find method with context
grep("def calculate_total", "-B": 2, "-A": 10)  # 2 lines before, 10 after

# Case-insensitive search
grep("TODO", "-i": True)

# Count occurrences
grep("import numpy", output_mode="count")

# Find files containing pattern
grep("class Canvas", output_mode="files_with_matches")
```

### Using search_replace
```python
# ❌ WRONG - Not unique (will fail if pattern appears multiple times)
search_replace(
    "main.py",
    old_string="def process():",
    new_string="def process_data():"
)

# ✅ CORRECT - Include context for uniqueness
search_replace(
    "main.py",
    old_string="""class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process():
        return self.data""",
    new_string="""class DataProcessor:
    def __init__(self):
        self.data = []
    
    def process_data():
        return self.data"""
)

# For renaming variables across file
search_replace(
    "main.py",
    old_string="old_var_name",
    new_string="new_var_name",
    replace_all=True
)
```

### Using codebase_search
```python
# ✅ GOOD - Specific question
codebase_search(
    query="How does the undo/redo system save state?",
    target_directories=["src/core/"],
    explanation="Find undo manager implementation details"
)

# ❌ BAD - Too vague
codebase_search(
    query="undo",
    target_directories=[],
    explanation="Looking for undo"
)

# ✅ GOOD - Focused search
codebase_search(
    query="Where are color palettes loaded from JSON files?",
    target_directories=["src/core/"],
    explanation="Find palette loading logic"
)
```

---

## 🐛 Debugging Techniques

### 1. Print Debugging
```python
# ❌ BAD - No context
print(x)

# ✅ GOOD - Descriptive prints
print(f"[DEBUG] Mouse click at x={x}, y={y}")
print(f"[DEBUG] Color selected: {color} (type: {type(color)})")
print(f"[DEBUG] Canvas size: {canvas.width}x{canvas.height}")

# Temporary debug prints (remove after debugging)
def calculate_total(items):
    print(f"[DEBUG] calculate_total called with {len(items)} items")
    total = sum(item.price for item in items)
    print(f"[DEBUG] Calculated total: ${total:.2f}")
    return total
```

### 2. Assertions for Sanity Checks
```python
def set_pixel(self, x, y, color):
    # Assertions for debugging (removed in production with -O flag)
    assert 0 <= x < self.width, f"x={x} out of bounds (width={self.width})"
    assert 0 <= y < self.height, f"y={y} out of bounds (height={self.height})"
    assert len(color) == 4, f"Color must be RGBA tuple, got {color}"
    assert all(0 <= c <= 255 for c in color), f"Color values must be 0-255, got {color}"
    
    self.pixels[y][x] = color
```

### 3. Logging for Production
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='app.log'
)

logger = logging.getLogger(__name__)

def load_project(filename):
    logger.info(f"Loading project: {filename}")
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        logger.debug(f"Loaded {len(data)} keys from project file")
        return data
    except FileNotFoundError:
        logger.error(f"Project file not found: {filename}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {filename}: {e}")
        raise
```

### 4. Inspect Variable State
```python
# Check type and contents
import pprint

def debug_variable(var, name="variable"):
    print(f"[DEBUG] {name}:")
    print(f"  Type: {type(var)}")
    print(f"  Value: {pprint.pformat(var)}")
    if hasattr(var, '__dict__'):
        print(f"  Attributes: {pprint.pformat(var.__dict__)}")

# Usage
debug_variable(canvas, "canvas")
debug_variable(color_palette, "color_palette")
```

---

## 📋 Project-Specific Patterns

### Pixel Perfect Application Patterns

#### 1. Theme System Pattern
```python
# Theme application follows consistent pattern:
def _apply_theme(self, theme):
    # 1. Update main containers
    self.left_panel.configure(fg_color=theme.bg_secondary)
    self.right_panel.configure(fg_color=theme.bg_secondary)
    
    # 2. Update buttons
    for btn in self.tool_buttons:
        btn.configure(
            fg_color=theme.button_bg,
            hover_color=theme.button_hover
        )
    
    # 3. Update specific UI elements
    self.color_wheel.update_theme(theme)
    
    # 4. Trigger redraws
    self.canvas.redraw()
```

#### 2. Event Handler Pattern
```python
# Mouse events follow this pattern:
def _on_canvas_mouse_down(self, event):
    # 1. Convert screen coords to canvas coords
    x, y = self._screen_to_canvas(event.x, event.y)
    
    # 2. Check bounds
    if not self._is_valid_position(x, y):
        return
    
    # 3. Get current state (color, tool, layer)
    color = self.palette_manager.get_current_color()
    tool = self.tool_manager.current_tool
    layer = self.layer_manager.active_layer
    
    # 4. Delegate to tool
    tool.on_mouse_down(layer, x, y, color)
    
    # 5. Save undo state
    self.undo_manager.save_state()
    
    # 6. Redraw
    self.canvas.redraw()
```

#### 3. Module Structure Pattern
```python
# New features follow this structure:

# src/core/<feature>.py - Business logic
class FeatureManager:
    def __init__(self):
        self.data = []
    
    def process(self):
        pass

# src/ui/<feature>_panel.py - UI components
class FeaturePanel(ctk.CTkFrame):
    def __init__(self, parent, feature_manager):
        super().__init__(parent)
        self.feature_manager = feature_manager
        self.create_ui()
    
    def create_ui(self):
        pass

# src/ui/main_window.py - Integration
class MainWindow:
    def __init__(self):
        self.feature_manager = FeatureManager()
        self.feature_panel = FeaturePanel(self.right_panel, self.feature_manager)
```

#### 4. Documentation Pattern
```python
# After any changes, update these files in order:

# 1. docs/SCRATCHPAD.md
"""
## Version X.XX - Feature Name
**Date**: October 15, 2025
**Status**: Complete ✅

### Feature: Description
<Problem, Solution, Implementation, Results, Benefits>
"""

# 2. docs/CHANGELOG.md
"""
### Version X.XX (Date)
🎯 **Feature Name**
- Feature description
- Technical details
- User benefits
"""

# 3. docs/SUMMARY.md
"""
## Latest Updates (vX.XX)
- Update feature list
- Update version number
- Update last modified date
"""

# 4. README.md (if user-facing feature)
"""
Update feature list with new capability
"""
```

---

## 🎓 Advanced Tips for AI Agents

### 1. When Uncertain, Ask
```python
# ❌ BAD - Guessing and potentially breaking things
# "I'll just assume this variable should be initialized here..."

# ✅ GOOD - Clarify before proceeding
# "I see two possible approaches:
#  1. Initialize in __init__ (cleaner, but changes initialization order)
#  2. Initialize on first use (safer, but adds None checks)
#  Which would you prefer?"
```

### 2. Provide Context in Explanations
```python
# ❌ BAD - Vague response
# "I fixed the bug."

# ✅ GOOD - Detailed explanation
# "Fixed the color wheel click detection bug:
#  - Problem: Wheel responded to clicks outside the ring
#  - Root cause: Distance calculation didn't account for ring thickness
#  - Solution: Added bounds check: radius - thickness <= distance <= radius
#  - Files changed: src/ui/color_wheel.py (line 156)
#  - Tested: Clicks on center and outside now properly ignored"
```

### 3. Test Your Changes Mentally
```python
# Before suggesting code, trace through execution:

# ❌ BAD - Suggesting untested code
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
# ^ What if numbers is empty? Division by zero!

# ✅ GOOD - Defensive coding
def calculate_average(numbers):
    if not numbers:
        return 0  # Or raise ValueError, depending on requirements
    return sum(numbers) / len(numbers)
```

### 4. Respect Existing Patterns
```python
# If project uses:
# - 4 spaces (not tabs)
# - Double quotes for strings (not single)
# - Specific import order
# - Particular naming conventions
# → Follow those patterns exactly!

# Don't introduce inconsistency just because you "prefer" a different style
```

### 5. Read Error Messages Carefully
```python
# Error message:
# TypeError: 'NoneType' object is not subscriptable

# Analyze:
# 1. "NoneType" - something is None when it shouldn't be
# 2. "not subscriptable" - trying to use [] on it
# 3. Most likely: result = some_function()[0] where some_function returned None

# Find the None:
# - Check function returns
# - Check variable assignments
# - Add print statements to trace
```

---

## 📖 Essential Python References

### Standard Library Must-Knows
- `os` / `pathlib` - File system operations
- `json` - JSON parsing and serialization
- `datetime` - Date and time handling
- `collections` - Specialized containers (defaultdict, Counter, deque)
- `itertools` - Iterator functions
- `functools` - Higher-order functions (lru_cache, partial)
- `typing` - Type hints
- `abc` - Abstract base classes
- `enum` - Enumerations

### Common Third-Party Libraries
- `numpy` - Numerical arrays and operations
- `Pillow (PIL)` - Image processing
- `customtkinter` - Modern Tkinter UI
- `requests` - HTTP requests
- `pytest` - Testing framework

---

## 🚀 Quick Reference Cheatsheet

### Python Syntax Quick Hits
```python
# List comprehension
[x*2 for x in range(10) if x % 2 == 0]

# Dictionary comprehension
{x: x**2 for x in range(5)}

# Set comprehension
{x % 3 for x in range(10)}

# Generator expression
(x*2 for x in range(10))

# Unpacking
a, b = [1, 2]
a, *rest, b = [1, 2, 3, 4, 5]  # a=1, rest=[2,3,4], b=5

# Dictionary unpacking
merged = {**dict1, **dict2}

# Function arguments
def func(pos_only, /, pos_or_kw, *, kw_only):
    pass

# f-strings
name = "Alice"
f"Hello, {name}!"
f"{value:.2f}"  # Format to 2 decimals
f"{value:>10}"  # Right-align in 10 chars

# Ternary operator
result = "yes" if condition else "no"

# Walrus operator (Python 3.8+)
if (n := len(items)) > 10:
    print(f"Too many items: {n}")

# Match statement (Python 3.10+)
match value:
    case 1:
        print("one")
    case 2:
        print("two")
    case _:
        print("other")
```

---

## 🎯 Summary: Core Principles for AI Agents

1. **Read documentation first** - Understand before changing
2. **Preserve patterns** - Consistency over personal preference
3. **Make small changes** - Incremental is safer
4. **Test mentally** - Trace execution before suggesting
5. **Document everything** - Help future agents (and humans)
6. **Ask when uncertain** - Better to clarify than assume
7. **Respect the user's style** - Follow their conventions
8. **Provide context** - Explain why, not just what
9. **Handle errors gracefully** - Defensive programming
10. **Keep learning** - Each project teaches new patterns

---

**Remember**: You're not just writing code—you're collaborating with humans and future AI agents. Write code that's clear, maintainable, and true to the project's vision.

---

*This document is a living resource. Update it as you discover new patterns, pitfalls, and best practices.*

**Version**: 1.0  
**Created**: October 15, 2025  
**For**: AI Agents working with Python in Cursor IDE


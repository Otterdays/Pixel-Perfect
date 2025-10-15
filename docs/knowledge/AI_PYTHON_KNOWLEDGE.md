# Python Knowledge for AI Agents
**A Comprehensive Guide for AI Assistants Working with Python Code**

---

## 📚 Table of Contents
1. [Understanding AI Agents in Cursor](#understanding-ai-agents-in-cursor)
2. [How to Read Python Code Effectively](#how-to-read-python-code-effectively)
3. [Python Core Concepts & Modern Features](#python-core-concepts--modern-features)
4. [Best Practices for AI-Assisted Development](#best-practices-for-ai-assisted-development)
5. [Common Python Pitfalls](#common-python-pitfalls)
6. [Architectural Patterns & Design Principles](#architectural-patterns--design-principles)
7. [Refactoring Strategies](#refactoring-strategies)
8. [Testing Frameworks & Methodologies](#testing-frameworks--methodologies)
9. [Performance Optimization](#performance-optimization)
10. [Dependency Management](#dependency-management)
11. [Maintainability Standards](#maintainability-standards)
12. [Tool Usage & File Operations](#tool-usage--file-operations)
13. [Debugging Techniques](#debugging-techniques)
14. [Project-Specific Patterns](#project-specific-patterns)
15. [Modern Python Features](#modern-python-features)

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

## 🐍 Python Core Concepts & Modern Features

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

### 11. Type Hints & Modern Python Features
```python
from typing import List, Dict, Optional, Union, Tuple, Callable, Any
from dataclasses import dataclass
from enum import Enum
import asyncio
from pathlib import Path

# Type hints improve code clarity and enable better IDE support
def process_pixels(
    canvas: 'Canvas',
    coordinates: List[Tuple[int, int]],
    color: Tuple[int, int, int, int]
) -> None:
    """Process pixels on canvas at given coordinates."""
    for x, y in coordinates:
        canvas.set_pixel(x, y, color)

# Optional type (can be None)
def find_layer(name: str) -> Optional['Layer']:
    """Find layer by name, returns Layer or None."""
    pass

# Union types
def parse_value(value: Union[str, int, float]) -> Any:
    """Parse different value types."""
    pass

# Dataclasses for structured data (Python 3.7+)
@dataclass
class Color:
    r: int
    g: int
    b: int
    a: int = 255  # Default value
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)

# Enums for constants
class ToolType(Enum):
    BRUSH = "brush"
    ERASER = "eraser"
    FILL = "fill"
    EYEDROPPER = "eyedropper"

# Async/await for concurrent operations
async def load_project_async(filename: Path) -> Dict[str, Any]:
    """Load project file asynchronously."""
    import aiofiles
    async with aiofiles.open(filename, 'r') as f:
        content = await f.read()
        return json.loads(content)

# Context managers for resource management
class DatabaseConnection:
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False  # Don't suppress exceptions

# Usage
with DatabaseConnection() as db:
    db.execute_query("SELECT * FROM users")
```

### 12. Modern Python Collections
```python
from collections import defaultdict, Counter, deque, namedtuple
from typing import DefaultDict

# defaultdict - automatically creates missing keys
word_count: DefaultDict[str, int] = defaultdict(int)
word_count["hello"] += 1  # No KeyError if "hello" doesn't exist

# Counter - count occurrences
text = "hello world hello"
counter = Counter(text.split())  # {'hello': 2, 'world': 1}

# deque - efficient double-ended queue
queue = deque([1, 2, 3])
queue.appendleft(0)  # Add to front: [0, 1, 2, 3]
queue.append(4)      # Add to back: [0, 1, 2, 3, 4]
front = queue.popleft()  # Remove from front: 0

# namedtuple - lightweight class alternative
Point = namedtuple('Point', ['x', 'y'])
p = Point(1, 2)
print(p.x, p.y)  # 1 2
```

### 13. Advanced Function Features
```python
from functools import wraps, lru_cache, partial
import time

# Decorators
def timing_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@timing_decorator
def expensive_calculation(n: int) -> int:
    """Calculate something expensive."""
    return sum(i * i for i in range(n))

# LRU Cache for memoization
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    """Calculate Fibonacci number with caching."""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Partial functions
def multiply(x: int, y: int) -> int:
    return x * y

double = partial(multiply, 2)  # Always multiply by 2
triple = partial(multiply, 3)   # Always multiply by 3

print(double(5))  # 10
print(triple(5))   # 15

# Lambda functions (use sparingly)
squares = list(map(lambda x: x ** 2, range(10)))
# Better: [x ** 2 for x in range(10)]
```

### 14. Path and File Operations
```python
from pathlib import Path
import shutil
import tempfile

# Modern path handling (Python 3.4+)
project_root = Path(__file__).parent.parent
config_file = project_root / "config" / "settings.json"
assets_dir = project_root / "assets"

# Path operations
if config_file.exists():
    content = config_file.read_text(encoding='utf-8')
    config_file.write_text("new content", encoding='utf-8')

# Directory operations
assets_dir.mkdir(parents=True, exist_ok=True)
for file_path in assets_dir.glob("*.png"):
    print(f"Found image: {file_path.name}")

# Temporary files
with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
    f.write('{"temp": "data"}')
    temp_path = Path(f.name)

# Clean up
temp_path.unlink()

# File copying
shutil.copy2(source_file, destination_file)  # Preserves metadata
shutil.copytree(source_dir, dest_dir)  # Copy directory tree
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

## 🧪 Testing Frameworks & Methodologies

### 1. Testing Philosophy & TDD
```python
# Test-Driven Development (TDD) Cycle:
# 1. RED: Write failing test
# 2. GREEN: Write minimal code to pass
# 3. REFACTOR: Improve code while keeping tests green

# Example TDD approach for a new feature
def test_canvas_resize():
    """Test canvas resizing functionality."""
    canvas = Canvas(32, 32)
    canvas.resize(64, 64)
    assert canvas.width == 64
    assert canvas.height == 64
    assert len(canvas.pixels) == 64
    assert len(canvas.pixels[0]) == 64

# Write the test first, then implement the feature
```

### 2. Pytest Framework
```python
# pytest is the modern standard for Python testing
# Install: pip install pytest pytest-cov pytest-mock

# Basic test structure
import pytest
from unittest.mock import Mock, patch
from src.core.canvas import Canvas

class TestCanvas:
    """Test suite for Canvas class."""
    
    def setup_method(self):
        """Setup before each test method."""
        self.canvas = Canvas(32, 32)
    
    def test_canvas_creation(self):
        """Test canvas initialization."""
        assert self.canvas.width == 32
        assert self.canvas.height == 32
        assert len(self.canvas.pixels) == 32
    
    def test_set_pixel_valid_coordinates(self):
        """Test setting pixel with valid coordinates."""
        color = (255, 0, 0, 255)
        self.canvas.set_pixel(10, 15, color)
        assert self.canvas.pixels[15][10] == color
    
    def test_set_pixel_invalid_coordinates(self):
        """Test setting pixel with invalid coordinates."""
        color = (255, 0, 0, 255)
        with pytest.raises(ValueError, match="Coordinates out of bounds"):
            self.canvas.set_pixel(100, 100, color)
    
    @pytest.mark.parametrize("x,y,expected", [
        (0, 0, True),
        (31, 31, True),
        (32, 32, False),
        (-1, -1, False),
    ])
    def test_is_valid_position(self, x, y, expected):
        """Test position validation with multiple inputs."""
        assert self.canvas.is_valid_position(x, y) == expected

# Fixtures for shared test data
@pytest.fixture
def sample_canvas():
    """Create a sample canvas for testing."""
    canvas = Canvas(16, 16)
    # Pre-populate with some pixels
    for x in range(16):
        for y in range(16):
            canvas.set_pixel(x, y, (x * 16, y * 16, 0, 255))
    return canvas

def test_canvas_operations(sample_canvas):
    """Test operations on pre-populated canvas."""
    assert sample_canvas.get_pixel(0, 0) == (0, 0, 0, 255)
    assert sample_canvas.get_pixel(15, 15) == (240, 240, 0, 255)
```

### 3. Mocking & Test Doubles
```python
from unittest.mock import Mock, patch, MagicMock
import pytest

class TestEventDispatcher:
    """Test event dispatcher with mocks."""
    
    def test_subscribe_and_emit(self):
        """Test event subscription and emission."""
        dispatcher = EventDispatcher()
        mock_callback = Mock()
        
        dispatcher.subscribe("test_event", mock_callback)
        dispatcher.emit("test_event", {"data": "test"})
        
        mock_callback.assert_called_once_with({"data": "test"})
    
    @patch('src.core.canvas.Canvas')
    def test_canvas_integration(self, mock_canvas_class):
        """Test integration with mocked canvas."""
        mock_canvas = Mock()
        mock_canvas_class.return_value = mock_canvas
        
        # Test code that uses canvas
        result = create_canvas_with_size(64, 64)
        
        mock_canvas_class.assert_called_once_with(64, 64)
        assert result == mock_canvas
    
    def test_file_operations_with_patch(self):
        """Test file operations with patched file system."""
        with patch('builtins.open', mock_open(read_data='{"test": "data"}')):
            with patch('pathlib.Path.exists', return_value=True):
                data = load_config_file("test.json")
                assert data == {"test": "data"}

# Mock external dependencies
@pytest.fixture
def mock_file_system():
    """Mock file system operations."""
    with patch('pathlib.Path.exists') as mock_exists, \
         patch('pathlib.Path.read_text') as mock_read, \
         patch('pathlib.Path.write_text') as mock_write:
        
        mock_exists.return_value = True
        mock_read.return_value = '{"mock": "data"}'
        
        yield {
            'exists': mock_exists,
            'read_text': mock_read,
            'write_text': mock_write
        }
```

### 4. Integration Testing
```python
import tempfile
import json
from pathlib import Path

class TestProjectIntegration:
    """Integration tests for project save/load functionality."""
    
    def test_save_and_load_project(self):
        """Test complete project save/load cycle."""
        # Create test project
        project = Project()
        project.canvas = Canvas(32, 32)
        project.canvas.set_pixel(10, 10, (255, 0, 0, 255))
        project.layers = [Layer("background"), Layer("foreground")]
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.pixpf', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            # Save project
            project.save(temp_path)
            
            # Load project
            loaded_project = Project.load(temp_path)
            
            # Verify data integrity
            assert loaded_project.canvas.width == 32
            assert loaded_project.canvas.height == 32
            assert loaded_project.canvas.get_pixel(10, 10) == (255, 0, 0, 255)
            assert len(loaded_project.layers) == 2
            assert loaded_project.layers[0].name == "background"
            
        finally:
            # Cleanup
            temp_path.unlink()
    
    def test_ui_integration(self):
        """Test UI components working together."""
        # This would test actual UI components
        # Note: For GUI testing, consider using pytest-qt or similar
        pass
```

### 5. Performance Testing
```python
import time
import pytest
from memory_profiler import profile

class TestPerformance:
    """Performance tests for critical operations."""
    
    def test_canvas_rendering_performance(self):
        """Test canvas rendering performance."""
        canvas = Canvas(512, 512)
        
        # Fill canvas with test data
        for x in range(512):
            for y in range(512):
                canvas.set_pixel(x, y, (x % 256, y % 256, 0, 255))
        
        # Measure rendering time
        start_time = time.time()
        canvas.render()
        end_time = time.time()
        
        # Should render in less than 100ms
        assert (end_time - start_time) < 0.1
    
    @pytest.mark.slow
    def test_large_canvas_operations(self):
        """Test operations on large canvas (marked as slow test)."""
        canvas = Canvas(1024, 1024)
        
        # Test fill operation performance
        start_time = time.time()
        canvas.fill((255, 255, 255, 255))
        end_time = time.time()
        
        # Should complete in reasonable time
        assert (end_time - start_time) < 1.0
    
    def test_memory_usage(self):
        """Test memory usage of canvas operations."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Create large canvas
        canvas = Canvas(1024, 1024)
        canvas.fill((255, 0, 0, 255))
        
        current_memory = process.memory_info().rss
        memory_increase = current_memory - initial_memory
        
        # Should not use more than 50MB for 1024x1024 canvas
        assert memory_increase < 50 * 1024 * 1024
```

### 6. Test Configuration & Running
```python
# pytest.ini configuration
"""
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
"""

# conftest.py for shared fixtures
import pytest
from src.core.canvas import Canvas

@pytest.fixture(scope="session")
def test_canvas():
    """Session-scoped canvas fixture."""
    return Canvas(32, 32)

@pytest.fixture
def empty_canvas():
    """Function-scoped empty canvas fixture."""
    return Canvas(16, 16)

# Running tests
"""
# Run all tests
pytest

# Run specific test file
pytest tests/test_canvas.py

# Run tests with coverage
pytest --cov=src --cov-report=html

# Run only fast tests
pytest -m "not slow"

# Run tests in parallel
pytest -n auto

# Run tests with verbose output
pytest -v

# Run tests and stop on first failure
pytest -x
"""
```

### 7. Continuous Integration Testing
```python
# .github/workflows/test.yml (GitHub Actions)
"""
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
"""

# Pre-commit hooks for testing
# .pre-commit-config.yaml
"""
repos:
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
        args: [--maxfail=1, -q]
"""
```

---

## ⚡ Performance Optimization

### 1. Profiling & Measurement
```python
import time
import cProfile
import pstats
from memory_profiler import profile
import psutil
import os

# Time profiling
def time_function(func):
    """Decorator to measure function execution time."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

# Memory profiling
@profile
def memory_intensive_function():
    """Function that uses a lot of memory."""
    large_list = [i for i in range(1000000)]
    return sum(large_list)

# CPU profiling
def profile_canvas_rendering():
    """Profile canvas rendering performance."""
    pr = cProfile.Profile()
    pr.enable()
    
    # Code to profile
    canvas = Canvas(512, 512)
    canvas.render()
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('cumulative').print_stats(10)

# Memory usage monitoring
def monitor_memory_usage():
    """Monitor memory usage during operations."""
    process = psutil.Process(os.getpid())
    
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    # Perform operations
    canvas = Canvas(1024, 1024)
    canvas.fill((255, 0, 0, 255))
    
    current_memory = process.memory_info().rss / 1024 / 1024  # MB
    memory_increase = current_memory - initial_memory
    
    print(f"Memory increase: {memory_increase:.2f} MB")
    return memory_increase
```

### 2. Algorithmic Optimization
```python
import numpy as np
from functools import lru_cache
import bisect

# Use NumPy for numerical operations
def slow_pixel_processing(pixels):
    """Slow pixel processing using Python lists."""
    result = []
    for row in pixels:
        new_row = []
        for pixel in row:
            new_row.append(pixel * 2)
        result.append(new_row)
    return result

def fast_pixel_processing(pixels):
    """Fast pixel processing using NumPy."""
    pixels_array = np.array(pixels)
    return (pixels_array * 2).tolist()

# Caching for expensive computations
@lru_cache(maxsize=128)
def expensive_calculation(n):
    """Expensive calculation with caching."""
    if n < 2:
        return n
    return expensive_calculation(n - 1) + expensive_calculation(n - 2)

# Binary search for sorted data
def find_color_index(colors, target_color):
    """Find color index using binary search."""
    # Sort colors first (one-time cost)
    sorted_colors = sorted(colors)
    
    # Binary search (O(log n) vs O(n) linear search)
    index = bisect.bisect_left(sorted_colors, target_color)
    return index if index < len(sorted_colors) and sorted_colors[index] == target_color else -1

# Efficient data structures
from collections import deque
import heapq

def efficient_queue_operations():
    """Demonstrate efficient queue operations."""
    # Use deque for O(1) operations on both ends
    queue = deque()
    queue.appendleft("front")  # O(1)
    queue.append("back")       # O(1)
    front = queue.popleft()    # O(1)
    back = queue.pop()         # O(1)

def efficient_priority_queue():
    """Demonstrate efficient priority queue."""
    # Use heapq for priority queue operations
    heap = []
    heapq.heappush(heap, (1, "high priority"))
    heapq.heappush(heap, (3, "low priority"))
    heapq.heappush(heap, (2, "medium priority"))
    
    # Always get highest priority item
    priority, item = heapq.heappop(heap)
    return item
```

### 3. Memory Optimization
```python
import gc
import weakref
from typing import List, Optional

# Weak references to avoid circular references
class Canvas:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = [[None] * width for _ in range(height)]
        self._observers = weakref.WeakSet()  # Avoid memory leaks
    
    def add_observer(self, observer):
        """Add observer using weak reference."""
        self._observers.add(observer)
    
    def notify_observers(self):
        """Notify all observers."""
        for observer in self._observers:
            observer.update()

# Memory-efficient data structures
class MemoryEfficientCanvas:
    """Canvas that uses less memory for sparse data."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = {}  # Dict instead of 2D list for sparse data
    
    def set_pixel(self, x: int, y: int, color: tuple):
        """Set pixel efficiently."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[(x, y)] = color
    
    def get_pixel(self, x: int, y: int) -> Optional[tuple]:
        """Get pixel efficiently."""
        return self.pixels.get((x, y), (0, 0, 0, 0))  # Default transparent
    
    def clear(self):
        """Clear all pixels."""
        self.pixels.clear()

# Garbage collection optimization
def optimize_memory_usage():
    """Optimize memory usage by managing garbage collection."""
    # Force garbage collection
    gc.collect()
    
    # Get memory stats
    memory_stats = gc.get_stats()
    print(f"Garbage collection stats: {memory_stats}")
    
    # Set garbage collection thresholds
    gc.set_threshold(700, 10, 10)  # More aggressive GC

# Object pooling for frequently created objects
class ColorPool:
    """Pool for reusing color objects."""
    
    def __init__(self):
        self._pool = {}
    
    def get_color(self, r: int, g: int, b: int, a: int = 255) -> tuple:
        """Get color from pool or create new one."""
        key = (r, g, b, a)
        if key not in self._pool:
            self._pool[key] = (r, g, b, a)
        return self._pool[key]
    
    def clear_pool(self):
        """Clear the color pool."""
        self._pool.clear()

# Use __slots__ for memory efficiency
class EfficientPoint:
    """Point class with __slots__ for memory efficiency."""
    __slots__ = ['x', 'y', 'color']
    
    def __init__(self, x: int, y: int, color: tuple):
        self.x = x
        self.y = y
        self.color = color
```

### 4. I/O Optimization
```python
import asyncio
import aiofiles
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path

# Asynchronous file operations
async def load_project_async(file_path: Path) -> dict:
    """Load project file asynchronously."""
    async with aiofiles.open(file_path, 'r') as f:
        content = await f.read()
        return json.loads(content)

async def save_project_async(file_path: Path, data: dict) -> None:
    """Save project file asynchronously."""
    content = json.dumps(data, indent=2)
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(content)

# Concurrent file operations
async def load_multiple_projects(file_paths: List[Path]) -> List[dict]:
    """Load multiple project files concurrently."""
    tasks = [load_project_async(path) for path in file_paths]
    return await asyncio.gather(*tasks)

# Thread pool for CPU-intensive operations
def cpu_intensive_operation(data):
    """CPU-intensive operation."""
    return sum(i * i for i in range(len(data)))

async def process_large_dataset(data_list: List[List[int]]) -> List[int]:
    """Process large dataset using thread pool."""
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as executor:
        tasks = [
            loop.run_in_executor(executor, cpu_intensive_operation, data)
            for data in data_list
        ]
        return await asyncio.gather(*tasks)

# Efficient JSON serialization
def efficient_json_serialization(data: dict) -> str:
    """Efficient JSON serialization."""
    # Use separators to reduce file size
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)

# Streaming for large files
def stream_large_file(file_path: Path):
    """Stream large file instead of loading entirely."""
    with open(file_path, 'r') as f:
        for line in f:
            yield json.loads(line.strip())
```

### 5. Caching Strategies
```python
from functools import lru_cache, cache
import hashlib
import pickle
from pathlib import Path

# Function-level caching
@lru_cache(maxsize=256)
def expensive_color_calculation(r: int, g: int, b: int) -> tuple:
    """Expensive color calculation with caching."""
    # Simulate expensive computation
    import time
    time.sleep(0.01)  # 10ms delay
    return (r * 2, g * 2, b * 2, 255)

# Method-level caching
class CachedCanvas:
    """Canvas with method-level caching."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.pixels = [[None] * width for _ in range(height)]
        self._render_cache = {}
    
    def render_with_cache(self, zoom: int = 1) -> str:
        """Render canvas with caching."""
        cache_key = f"render_{zoom}_{hash(str(self.pixels))}"
        
        if cache_key in self._render_cache:
            return self._render_cache[cache_key]
        
        # Expensive rendering operation
        result = self._perform_rendering(zoom)
        self._render_cache[cache_key] = result
        return result
    
    def _perform_rendering(self, zoom: int) -> str:
        """Perform actual rendering."""
        # Simulate rendering
        return f"rendered_canvas_{zoom}x"

# File-based caching
class FileCache:
    """File-based caching system."""
    
    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cache_path(self, key: str) -> Path:
        """Get cache file path for key."""
        hash_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hash_key}.cache"
    
    def get(self, key: str) -> Optional[any]:
        """Get value from cache."""
        cache_path = self.get_cache_path(key)
        if cache_path.exists():
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None
    
    def set(self, key: str, value: any) -> None:
        """Set value in cache."""
        cache_path = self.get_cache_path(key)
        with open(cache_path, 'wb') as f:
            pickle.dump(value, f)
    
    def clear(self) -> None:
        """Clear all cache files."""
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink()

# Memoization for expensive operations
def memoize(func):
    """Memoization decorator."""
    cache = {}
    
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()
    return wrapper

@memoize
def complex_calculation(n: int, multiplier: float = 1.0) -> float:
    """Complex calculation with memoization."""
    # Simulate complex calculation
    result = 0
    for i in range(n):
        result += i * multiplier
    return result
```

### 6. Database Optimization
```python
import sqlite3
from contextlib import contextmanager
import json

# Connection pooling
class DatabasePool:
    """Database connection pool."""
    
    def __init__(self, db_path: str, max_connections: int = 10):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = []
        self.lock = asyncio.Lock()
    
    @contextmanager
    def get_connection(self):
        """Get database connection from pool."""
        if self.connections:
            conn = self.connections.pop()
        else:
            conn = sqlite3.connect(self.db_path)
        
        try:
            yield conn
        finally:
            if len(self.connections) < self.max_connections:
                self.connections.append(conn)
            else:
                conn.close()

# Batch operations
def batch_insert_pixels(db_pool: DatabasePool, pixels: List[tuple]):
    """Batch insert pixels for better performance."""
    with db_pool.get_connection() as conn:
        cursor = conn.cursor()
        
        # Use executemany for batch operations
        cursor.executemany(
            "INSERT INTO pixels (x, y, r, g, b, a) VALUES (?, ?, ?, ?, ?, ?)",
            pixels
        )
        conn.commit()

# Prepared statements
def optimized_pixel_queries(db_pool: DatabasePool):
    """Use prepared statements for better performance."""
    with db_pool.get_connection() as conn:
        cursor = conn.cursor()
        
        # Prepare statement once
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pixels (
                x INTEGER, y INTEGER, r INTEGER, g INTEGER, b INTEGER, a INTEGER,
                PRIMARY KEY (x, y)
            )
        """)
        
        # Use prepared statement
        insert_stmt = cursor.prepare(
            "INSERT OR REPLACE INTO pixels (x, y, r, g, b, a) VALUES (?, ?, ?, ?, ?, ?)"
        )
        
        return insert_stmt

# Indexing for better query performance
def create_optimized_schema(db_pool: DatabasePool):
    """Create optimized database schema with indexes."""
    with db_pool.get_connection() as conn:
        cursor = conn.cursor()
        
        # Create table with proper indexes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pixels (
                x INTEGER, y INTEGER, r INTEGER, g INTEGER, b INTEGER, a INTEGER,
                PRIMARY KEY (x, y)
            )
        """)
        
        # Create indexes for common queries
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pixels_color ON pixels (r, g, b, a)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_pixels_position ON pixels (x, y)")
        
        conn.commit()
```

---

## 📦 Dependency Management

### 1. Virtual Environments
```python
# Create virtual environment
# Windows:
python -m venv venv
venv\Scripts\activate

# Linux/Mac:
python -m venv venv
source venv/bin/activate

# Deactivate
deactivate

# Using virtualenv (alternative)
pip install virtualenv
virtualenv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 2. Requirements Management
```python
# requirements.txt - Basic dependencies
customtkinter>=5.2.0
Pillow>=10.0.0
numpy>=1.24.0
PyInstaller>=5.13.0

# requirements-dev.txt - Development dependencies
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
black>=23.0.0
flake8>=6.0.0
mypy>=1.5.0
pre-commit>=3.4.0

# requirements-prod.txt - Production dependencies
customtkinter>=5.2.0
Pillow>=10.0.0
numpy>=1.24.0

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 3. Poetry (Modern Dependency Management)
```python
# pyproject.toml - Poetry configuration
[tool.poetry]
name = "pixel-perfect"
version = "1.0.0"
description = "Pixel art editor"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.9"
customtkinter = "^5.2.0"
Pillow = "^10.0.0"
numpy = "^1.24.0"
PyInstaller = "^5.13.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-cov = "^4.1.0"
black = "^23.0.0"
flake8 = "^6.0.0"
mypy = "^1.5.0"

[tool.poetry.scripts]
pixel-perfect = "main:main"

# Poetry commands
poetry install          # Install dependencies
poetry add package      # Add new dependency
poetry add --dev package  # Add dev dependency
poetry update           # Update dependencies
poetry show             # Show installed packages
poetry export -f requirements.txt --output requirements.txt
```

### 4. Pipenv (Alternative)
```python
# Pipfile - Pipenv configuration
[[source]]
url = "https://pypi.org/simple"
verify_ssl = true
name = "pypi"

[packages]
customtkinter = ">=5.2.0"
Pillow = ">=10.0.0"
numpy = ">=1.24.0"
PyInstaller = ">=5.13.0"

[dev-packages]
pytest = ">=7.4.0"
pytest-cov = ">=4.1.0"
black = ">=23.0.0"
flake8 = ">=6.0.0"

[requires]
python_version = "3.9"

# Pipenv commands
pipenv install          # Install dependencies
pipenv install package  # Add new dependency
pipenv install --dev package  # Add dev dependency
pipenv update           # Update dependencies
pipenv shell            # Activate virtual environment
pipenv run command      # Run command in virtual environment
```

### 5. Security Considerations
```python
# Install security tools
pip install safety bandit pip-audit

# Check for known vulnerabilities
safety check
bandit -r src/
pip-audit

# Pin versions for security
# requirements.txt with pinned versions
customtkinter==5.2.0
Pillow==10.0.0
numpy==1.24.0
PyInstaller==5.13.0

# Use pip-tools for dependency compilation
pip install pip-tools
pip-compile requirements.in
pip-sync requirements.txt
```

### 6. Dependency Locking
```python
# requirements.in - High-level dependencies
customtkinter>=5.2.0
Pillow>=10.0.0
numpy>=1.24.0

# Generate locked requirements.txt
pip-compile requirements.in

# Result: requirements.txt with exact versions
customtkinter==5.2.0
Pillow==10.0.0
numpy==1.24.0
# ... all transitive dependencies with exact versions

# Update dependencies
pip-compile --upgrade requirements.in
```

### 7. Package Distribution
```python
# setup.py - Package configuration
from setuptools import setup, find_packages

setup(
    name="pixel-perfect",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "customtkinter>=5.2.0",
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "pixel-perfect=main:main",
        ],
    },
    python_requires=">=3.9",
)

# Build and distribute
python setup.py sdist bdist_wheel
pip install dist/pixel_perfect-1.0.0-py3-none-any.whl
```

---

## 🏗️ Maintainability Standards

### 1. Code Organization
```python
# Project structure following Python best practices
project/
├── src/
│   ├── pixel_perfect/
│   │   ├── __init__.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── canvas.py
│   │   │   ├── color_palette.py
│   │   │   └── project.py
│   │   ├── ui/
│   │   │   ├── __init__.py
│   │   │   ├── main_window.py
│   │   │   └── components/
│   │   │       ├── __init__.py
│   │   │       ├── color_wheel.py
│   │   │       └── layer_panel.py
│   │   ├── tools/
│   │   │   ├── __init__.py
│   │   │   ├── base_tool.py
│   │   │   ├── brush.py
│   │   │   └── eraser.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── export.py
│   │       └── file_operations.py
│   └── tests/
│       ├── __init__.py
│       ├── test_core/
│       ├── test_ui/
│       └── test_tools/
├── docs/
├── requirements.txt
├── pyproject.toml
├── setup.py
└── README.md
```

### 2. Documentation Standards
```python
# Module-level documentation
"""
Pixel Perfect - Professional Pixel Art Editor

This module provides the core functionality for creating and editing pixel art.
It includes canvas management, color palette handling, and drawing tools.

Example:
    >>> from pixel_perfect.core import Canvas
    >>> canvas = Canvas(32, 32)
    >>> canvas.set_pixel(10, 10, (255, 0, 0, 255))
"""

# Class documentation
class Canvas:
    """
    A canvas for pixel art creation and editing.
    
    The Canvas class manages pixel data and provides methods for drawing,
    erasing, and manipulating pixels. It supports multiple layers and
    various drawing operations.
    
    Attributes:
        width (int): Canvas width in pixels
        height (int): Canvas height in pixels
        pixels (List[List[Tuple[int, int, int, int]]]): 2D array of RGBA pixels
        
    Example:
        >>> canvas = Canvas(32, 32)
        >>> canvas.set_pixel(10, 10, (255, 0, 0, 255))
        >>> color = canvas.get_pixel(10, 10)
        >>> print(color)  # (255, 0, 0, 255)
    """
    
    def __init__(self, width: int, height: int):
        """
        Initialize a new canvas.
        
        Args:
            width: Canvas width in pixels (1-1024)
            height: Canvas height in pixels (1-1024)
            
        Raises:
            ValueError: If width or height is invalid
            
        Example:
            >>> canvas = Canvas(32, 32)
            >>> print(canvas.width, canvas.height)  # 32 32
        """
        if not (1 <= width <= 1024) or not (1 <= height <= 1024):
            raise ValueError("Canvas size must be between 1x1 and 1024x1024")
        
        self.width = width
        self.height = height
        self.pixels = [[(0, 0, 0, 0)] * width for _ in range(height)]
    
    def set_pixel(self, x: int, y: int, color: Tuple[int, int, int, int]) -> None:
        """
        Set a pixel at the specified coordinates.
        
        Args:
            x: X coordinate (0 to width-1)
            y: Y coordinate (0 to height-1)
            color: RGBA color tuple (0-255 each)
            
        Raises:
            ValueError: If coordinates are out of bounds
            TypeError: If color is not a 4-tuple of integers
            
        Example:
            >>> canvas = Canvas(32, 32)
            >>> canvas.set_pixel(10, 15, (255, 0, 0, 255))
            >>> color = canvas.get_pixel(10, 15)
            >>> print(color)  # (255, 0, 0, 255)
        """
        if not (0 <= x < self.width) or not (0 <= y < self.height):
            raise ValueError(f"Coordinates ({x}, {y}) out of bounds")
        
        if not isinstance(color, tuple) or len(color) != 4:
            raise TypeError("Color must be a 4-tuple of integers")
        
        if not all(isinstance(c, int) and 0 <= c <= 255 for c in color):
            raise ValueError("Color values must be integers between 0 and 255")
        
        self.pixels[y][x] = color
```

### 3. Linting & Formatting
```python
# .flake8 configuration
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude = 
    .git,
    __pycache__,
    .venv,
    venv,
    .tox,
    .eggs,
    *.egg,
    build,
    dist

# pyproject.toml for black
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | venv
  | _build
  | buck-out
  | build
  | dist
)/
'''

# mypy configuration
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

# pre-commit configuration
repos:
  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3.9
  
  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
  
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### 4. CI/CD Pipeline
```python
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11, 3.12]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/
    
    - name: Format check with black
      run: |
        black --check src/ tests/
    
    - name: Type check with mypy
      run: |
        mypy src/
    
    - name: Test with pytest
      run: |
        pytest --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install PyInstaller
    
    - name: Build executable
      run: |
        pyinstaller --onefile --windowed main.py
    
    - name: Upload build artifacts
      uses: actions/upload-artifact@v3
      with:
        name: pixel-perfect-${{ github.sha }}
        path: dist/
```

### 5. Error Handling & Logging
```python
import logging
import traceback
from typing import Optional
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pixel_perfect.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ProjectManager:
    """Manages project save/load operations with proper error handling."""
    
    def __init__(self):
        self.current_project: Optional[Project] = None
        self.project_path: Optional[Path] = None
    
    def save_project(self, file_path: Path) -> bool:
        """
        Save current project to file.
        
        Args:
            file_path: Path to save the project
            
        Returns:
            True if save successful, False otherwise
        """
        try:
            if not self.current_project:
                logger.warning("No project to save")
                return False
            
            # Validate file path
            if not file_path.parent.exists():
                file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save project data
            project_data = self.current_project.to_dict()
            
            with open(file_path, 'w') as f:
                json.dump(project_data, f, indent=2)
            
            self.project_path = file_path
            logger.info(f"Project saved successfully to {file_path}")
            return True
            
        except PermissionError as e:
            logger.error(f"Permission denied saving project: {e}")
            return False
            
        except OSError as e:
            logger.error(f"File system error saving project: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error saving project: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def load_project(self, file_path: Path) -> bool:
        """
        Load project from file.
        
        Args:
            file_path: Path to load the project from
            
        Returns:
            True if load successful, False otherwise
        """
        try:
            if not file_path.exists():
                logger.error(f"Project file not found: {file_path}")
                return False
            
            with open(file_path, 'r') as f:
                project_data = json.load(f)
            
            # Validate project data
            if not self._validate_project_data(project_data):
                logger.error("Invalid project data format")
                return False
            
            # Create project from data
            self.current_project = Project.from_dict(project_data)
            self.project_path = file_path
            
            logger.info(f"Project loaded successfully from {file_path}")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in project file: {e}")
            return False
            
        except Exception as e:
            logger.error(f"Unexpected error loading project: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def _validate_project_data(self, data: dict) -> bool:
        """Validate project data structure."""
        required_fields = ['version', 'canvas', 'layers']
        return all(field in data for field in required_fields)
```

### 6. Configuration Management
```python
from dataclasses import dataclass
from typing import Dict, Any
import json
from pathlib import Path

@dataclass
class AppConfig:
    """Application configuration."""
    canvas_width: int = 32
    canvas_height: int = 32
    default_zoom: int = 8
    theme: str = "dark"
    auto_save: bool = True
    auto_save_interval: int = 300  # seconds
    
    @classmethod
    def from_file(cls, config_path: Path) -> 'AppConfig':
        """Load configuration from file."""
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        return cls()
    
    def save_to_file(self, config_path: Path) -> None:
        """Save configuration to file."""
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(self.__dict__, f, indent=2)
    
    def update(self, **kwargs) -> None:
        """Update configuration values."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Unknown configuration key: {key}")

# Usage
config = AppConfig.from_file(Path("config/app_config.json"))
config.update(canvas_width=64, theme="light")
config.save_to_file(Path("config/app_config.json"))
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

## 🚀 Modern Python Features

### 1. Python 3.9+ Features
```python
# Union types with | operator (Python 3.10+)
def process_value(value: str | int | float) -> str:
    """Process different value types using modern union syntax."""
    return str(value)

# Match statements (Python 3.10+)
def handle_tool_selection(tool_type: str) -> str:
    """Handle tool selection using match statement."""
    match tool_type:
        case "brush":
            return "Brush tool selected"
        case "eraser":
            return "Eraser tool selected"
        case "fill":
            return "Fill tool selected"
        case _:
            return "Unknown tool"

# Structural pattern matching
def process_color(color: tuple) -> str:
    """Process color using structural pattern matching."""
    match color:
        case (r, g, b, a) if r == g == b == 0:
            return "Black"
        case (r, g, b, a) if r == g == b == 255:
            return "White"
        case (r, g, b, a) if r > 200 and g < 100 and b < 100:
            return "Red"
        case (r, g, b, a):
            return f"Color({r}, {g}, {b}, {a})"

# Positional-only parameters (Python 3.8+)
def create_canvas(width: int, height: int, /, *, name: str = "Canvas") -> 'Canvas':
    """Create canvas with positional-only parameters."""
    return Canvas(width, height, name=name)

# Usage: create_canvas(32, 32, name="My Canvas")  # OK
# Usage: create_canvas(width=32, height=32)       # Error - positional-only
```

### 2. Advanced Type Hints
```python
from typing import TypeVar, Generic, Protocol, Literal, TypedDict, Annotated
from dataclasses import dataclass
from enum import Enum

# Type variables for generic classes
T = TypeVar('T')

class Stack(Generic[T]):
    """Generic stack implementation."""
    def __init__(self) -> None:
        self._items: list[T] = []
    
    def push(self, item: T) -> None:
        self._items.append(item)
    
    def pop(self) -> T:
        return self._items.pop()
    
    def is_empty(self) -> bool:
        return len(self._items) == 0

# Protocols for structural typing
class Drawable(Protocol):
    """Protocol for drawable objects."""
    def draw(self, canvas: 'Canvas') -> None:
        """Draw the object on canvas."""
        ...

class Shape:
    """Shape that implements Drawable protocol."""
    def draw(self, canvas: 'Canvas') -> None:
        print("Drawing shape")

# Literal types
ToolType = Literal["brush", "eraser", "fill", "eyedropper"]

def set_tool(tool: ToolType) -> None:
    """Set the current tool."""
    print(f"Tool set to: {tool}")

# TypedDict for structured data
class PixelData(TypedDict):
    """Typed dictionary for pixel data."""
    x: int
    y: int
    r: int
    g: int
    b: int
    a: int

# Annotated types for additional metadata
from typing import Annotated

def set_pixel(
    x: Annotated[int, "X coordinate"],
    y: Annotated[int, "Y coordinate"],
    color: Annotated[tuple[int, int, int, int], "RGBA color"]
) -> None:
    """Set pixel with annotated types."""
    pass
```

### 3. Async/Await Patterns
```python
import asyncio
import aiohttp
from typing import AsyncGenerator, AsyncIterator

# Async context managers
class AsyncCanvas:
    """Async canvas for concurrent operations."""
    
    async def __aenter__(self):
        """Async context manager entry."""
        await self.initialize()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.cleanup()
    
    async def initialize(self) -> None:
        """Initialize canvas asynchronously."""
        await asyncio.sleep(0.1)  # Simulate initialization
    
    async def cleanup(self) -> None:
        """Cleanup canvas asynchronously."""
        await asyncio.sleep(0.1)  # Simulate cleanup

# Async generators
async def generate_pixels(width: int, height: int) -> AsyncGenerator[tuple[int, int], None]:
    """Generate pixel coordinates asynchronously."""
    for x in range(width):
        for y in range(height):
            yield (x, y)
            await asyncio.sleep(0.001)  # Yield control

# Async iteration
async def process_pixels_async(canvas: AsyncCanvas) -> None:
    """Process pixels asynchronously."""
    async for x, y in generate_pixels(32, 32):
        await canvas.set_pixel_async(x, y, (255, 0, 0, 255))

# Concurrent operations
async def load_multiple_projects(file_paths: list[str]) -> list[dict]:
    """Load multiple projects concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [load_project_async(session, path) for path in file_paths]
        return await asyncio.gather(*tasks)

async def load_project_async(session: aiohttp.ClientSession, path: str) -> dict:
    """Load a single project asynchronously."""
    # Simulate async file loading
    await asyncio.sleep(0.1)
    return {"path": path, "data": "project_data"}
```

### 4. Advanced Data Structures
```python
from collections import defaultdict, Counter, deque, ChainMap
from dataclasses import dataclass, field
from typing import DefaultDict, Deque
import heapq
from functools import total_ordering

# Advanced defaultdict usage
class Graph:
    """Graph implementation using defaultdict."""
    
    def __init__(self):
        self.adjacency: DefaultDict[str, list[str]] = defaultdict(list)
    
    def add_edge(self, from_node: str, to_node: str) -> None:
        """Add edge to graph."""
        self.adjacency[from_node].append(to_node)
        self.adjacency[to_node].append(from_node)
    
    def get_neighbors(self, node: str) -> list[str]:
        """Get neighbors of a node."""
        return self.adjacency[node]

# Priority queue with custom objects
@total_ordering
@dataclass
class Task:
    """Task with priority."""
    name: str
    priority: int
    data: dict = field(default_factory=dict)
    
    def __lt__(self, other: 'Task') -> bool:
        return self.priority < other.priority
    
    def __eq__(self, other: 'Task') -> bool:
        return self.priority == other.priority

class TaskQueue:
    """Priority queue for tasks."""
    
    def __init__(self):
        self._queue: list[Task] = []
    
    def add_task(self, task: Task) -> None:
        """Add task to queue."""
        heapq.heappush(self._queue, task)
    
    def get_next_task(self) -> Task:
        """Get next highest priority task."""
        return heapq.heappop(self._queue)
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return len(self._queue) == 0

# ChainMap for layered configuration
default_config = {
    "canvas_width": 32,
    "canvas_height": 32,
    "theme": "dark",
    "auto_save": True
}

user_config = {
    "canvas_width": 64,
    "theme": "light"
}

runtime_config = {
    "auto_save": False
}

# ChainMap allows overriding configs in order
config = ChainMap(runtime_config, user_config, default_config)
print(config["canvas_width"])  # 64 (from user_config)
print(config["auto_save"])      # False (from runtime_config)
```

### 5. Metaclasses and Descriptors
```python
from typing import Any, Optional
import weakref

# Descriptor for property validation
class ValidatedProperty:
    """Descriptor that validates property values."""
    
    def __init__(self, validator_func):
        self.validator_func = validator_func
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if not self.validator_func(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        instance.__dict__[self.name] = value

def validate_color(value):
    """Validate color value."""
    return isinstance(value, tuple) and len(value) == 4 and all(0 <= c <= 255 for c in value)

class Canvas:
    """Canvas with validated properties."""
    
    background_color = ValidatedProperty(validate_color)
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.background_color = (0, 0, 0, 0)  # Will be validated

# Metaclass for automatic registration
class ToolRegistry(type):
    """Metaclass for automatic tool registration."""
    
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if name != 'BaseTool':
            ToolRegistry.register_tool(new_class)
        return new_class
    
    _tools = {}
    
    @classmethod
    def register_tool(cls, tool_class):
        """Register a tool class."""
        cls._tools[tool_class.__name__.lower()] = tool_class
    
    @classmethod
    def get_tool(cls, name: str):
        """Get tool by name."""
        return cls._tools.get(name.lower())

class BaseTool(metaclass=ToolRegistry):
    """Base tool class."""
    pass

class BrushTool(BaseTool):
    """Brush tool automatically registered."""
    pass

class EraserTool(BaseTool):
    """Eraser tool automatically registered."""
    pass

# Usage
brush = ToolRegistry.get_tool("brushtool")()  # Creates BrushTool instance
```

### 6. Context Managers and Resource Management
```python
from contextlib import contextmanager, asynccontextmanager, ExitStack
from typing import Generator, AsyncGenerator
import tempfile
import os

# Custom context manager
class CanvasContext:
    """Context manager for canvas operations."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.canvas = None
    
    def __enter__(self) -> 'Canvas':
        """Enter context."""
        self.canvas = Canvas(self.width, self.height)
        print(f"Canvas {self.width}x{self.height} created")
        return self.canvas
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        """Exit context."""
        if exc_type is not None:
            print(f"Error in canvas context: {exc_val}")
        print("Canvas context cleaned up")
        return False  # Don't suppress exceptions

# Context manager decorator
@contextmanager
def temporary_canvas(width: int, height: int) -> Generator['Canvas', None, None]:
    """Create temporary canvas context."""
    canvas = Canvas(width, height)
    try:
        yield canvas
    finally:
        canvas.cleanup()

# Async context manager
@asynccontextmanager
async def async_canvas_context(width: int, height: int) -> AsyncGenerator['Canvas', None]:
    """Async canvas context manager."""
    canvas = await create_canvas_async(width, height)
    try:
        yield canvas
    finally:
        await canvas.cleanup_async()

# ExitStack for multiple context managers
def process_multiple_files(file_paths: list[str]) -> None:
    """Process multiple files using ExitStack."""
    with ExitStack() as stack:
        files = [stack.enter_context(open(path, 'r')) for path in file_paths]
        for file in files:
            content = file.read()
            print(f"Processing {file.name}: {len(content)} characters")

# Usage examples
with CanvasContext(32, 32) as canvas:
    canvas.set_pixel(10, 10, (255, 0, 0, 255))

with temporary_canvas(64, 64) as canvas:
    canvas.fill((0, 255, 0, 255))
```

### 7. Performance Optimization Techniques
```python
import functools
import operator
from typing import Callable, Any
import time

# Memoization with custom cache
def memoize_with_ttl(ttl_seconds: int = 300):
    """Memoize function with time-to-live."""
    def decorator(func: Callable) -> Callable:
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = str(args) + str(sorted(kwargs.items()))
            now = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl_seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        wrapper.cache_clear = lambda: cache.clear()
        return wrapper
    return decorator

@memoize_with_ttl(ttl_seconds=60)
def expensive_calculation(n: int) -> int:
    """Expensive calculation with TTL cache."""
    time.sleep(0.1)  # Simulate expensive operation
    return n * n

# Lazy evaluation
class LazyCanvas:
    """Canvas with lazy evaluation."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self._pixels = None
        self._dirty = True
    
    @property
    def pixels(self) -> list[list[tuple]]:
        """Lazy-loaded pixels."""
        if self._pixels is None or self._dirty:
            self._pixels = [[(0, 0, 0, 0)] * self.width for _ in range(self.height)]
            self._dirty = False
        return self._pixels
    
    def set_pixel(self, x: int, y: int, color: tuple) -> None:
        """Set pixel and mark as dirty."""
        self.pixels[y][x] = color
        self._dirty = True

# Function composition
def compose(*functions):
    """Compose multiple functions."""
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)

def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2

def square(x: int) -> int:
    return x * x

# Compose functions: square(multiply_by_two(add_one(x)))
composed = compose(square, multiply_by_two, add_one)
result = composed(3)  # square(multiply_by_two(add_one(3))) = square(multiply_by_two(4)) = square(8) = 64
```

---

**Remember**: You're not just writing code—you're collaborating with humans and future AI agents. Write code that's clear, maintainable, and true to the project's vision.

---

*This document is a living resource. Update it as you discover new patterns, pitfalls, and best practices.*

**Version**: 2.0  
**Created**: October 15, 2025  
**Enhanced**: December 2024  
**For**: AI Agents working with Python in Cursor IDE


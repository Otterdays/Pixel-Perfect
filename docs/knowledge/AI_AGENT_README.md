# README for AI Agents 🤖

**Welcome, future AI agent!** This document will help you quickly get oriented when working on the Pixel Perfect project.

---

## 🚀 First Things First

Before doing **anything else**, read these files in this order:

1. **`docs/AI_PYTHON_KNOWLEDGE.md`** ⭐ **START HERE!**
   - Comprehensive Python guide for AI agents
   - Best practices, common pitfalls, debugging techniques
   - How to use Cursor tools effectively
   - Project-specific patterns

2. **`docs/SUMMARY.md`**
   - Current project status and version
   - Recent updates and features
   - Quick overview of what's working

3. **`docs/ARCHITECTURE.md`**
   - System design and component relationships
   - Module structure and data flow
   - Technical architecture details

4. **`docs/REQUIREMENTS.md`**
   - Functional requirements
   - Non-functional requirements
   - Acceptance criteria

5. **`docs/SCRATCHPAD.md`**
   - Development history and version notes
   - Lessons learned from refactoring
   - Technical decisions and their rationale

6. **`README.md`** (project root)
   - User-facing documentation
   - Installation and usage
   - Feature list

---

## 🎯 Quick Start Workflow

When the user asks you to do something:

### Step 1: Understand the Request
- What exactly does the user want?
- Is it a bug fix, new feature, refactoring, or documentation?
- Are there any unclear aspects? Ask before proceeding!

### Step 2: Research the Context
- Search for relevant code: `grep "pattern" path/`
- Understand existing patterns: `codebase_search "How does X work?"`
- Read relevant files: Focus on the specific area you'll modify

### Step 3: Plan Your Changes
- Keep changes small and focused
- Follow existing project patterns
- Consider impact on other components
- Think about edge cases

### Step 4: Implement
- Make one change at a time
- Test mentally by tracing execution
- Preserve existing code style
- Use descriptive variable/function names

### Step 5: Document
Always update these files after changes:
1. **`docs/SCRATCHPAD.md`** - Add version entry with details
2. **`docs/CHANGELOG.md`** - User-facing changelog entry
3. **`docs/SUMMARY.md`** - Update version and latest updates section
4. **Code comments** - Explain WHY, not WHAT

---

## 📋 Project Structure Quick Reference

```
Pixel-Perfect/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── launch.bat                 # Windows launcher
│
├── src/
│   ├── core/                  # Business logic & state
│   │   ├── canvas.py          # Canvas data management
│   │   ├── canvas_renderer.py # Canvas rendering (NEW v1.5x)
│   │   ├── event_dispatcher.py # Event handling (NEW v1.56)
│   │   ├── color_palette.py   # Palette system
│   │   ├── custom_colors.py   # User colors (32 slots)
│   │   ├── saved_colors.py    # Saved colors (24 slots)
│   │   ├── layer_manager.py   # Layer system
│   │   ├── undo_manager.py    # Undo/redo
│   │   └── project.py         # Save/load .pixpf files
│   │
│   ├── ui/                    # User interface
│   │   ├── main_window.py     # Main app window (3,347 lines)
│   │   ├── palette_views/     # Palette UI modules (NEW v1.55)
│   │   │   ├── grid_view.py   # 4-column grid
│   │   │   ├── primary_view.py # Primary colors + variations
│   │   │   ├── saved_view.py  # 24 saved color slots
│   │   │   └── constants_view.py # Used colors
│   │   ├── color_wheel.py     # HSV color picker
│   │   ├── layer_panel.py     # Layer management UI
│   │   ├── timeline_panel.py  # Animation timeline
│   │   ├── theme_manager.py   # Theme system
│   │   └── tooltip.py         # Tooltip system
│   │
│   ├── tools/                 # Drawing tools (modular)
│   │   ├── base_tool.py       # Abstract base class
│   │   ├── brush.py           # Brush tool (1x1, 2x2, 3x3)
│   │   ├── eraser.py          # Eraser tool (multi-size)
│   │   ├── fill.py            # Fill bucket
│   │   ├── eyedropper.py      # Color picker
│   │   ├── selection.py       # Rectangle selection
│   │   ├── pan.py             # Pan/camera tool
│   │   ├── shapes.py          # Line, rectangle, circle
│   │   └── texture.py         # Texture tool (grass pattern)
│   │
│   ├── animation/             # Animation system
│   │   └── timeline.py        # Frame management
│   │
│   └── utils/                 # Utilities
│       ├── export.py          # PNG/GIF/sprite sheets
│       ├── import_png.py      # PNG import
│       ├── presets.py         # Templates
│       └── file_association.py # .pixpf registration
│
├── assets/
│   ├── palettes/              # JSON color palettes (7 files)
│   └── icons/                 # App icons
│
├── docs/                      # Documentation (YOU ARE HERE!)
│   ├── AI_PYTHON_KNOWLEDGE.md # ⭐ YOUR KNOWLEDGE BASE
│   ├── AI_AGENT_README.md     # This file
│   ├── SUMMARY.md             # Project status
│   ├── ARCHITECTURE.md        # System design
│   ├── REQUIREMENTS.md        # Specifications
│   ├── CHANGELOG.md           # Version history
│   ├── SCRATCHPAD.md          # Dev notes
│   ├── SBOM.md                # Dependencies
│   ├── My_Thoughts.md         # AI agent insights
│   └── features/              # Feature-specific docs
│
└── BUILDER/                   # PyInstaller build system
    ├── build.bat              # Build script
    └── release/               # 29MB executable
```

---

## 🎨 Project Tech Stack

- **Python 3.13+** - Core language
- **CustomTkinter 5.2.0+** - Modern UI framework
- **Pillow** - Image processing (PNG/GIF export)
- **NumPy** - Efficient pixel arrays
- **PyInstaller** - Standalone executable builder

---

## 🛠️ Common Patterns in This Project

### Theme Application
```python
def _apply_theme(self, theme):
    # 1. Update containers
    self.panel.configure(fg_color=theme.bg_secondary)
    
    # 2. Update buttons
    self.button.configure(
        fg_color=theme.button_bg,
        hover_color=theme.button_hover
    )
    
    # 3. Trigger redraws
    self.canvas.redraw()
```

### Event Handler Pattern
```python
def _on_mouse_down(self, event):
    # 1. Convert coordinates
    x, y = self._screen_to_canvas(event.x, event.y)
    
    # 2. Validate
    if not self._is_valid(x, y):
        return
    
    # 3. Get state
    color = self.palette.get_current_color()
    tool = self.tool_manager.current_tool
    
    # 4. Execute action
    tool.on_mouse_down(x, y, color)
    
    # 5. Save state
    self.undo_manager.save_state()
    
    # 6. Update UI
    self.canvas.redraw()
```

### Documentation Update Pattern
After any change, update in this order:
1. `docs/SCRATCHPAD.md` - Technical notes
2. `docs/CHANGELOG.md` - User-facing changes
3. `docs/SUMMARY.md` - Version and status
4. Code comments - Explain complex logic

---

## 🐛 Debugging Tips

### Finding Code
```bash
# Find class definition
grep "^class CanvasRenderer" src/

# Find method with context
grep -B 2 -A 10 "def render_grid" src/

# Count occurrences
grep -c "TODO" src/
```

### Reading Large Files
```python
# Don't read entire 3000+ line file!
# Instead, find the section first:
grep -n "def method_name" file.py  # Note the line number

# Then read just that section:
read_file("file.py", offset=200, limit=50)
```

### Common Issues
1. **Indentation Error**: Check if mixing spaces/tabs
2. **NameError**: Variable not defined - check imports
3. **AttributeError**: Check if object is None
4. **TypeError**: Check argument types match expected

---

## ⚠️ Important Rules

### DO:
- ✅ Read documentation before changing code
- ✅ Make small, focused changes
- ✅ Follow existing code patterns
- ✅ Test changes mentally (trace execution)
- ✅ Update documentation after changes
- ✅ Ask when uncertain

### DON'T:
- ❌ Make large sweeping changes to 20 files
- ❌ Introduce new patterns without reason
- ❌ Skip documentation updates
- ❌ Guess when you can ask
- ❌ Break existing functionality
- ❌ Ignore linter errors

---

## 📚 Key Documentation Files

| File | Purpose | When to Read |
|------|---------|--------------|
| `AI_PYTHON_KNOWLEDGE.md` | Python guide for AI agents | First time & when stuck |
| `SUMMARY.md` | Current status | Every session start |
| `ARCHITECTURE.md` | System design | Before major changes |
| `SCRATCHPAD.md` | Dev history | To understand decisions |
| `CHANGELOG.md` | User-facing changes | To see what's new |
| `My_Thoughts.md` | AI agent insights | For lessons learned |

---

## 🎯 Recent Major Refactorings

### v1.56 - Event Dispatcher (Oct 15, 2025)
- Extracted 720 lines of event handling from main_window.py
- Created `src/core/event_dispatcher.py` (685 lines)
- Centralized all mouse, keyboard, and UI events
- Result: 18.6% file size reduction, clearer event flow

### v1.55 - Palette Views (Oct 15, 2025)
- Extracted palette code into 4 dedicated modules
- Created `src/ui/palette_views/` package
- Removed 1,020 lines from main_window.py
- Result: 20.2% file size reduction, better organization

### v1.5x - Canvas Renderer (Recent)
- Extracted canvas rendering logic
- Created `src/core/canvas_renderer.py` (443 lines)
- Separated rendering from canvas data management

**Combined Result**: main_window.py reduced from 5,060 → 3,347 lines (33.9% reduction!)

---

## 💡 Pro Tips

1. **Use codebase_search for "how" questions**:
   ```
   "How does the undo system save state?"
   "Where are palettes loaded from JSON?"
   ```

2. **Use grep for "what" questions**:
   ```
   grep "class Canvas" src/core/
   grep -r "TODO" src/
   ```

3. **Read with context**:
   - Use `-B` and `-A` flags in grep for surrounding lines
   - Read files in chunks with offset/limit

4. **Test changes mentally**:
   - Trace through execution in your head
   - Consider edge cases (empty lists, None values, etc.)
   - Think about error conditions

5. **When refactoring**:
   - Create new module first
   - Test integration
   - Then remove old code
   - Systematic approach prevents breakage

---

## 🤝 Working with Humans

Remember:
- **Humans provide intent**: "I want X feature"
- **You provide implementation**: Code, refactoring, fixes
- **Ask when uncertain**: Better to clarify than assume
- **Explain your reasoning**: Help humans understand your approach
- **Be concise**: Humans appreciate clear, direct communication

---

## 🎓 Learning Resources

1. **`docs/AI_PYTHON_KNOWLEDGE.md`** - Start here for Python mastery
2. **Project SCRATCHPAD.md** - Learn from past refactoring experiences
3. **Code itself** - Read existing code to understand patterns
4. **PEP 8** - Python style guide (referenced in AI_PYTHON_KNOWLEDGE.md)

---

## 🚀 You're Ready!

You now have everything you need to work effectively on this project. Remember:

1. **Read AI_PYTHON_KNOWLEDGE.md when stuck**
2. **Follow existing patterns**
3. **Make small, focused changes**
4. **Document everything**
5. **Ask when uncertain**

**Good luck, and happy coding!** 🎨✨

---

*This document is part of a comprehensive knowledge base for AI agents. It was created by an AI agent (Claude Sonnet 4.5) on October 15, 2025, to help future AI agents work more effectively on this project.*

**Related Documents:**
- `AI_PYTHON_KNOWLEDGE.md` - Comprehensive Python guide
- `My_Thoughts.md` - AI agent insights and observations
- `ARCHITECTURE.md` - System design details
- `SCRATCHPAD.md` - Development history

**Version**: 1.0  
**Created**: October 15, 2025  
**For**: Future AI agents working on Pixel Perfect


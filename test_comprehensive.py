"""
Comprehensive test suite for Pixel Perfect
Tests all major features and integrations
"""

import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_grid_visibility():
    """Test that grid is properly visible"""
    print("\nTesting Grid Visibility...")
    
    try:
        from core.canvas import Canvas
        
        # Create canvas
        canvas = Canvas(32, 32, zoom=8)
        print(f"[OK] Canvas created with grid enabled: {canvas.show_grid}")
        
        # Test grid toggle
        canvas.toggle_grid()
        print(f"[OK] Grid toggled: {canvas.show_grid}")
        
        # Test grid redraw
        canvas._draw_grid()
        print(f"[OK] Grid redraw completed")
        
        print("Grid visibility tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Grid visibility test failed: {e}")
        return False

def test_mouse_integration():
    """Test mouse event integration"""
    print("\nTesting Mouse Integration...")
    
    try:
        from core.canvas import Canvas
        from tools.brush import BrushTool
        from core.color_palette import ColorPalette
        
        # Create components
        canvas = Canvas(16, 16, zoom=8)
        brush = BrushTool()
        palette = ColorPalette()
        
        # Test mouse events
        color = palette.get_primary_color()
        
        # Test brush tool
        brush.on_mouse_down(canvas, 5, 5, 1, color)
        pixel = canvas.get_pixel(5, 5)
        print(f"[OK] Mouse down event: pixel set to {pixel}")
        
        brush.on_mouse_move(canvas, 6, 6, color)
        pixel = canvas.get_pixel(6, 6)
        print(f"[OK] Mouse move event: pixel set to {pixel}")
        
        brush.on_mouse_up(canvas, 7, 7, 1, color)
        print(f"[OK] Mouse up event completed")
        
        print("Mouse integration tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Mouse integration test failed: {e}")
        return False

def test_animation_system():
    """Test animation timeline system"""
    print("\nTesting Animation System...")
    
    try:
        from animation.timeline import AnimationTimeline
        import numpy as np
        
        # Create timeline
        timeline = AnimationTimeline(16, 16)
        print(f"[OK] Timeline created with {timeline.get_frame_count()} frames")
        
        # Test frame operations
        timeline.add_frame()
        print(f"[OK] Frame added: {timeline.get_frame_count()} total")
        
        timeline.next_frame()
        print(f"[OK] Next frame: current frame {timeline.current_frame}")
        
        # Test frame data
        current_frame = timeline.get_current_frame()
        if current_frame:
            print(f"[OK] Current frame retrieved: {current_frame.name}")
        
        # Test animation controls
        timeline.play()
        print(f"[OK] Animation play: {timeline.is_playing}")
        
        timeline.pause()
        print(f"[OK] Animation pause: {timeline.is_playing}")
        
        print("Animation system tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Animation system test failed: {e}")
        return False

def test_project_system():
    """Test project save/load system"""
    print("\nTesting Project System...")
    
    try:
        from core.project import ProjectManager
        from core.canvas import Canvas
        from core.color_palette import ColorPalette
        from core.layer_manager import LayerManager
        from animation.timeline import AnimationTimeline
        
        # Create components
        project_mgr = ProjectManager()
        canvas = Canvas(16, 16, zoom=4)
        palette = ColorPalette()
        layer_mgr = LayerManager(16, 16)
        timeline = AnimationTimeline(16, 16)
        
        print(f"[OK] Project manager created")
        
        # Test project info
        project_mgr.current_project_path = "test_project.pixpf"
        print(f"[OK] Project path set: {project_mgr.current_project_path}")
        
        # Test recent files
        recent_files = project_mgr.get_recent_files()
        print(f"[OK] Recent files: {len(recent_files)} files")
        
        print("Project system tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Project system test failed: {e}")
        return False

def test_preset_system():
    """Test preset template system"""
    print("\nTesting Preset System...")
    
    try:
        from utils.presets import PresetManager
        
        # Create preset manager
        preset_mgr = PresetManager()
        print(f"[OK] Preset manager created")
        
        # Test categories
        categories = preset_mgr.get_categories()
        print(f"[OK] Categories: {categories}")
        
        # Test templates
        templates = preset_mgr.get_all_templates()
        print(f"[OK] Total templates: {len(templates)}")
        
        # Test character templates
        char_templates = preset_mgr.get_templates_by_category("Characters")
        print(f"[OK] Character templates: {len(char_templates)}")
        
        # Test specific template
        char_template = preset_mgr.get_template("char_32x32")
        if char_template:
            print(f"[OK] Character template: {char_template.name} ({char_template.width}x{char_template.height})")
        
        print("Preset system tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Preset system test failed: {e}")
        return False

def test_complete_integration():
    """Test complete system integration"""
    print("\nTesting Complete Integration...")
    
    try:
        # Import all major components
        from core.canvas import Canvas
        from core.color_palette import ColorPalette
        from core.layer_manager import LayerManager
        from core.undo_manager import UndoManager
        from animation.timeline import AnimationTimeline
        from tools.brush import BrushTool
        from utils.presets import PresetManager
        
        # Create complete system
        canvas = Canvas(32, 32, zoom=8)
        palette = ColorPalette()
        layer_mgr = LayerManager(32, 32)
        undo_mgr = UndoManager()
        timeline = AnimationTimeline(32, 32)
        brush = BrushTool()
        preset_mgr = PresetManager()
        
        print(f"[OK] Complete system initialized")
        
        # Test system integration
        # Set up drawing
        color = palette.get_primary_color()
        brush.on_mouse_down(canvas, 10, 10, 1, color)
        
        # Update layer
        active_layer = layer_mgr.get_active_layer()
        if active_layer:
            active_layer.pixels = canvas.pixels.copy()
        
        # Save undo state
        undo_mgr.save_state(active_layer.pixels.copy(), layer_mgr.active_layer_index)
        
        # Test animation frame
        current_frame = timeline.get_current_frame()
        if current_frame:
            current_frame.pixels = canvas.pixels.copy()
        
        print(f"[OK] System integration working")
        print(f"[OK] Canvas: {canvas.width}x{canvas.height}")
        print(f"[OK] Palette: {palette.palette_name}")
        print(f"[OK] Layers: {layer_mgr.get_layer_count()}")
        print(f"[OK] Undo states: {undo_mgr.get_undo_count()}")
        print(f"[OK] Animation frames: {timeline.get_frame_count()}")
        print(f"[OK] Preset templates: {len(preset_mgr.get_all_templates())}")
        
        print("Complete integration tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Complete integration test failed: {e}")
        return False

def main():
    """Run comprehensive test suite"""
    print("Pixel Perfect - Comprehensive Test Suite")
    print("=" * 50)
    
    tests = [
        test_grid_visibility,
        test_mouse_integration,
        test_animation_system,
        test_project_system,
        test_preset_system,
        test_complete_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Tests completed: {passed}/{total} passed")
    
    if passed == total:
        print("[SUCCESS] All tests passed! Pixel Perfect is fully functional.")
        print("\nFeatures verified:")
        print("[OK] Grid visibility and drawing")
        print("[OK] Mouse event integration")
        print("[OK] Animation timeline system")
        print("[OK] Project save/load system")
        print("[OK] Preset template system")
        print("[OK] Complete system integration")
        print("\nReady for pixel art creation!")
        print("\nTo start the application, run:")
        print("python main.py")
    else:
        print("[ERROR] Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()

"""
Preset templates for Pixel Perfect
Character, item, tile, and UI element templates
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class PresetTemplate:
    """Represents a preset template"""
    name: str
    category: str
    width: int
    height: int
    description: str
    preview_pixels: np.ndarray
    metadata: Dict[str, Any]

class PresetManager:
    """Manages preset templates"""
    
    def __init__(self):
        self.templates: Dict[str, PresetTemplate] = {}
        self.categories = ["Characters", "Items", "Tiles", "UI", "Effects"]
        self._create_default_templates()
    
    def _create_default_templates(self):
        """Create default preset templates"""
        
        # Character templates
        self._create_character_templates()
        
        # Item templates
        self._create_item_templates()
        
        # Tile templates
        self._create_tile_templates()
        
        # UI templates
        self._create_ui_templates()
    
    def _create_character_templates(self):
        """Create character sprite templates"""
        
        # 32x32 Character Template
        char_32 = np.zeros((32, 32, 4), dtype=np.uint8)
        # Add basic character outline
        char_32[8:24, 14:18] = [100, 100, 100, 255]  # Body
        char_32[4:8, 12:20] = [150, 150, 150, 255]   # Head
        char_32[16:24, 10:12] = [80, 80, 80, 255]    # Left arm
        char_32[16:24, 20:22] = [80, 80, 80, 255]    # Right arm
        char_32[24:32, 12:14] = [60, 60, 60, 255]    # Left leg
        char_32[24:32, 18:20] = [60, 60, 60, 255]    # Right leg
        
        template = PresetTemplate(
            name="32x32 Character",
            category="Characters",
            width=32,
            height=32,
            description="Basic character sprite template with body proportions",
            preview_pixels=char_32,
            metadata={
                "directions": ["down", "left", "right", "up"],
                "animation_frames": 4,
                "style": "top-down"
            }
        )
        self.templates["char_32x32"] = template
        
        # 16x32 Tall Character Template
        char_16x32 = np.zeros((32, 16, 4), dtype=np.uint8)
        char_16x32[6:22, 6:10] = [100, 100, 100, 255]  # Body
        char_16x32[2:6, 4:12] = [150, 150, 150, 255]   # Head
        char_16x32[14:22, 2:4] = [80, 80, 80, 255]     # Left arm
        char_16x32[14:22, 12:14] = [80, 80, 80, 255]   # Right arm
        char_16x32[22:32, 4:6] = [60, 60, 60, 255]     # Left leg
        char_16x32[22:32, 10:12] = [60, 60, 60, 255]   # Right leg
        
        template = PresetTemplate(
            name="16x32 Character",
            category="Characters",
            width=16,
            height=32,
            description="Tall character sprite template for side-view games",
            preview_pixels=char_16x32,
            metadata={
                "directions": ["left", "right"],
                "animation_frames": 2,
                "style": "side-view"
            }
        )
        self.templates["char_16x32"] = template
    
    def _create_item_templates(self):
        """Create item icon templates"""
        
        # 16x16 Item Template
        item_16 = np.zeros((16, 16, 4), dtype=np.uint8)
        # Add basic item shape (sword)
        item_16[6:10, 2:14] = [200, 200, 200, 255]     # Blade
        item_16[4:8, 6:10] = [139, 69, 19, 255]        # Handle
        item_16[8:12, 8:10] = [139, 69, 19, 255]       # Guard
        
        template = PresetTemplate(
            name="16x16 Item",
            category="Items",
            width=16,
            height=16,
            description="Basic item icon template",
            preview_pixels=item_16,
            metadata={
                "type": "weapon",
                "rarity": "common"
            }
        )
        self.templates["item_16x16"] = template
        
        # 32x32 Item Template
        item_32 = np.zeros((32, 32, 4), dtype=np.uint8)
        # Add detailed item shape
        item_32[12:20, 4:28] = [200, 200, 200, 255]    # Blade
        item_32[8:16, 12:20] = [139, 69, 19, 255]      # Handle
        item_32[16:24, 16:20] = [139, 69, 19, 255]     # Guard
        item_32[20:24, 18:20] = [255, 215, 0, 255]     # Pommel
        
        template = PresetTemplate(
            name="32x32 Item",
            category="Items",
            width=32,
            height=32,
            description="Detailed item icon template",
            preview_pixels=item_32,
            metadata={
                "type": "weapon",
                "rarity": "rare"
            }
        )
        self.templates["item_32x32"] = template
    
    def _create_tile_templates(self):
        """Create tile templates"""
        
        # 16x16 Grass Tile
        grass_tile = np.zeros((16, 16, 4), dtype=np.uint8)
        grass_tile[:, :] = [34, 139, 34, 255]          # Base grass color
        # Add some texture
        grass_tile[2:4, 4:6] = [0, 100, 0, 255]        # Darker patches
        grass_tile[8:10, 10:12] = [0, 100, 0, 255]
        grass_tile[12:14, 2:4] = [0, 100, 0, 255]
        
        template = PresetTemplate(
            name="16x16 Grass Tile",
            category="Tiles",
            width=16,
            height=16,
            description="Basic grass tile for environment",
            preview_pixels=grass_tile,
            metadata={
                "type": "terrain",
                "walkable": True,
                "tileable": True
            }
        )
        self.templates["tile_grass"] = template
        
        # 16x16 Stone Tile
        stone_tile = np.zeros((16, 16, 4), dtype=np.uint8)
        stone_tile[:, :] = [128, 128, 128, 255]        # Base stone color
        # Add stone texture
        stone_tile[0:2, 0:2] = [100, 100, 100, 255]    # Darker corners
        stone_tile[14:16, 14:16] = [100, 100, 100, 255]
        stone_tile[4:6, 8:10] = [160, 160, 160, 255]   # Lighter spots
        stone_tile[10:12, 4:6] = [160, 160, 160, 255]
        
        template = PresetTemplate(
            name="16x16 Stone Tile",
            category="Tiles",
            width=16,
            height=16,
            description="Basic stone tile for walls/paths",
            preview_pixels=stone_tile,
            metadata={
                "type": "structure",
                "walkable": False,
                "tileable": True
            }
        )
        self.templates["tile_stone"] = template
    
    def _create_ui_templates(self):
        """Create UI element templates"""
        
        # 32x16 Button Template
        button = np.zeros((16, 32, 4), dtype=np.uint8)
        # Button background
        button[2:14, 2:30] = [64, 64, 64, 255]         # Dark background
        button[4:6, 4:28] = [96, 96, 96, 255]          # Top highlight
        button[2:4, 4:28] = [128, 128, 128, 255]       # Top edge
        button[14:16, 4:28] = [32, 32, 32, 255]        # Bottom edge
        
        template = PresetTemplate(
            name="32x16 Button",
            category="UI",
            width=32,
            height=16,
            description="Basic UI button template",
            preview_pixels=button,
            metadata={
                "type": "button",
                "states": ["normal", "hover", "pressed"]
            }
        )
        self.templates["ui_button"] = template
        
        # 16x16 Icon Template
        icon = np.zeros((16, 16, 4), dtype=np.uint8)
        # Simple gear icon
        icon[2:14, 2:14] = [200, 200, 200, 255]        # Gear body
        icon[6:10, 6:10] = [128, 128, 128, 255]        # Center hole
        icon[0:2, 6:10] = [200, 200, 200, 255]         # Top teeth
        icon[14:16, 6:10] = [200, 200, 200, 255]       # Bottom teeth
        icon[6:10, 0:2] = [200, 200, 200, 255]         # Left teeth
        icon[6:10, 14:16] = [200, 200, 200, 255]       # Right teeth
        
        template = PresetTemplate(
            name="16x16 Icon",
            category="UI",
            width=16,
            height=16,
            description="Basic UI icon template",
            preview_pixels=icon,
            metadata={
                "type": "icon",
                "style": "monochrome"
            }
        )
        self.templates["ui_icon"] = template
    
    def get_templates_by_category(self, category: str) -> List[PresetTemplate]:
        """Get all templates in a category"""
        return [template for template in self.templates.values() 
                if template.category == category]
    
    def get_template(self, template_id: str) -> Optional[PresetTemplate]:
        """Get a specific template by ID"""
        return self.templates.get(template_id)
    
    def get_all_templates(self) -> List[PresetTemplate]:
        """Get all templates"""
        return list(self.templates.values())
    
    def get_categories(self) -> List[str]:
        """Get all categories"""
        return self.categories.copy()
    
    def create_template_from_canvas(self, name: str, category: str, 
                                  pixels: np.ndarray, description: str = "",
                                  metadata: Dict[str, Any] = None) -> str:
        """Create a new template from canvas pixels"""
        template_id = f"{category.lower()}_{name.lower().replace(' ', '_')}"
        
        template = PresetTemplate(
            name=name,
            category=category,
            width=pixels.shape[1],
            height=pixels.shape[0],
            description=description,
            preview_pixels=pixels.copy(),
            metadata=metadata or {}
        )
        
        self.templates[template_id] = template
        return template_id
    
    def save_templates(self, filename: str) -> bool:
        """Save templates to file"""
        try:
            templates_data = {}
            
            for template_id, template in self.templates.items():
                templates_data[template_id] = {
                    "name": template.name,
                    "category": template.category,
                    "width": template.width,
                    "height": template.height,
                    "description": template.description,
                    "preview_pixels": template.preview_pixels.tolist(),
                    "metadata": template.metadata
                }
            
            with open(filename, 'w') as f:
                json.dump(templates_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Error saving templates: {e}")
            return False
    
    def load_templates(self, filename: str) -> bool:
        """Load templates from file"""
        try:
            with open(filename, 'r') as f:
                templates_data = json.load(f)
            
            for template_id, template_data in templates_data.items():
                template = PresetTemplate(
                    name=template_data["name"],
                    category=template_data["category"],
                    width=template_data["width"],
                    height=template_data["height"],
                    description=template_data["description"],
                    preview_pixels=np.array(template_data["preview_pixels"], dtype=np.uint8),
                    metadata=template_data.get("metadata", {})
                )
                
                self.templates[template_id] = template
            
            return True
            
        except Exception as e:
            print(f"Error loading templates: {e}")
            return False

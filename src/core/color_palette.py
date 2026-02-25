"""
Color palette management for Pixel Perfect
Handles SNES-inspired palettes and custom color management
"""

import json
from typing import List, Tuple, Dict, Optional
from enum import Enum

class PaletteType(Enum):
    """Types of color palettes"""
    SNES_CLASSIC = "snes_classic"
    CUSTOM = "custom"

# Hardcoded JSON data to fix portable executable issue
HARDCODED_PALETTES_DATA = {
    "Curse of Aros": {
        "name": "Curse of Aros",
        "type": "curse_of_aros",
        "colors": [
            [
                45,
                45,
                45,
                255
            ],
            [
                89,
                89,
                89,
                255
            ],
            [
                134,
                134,
                134,
                255
            ],
            [
                101,
                67,
                33,
                255
            ],
            [
                139,
                90,
                43,
                255
            ],
            [
                67,
                101,
                33,
                255
            ],
            [
                90,
                139,
                43,
                255
            ],
            [
                33,
                67,
                101,
                255
            ],
            [
                43,
                90,
                139,
                255
            ],
            [
                101,
                33,
                67,
                255
            ],
            [
                139,
                43,
                90,
                255
            ],
            [
                67,
                101,
                67,
                255
            ],
            [
                90,
                139,
                90,
                255
            ],
            [
                33,
                33,
                33,
                255
            ],
            [
                200,
                200,
                200,
                255
            ],
            [
                255,
                255,
                255,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Definya": {
        "name": "Definya",
        "type": "definya",
        "colors": [
            [
                0,
                0,
                0,
                255
            ],
            [
                255,
                255,
                255,
                255
            ],
            [
                255,
                0,
                0,
                255
            ],
            [
                0,
                255,
                0,
                255
            ],
            [
                0,
                0,
                255,
                255
            ],
            [
                255,
                255,
                0,
                255
            ],
            [
                255,
                0,
                255,
                255
            ],
            [
                0,
                255,
                255,
                255
            ],
            [
                128,
                0,
                0,
                255
            ],
            [
                0,
                128,
                0,
                255
            ],
            [
                0,
                0,
                128,
                255
            ],
            [
                128,
                128,
                0,
                255
            ],
            [
                128,
                0,
                128,
                255
            ],
            [
                0,
                128,
                128,
                255
            ],
            [
                64,
                64,
                64,
                255
            ],
            [
                192,
                192,
                192,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Grass": {
        "name": "Grass",
        "type": "custom",
        "description": "16 variations of natural grass coloration",
        "colors": [
            [
                18,
                38,
                18,
                255
            ],
            [
                28,
                56,
                26,
                255
            ],
            [
                38,
                74,
                30,
                255
            ],
            [
                50,
                92,
                36,
                255
            ],
            [
                62,
                110,
                42,
                255
            ],
            [
                74,
                128,
                48,
                255
            ],
            [
                88,
                146,
                56,
                255
            ],
            [
                102,
                164,
                64,
                255
            ],
            [
                120,
                176,
                74,
                255
            ],
            [
                138,
                188,
                84,
                255
            ],
            [
                156,
                200,
                94,
                255
            ],
            [
                174,
                212,
                104,
                255
            ],
            [
                192,
                220,
                116,
                255
            ],
            [
                208,
                228,
                128,
                255
            ],
            [
                134,
                160,
                80,
                255
            ],
            [
                100,
                130,
                70,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Hair Colors (Extended)": {
        "name": "Hair Colors (Extended)",
        "type": "custom",
        "description": "Comprehensive 90-color hair palette (Blondes, Browns, Reds, Blacks, Greys/Whites, and Fantasy accents) with detailed shading ramps.",
        "colors": [
            [
                255,
                255,
                255,
                255
            ],
            [
                245,
                245,
                245,
                255
            ],
            [
                230,
                230,
                230,
                255
            ],
            [
                210,
                210,
                210,
                255
            ],
            [
                190,
                190,
                190,
                255
            ],
            [
                169,
                169,
                169,
                255
            ],
            [
                150,
                150,
                150,
                255
            ],
            [
                130,
                130,
                130,
                255
            ],
            [
                105,
                105,
                105,
                255
            ],
            [
                80,
                80,
                80,
                255
            ],
            [
                60,
                60,
                60,
                255
            ],
            [
                40,
                40,
                40,
                255
            ],
            [
                255,
                253,
                208,
                255
            ],
            [
                255,
                250,
                205,
                255
            ],
            [
                255,
                245,
                180,
                255
            ],
            [
                250,
                235,
                150,
                255
            ],
            [
                245,
                225,
                120,
                255
            ],
            [
                238,
                215,
                90,
                255
            ],
            [
                220,
                200,
                80,
                255
            ],
            [
                200,
                180,
                70,
                255
            ],
            [
                180,
                160,
                60,
                255
            ],
            [
                160,
                140,
                50,
                255
            ],
            [
                140,
                120,
                40,
                255
            ],
            [
                120,
                100,
                30,
                255
            ],
            [
                245,
                245,
                220,
                255
            ],
            [
                230,
                225,
                195,
                255
            ],
            [
                215,
                210,
                175,
                255
            ],
            [
                200,
                195,
                155,
                255
            ],
            [
                185,
                180,
                135,
                255
            ],
            [
                170,
                165,
                115,
                255
            ],
            [
                155,
                150,
                95,
                255
            ],
            [
                140,
                135,
                80,
                255
            ],
            [
                125,
                120,
                70,
                255
            ],
            [
                110,
                105,
                60,
                255
            ],
            [
                95,
                90,
                50,
                255
            ],
            [
                80,
                75,
                40,
                255
            ],
            [
                255,
                240,
                230,
                255
            ],
            [
                255,
                225,
                210,
                255
            ],
            [
                255,
                210,
                190,
                255
            ],
            [
                255,
                195,
                170,
                255
            ],
            [
                255,
                180,
                150,
                255
            ],
            [
                255,
                160,
                120,
                255
            ],
            [
                255,
                140,
                100,
                255
            ],
            [
                240,
                120,
                80,
                255
            ],
            [
                220,
                100,
                60,
                255
            ],
            [
                200,
                80,
                40,
                255
            ],
            [
                180,
                60,
                30,
                255
            ],
            [
                160,
                40,
                20,
                255
            ],
            [
                255,
                210,
                180,
                255
            ],
            [
                255,
                185,
                150,
                255
            ],
            [
                245,
                160,
                120,
                255
            ],
            [
                235,
                135,
                90,
                255
            ],
            [
                220,
                110,
                60,
                255
            ],
            [
                205,
                85,
                40,
                255
            ],
            [
                185,
                65,
                30,
                255
            ],
            [
                165,
                45,
                20,
                255
            ],
            [
                145,
                35,
                15,
                255
            ],
            [
                125,
                25,
                10,
                255
            ],
            [
                105,
                15,
                5,
                255
            ],
            [
                85,
                10,
                0,
                255
            ],
            [
                240,
                230,
                220,
                255
            ],
            [
                220,
                205,
                190,
                255
            ],
            [
                200,
                180,
                160,
                255
            ],
            [
                180,
                155,
                130,
                255
            ],
            [
                160,
                130,
                100,
                255
            ],
            [
                140,
                110,
                80,
                255
            ],
            [
                120,
                90,
                60,
                255
            ],
            [
                100,
                70,
                45,
                255
            ],
            [
                80,
                50,
                30,
                255
            ],
            [
                65,
                40,
                20,
                255
            ],
            [
                50,
                30,
                15,
                255
            ],
            [
                35,
                20,
                10,
                255
            ],
            [
                45,
                45,
                50,
                255
            ],
            [
                35,
                35,
                40,
                255
            ],
            [
                25,
                25,
                30,
                255
            ],
            [
                20,
                20,
                25,
                255
            ],
            [
                15,
                15,
                20,
                255
            ],
            [
                10,
                10,
                15,
                255
            ],
            [
                5,
                5,
                10,
                255
            ],
            [
                0,
                0,
                0,
                255
            ],
            [
                40,
                20,
                10,
                255
            ],
            [
                30,
                15,
                5,
                255
            ],
            [
                20,
                10,
                0,
                255
            ],
            [
                15,
                5,
                0,
                255
            ],
            [
                10,
                2,
                0,
                255
            ],
            [
                5,
                0,
                0,
                255
            ],
            [
                200,
                220,
                255,
                255
            ],
            [
                255,
                200,
                220,
                255
            ],
            [
                220,
                255,
                200,
                255
            ],
            [
                220,
                200,
                255,
                255
            ]
        ],
        "primary_color": 65,
        "secondary_color": 15
    },
    "Heartwood Online": {
        "name": "Heartwood Online",
        "type": "heartwood",
        "colors": [
            [
                34,
                51,
                34,
                255
            ],
            [
                68,
                85,
                68,
                255
            ],
            [
                102,
                119,
                102,
                255
            ],
            [
                51,
                68,
                34,
                255
            ],
            [
                85,
                102,
                68,
                255
            ],
            [
                119,
                136,
                102,
                255
            ],
            [
                68,
                51,
                34,
                255
            ],
            [
                102,
                85,
                68,
                255
            ],
            [
                136,
                119,
                102,
                255
            ],
            [
                51,
                51,
                34,
                255
            ],
            [
                85,
                85,
                68,
                255
            ],
            [
                119,
                119,
                102,
                255
            ],
            [
                34,
                34,
                34,
                255
            ],
            [
                68,
                68,
                68,
                255
            ],
            [
                102,
                102,
                102,
                255
            ],
            [
                136,
                136,
                136,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Kakele Online": {
        "name": "Kakele Online",
        "type": "kakele",
        "colors": [
            [
                255,
                255,
                0,
                255
            ],
            [
                255,
                128,
                0,
                255
            ],
            [
                255,
                0,
                0,
                255
            ],
            [
                255,
                0,
                128,
                255
            ],
            [
                128,
                0,
                255,
                255
            ],
            [
                0,
                0,
                255,
                255
            ],
            [
                0,
                128,
                255,
                255
            ],
            [
                0,
                255,
                255,
                255
            ],
            [
                0,
                255,
                128,
                255
            ],
            [
                0,
                255,
                0,
                255
            ],
            [
                128,
                255,
                0,
                255
            ],
            [
                255,
                255,
                128,
                255
            ],
            [
                128,
                128,
                128,
                255
            ],
            [
                64,
                64,
                64,
                255
            ],
            [
                192,
                192,
                192,
                255
            ],
            [
                255,
                255,
                255,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Old School RuneScape": {
        "name": "Old School RuneScape",
        "type": "old_school_runescape",
        "description": "Classic OSRS medieval fantasy palette with earthy tones, iconic interface colors, and low-saturation aesthetic from 2007-era RuneScape",
        "colors": [
            [
                0,
                0,
                0,
                255
            ],
            [
                255,
                255,
                255,
                255
            ],
            [
                139,
                69,
                19,
                255
            ],
            [
                36,
                97,
                49,
                255
            ],
            [
                125,
                102,
                48,
                255
            ],
            [
                255,
                215,
                0,
                255
            ],
            [
                128,
                0,
                0,
                255
            ],
            [
                1,
                111,
                189,
                255
            ],
            [
                246,
                103,
                57,
                255
            ],
            [
                225,
                158,
                37,
                255
            ],
            [
                112,
                128,
                144,
                255
            ],
            [
                101,
                67,
                33,
                255
            ],
            [
                192,
                192,
                192,
                255
            ],
            [
                76,
                105,
                38,
                255
            ],
            [
                70,
                70,
                70,
                255
            ],
            [
                160,
                82,
                45,
                255
            ]
        ]
    },
    "Rucoy Online": {
        "name": "Rucoy Online",
        "type": "rucoy",
        "colors": [
            [
                0,
                0,
                0,
                255
            ],
            [
                32,
                32,
                32,
                255
            ],
            [
                64,
                64,
                64,
                255
            ],
            [
                96,
                96,
                96,
                255
            ],
            [
                128,
                128,
                128,
                255
            ],
            [
                160,
                160,
                160,
                255
            ],
            [
                192,
                192,
                192,
                255
            ],
            [
                224,
                224,
                224,
                255
            ],
            [
                255,
                255,
                255,
                255
            ],
            [
                64,
                32,
                0,
                255
            ],
            [
                128,
                64,
                0,
                255
            ],
            [
                192,
                96,
                0,
                255
            ],
            [
                0,
                64,
                0,
                255
            ],
            [
                0,
                128,
                0,
                255
            ],
            [
                0,
                192,
                0,
                255
            ],
            [
                0,
                0,
                64,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    },
    "Skin Tones (Extended)": {
        "name": "Skin Tones (Extended)",
        "type": "custom",
        "description": "Comprehensive 88-color skin tone palette covering Cool, Neutral, Warm, and Olive undertones from pale to deep ebony.",
        "colors": [
            [
                255,
                245,
                245,
                255
            ],
            [
                255,
                235,
                235,
                255
            ],
            [
                255,
                225,
                225,
                255
            ],
            [
                255,
                215,
                215,
                255
            ],
            [
                255,
                205,
                205,
                255
            ],
            [
                245,
                195,
                195,
                255
            ],
            [
                235,
                180,
                180,
                255
            ],
            [
                225,
                165,
                165,
                255
            ],
            [
                215,
                150,
                150,
                255
            ],
            [
                205,
                135,
                135,
                255
            ],
            [
                195,
                120,
                120,
                255
            ],
            [
                180,
                105,
                105,
                255
            ],
            [
                165,
                90,
                90,
                255
            ],
            [
                150,
                75,
                75,
                255
            ],
            [
                135,
                60,
                60,
                255
            ],
            [
                120,
                45,
                45,
                255
            ],
            [
                105,
                35,
                35,
                255
            ],
            [
                90,
                25,
                25,
                255
            ],
            [
                75,
                15,
                15,
                255
            ],
            [
                60,
                10,
                10,
                255
            ],
            [
                45,
                5,
                5,
                255
            ],
            [
                30,
                0,
                0,
                255
            ],
            [
                255,
                248,
                240,
                255
            ],
            [
                255,
                240,
                225,
                255
            ],
            [
                255,
                232,
                210,
                255
            ],
            [
                255,
                224,
                195,
                255
            ],
            [
                250,
                215,
                180,
                255
            ],
            [
                245,
                205,
                165,
                255
            ],
            [
                240,
                195,
                150,
                255
            ],
            [
                235,
                185,
                135,
                255
            ],
            [
                230,
                175,
                120,
                255
            ],
            [
                220,
                165,
                105,
                255
            ],
            [
                210,
                155,
                90,
                255
            ],
            [
                200,
                145,
                75,
                255
            ],
            [
                190,
                130,
                65,
                255
            ],
            [
                175,
                115,
                55,
                255
            ],
            [
                160,
                100,
                45,
                255
            ],
            [
                145,
                85,
                35,
                255
            ],
            [
                130,
                70,
                25,
                255
            ],
            [
                115,
                55,
                20,
                255
            ],
            [
                100,
                45,
                15,
                255
            ],
            [
                85,
                35,
                10,
                255
            ],
            [
                70,
                25,
                5,
                255
            ],
            [
                55,
                15,
                0,
                255
            ],
            [
                255,
                250,
                240,
                255
            ],
            [
                255,
                245,
                225,
                255
            ],
            [
                255,
                240,
                210,
                255
            ],
            [
                255,
                230,
                190,
                255
            ],
            [
                255,
                220,
                170,
                255
            ],
            [
                245,
                210,
                155,
                255
            ],
            [
                235,
                200,
                140,
                255
            ],
            [
                225,
                190,
                125,
                255
            ],
            [
                215,
                180,
                110,
                255
            ],
            [
                205,
                165,
                95,
                255
            ],
            [
                195,
                150,
                80,
                255
            ],
            [
                185,
                135,
                65,
                255
            ],
            [
                170,
                120,
                50,
                255
            ],
            [
                155,
                105,
                40,
                255
            ],
            [
                140,
                90,
                30,
                255
            ],
            [
                125,
                75,
                20,
                255
            ],
            [
                110,
                60,
                15,
                255
            ],
            [
                95,
                50,
                10,
                255
            ],
            [
                80,
                40,
                5,
                255
            ],
            [
                65,
                30,
                0,
                255
            ],
            [
                50,
                20,
                0,
                255
            ],
            [
                35,
                10,
                0,
                255
            ],
            [
                250,
                250,
                235,
                255
            ],
            [
                245,
                245,
                220,
                255
            ],
            [
                235,
                235,
                200,
                255
            ],
            [
                225,
                225,
                180,
                255
            ],
            [
                215,
                215,
                160,
                255
            ],
            [
                200,
                200,
                140,
                255
            ],
            [
                185,
                185,
                120,
                255
            ],
            [
                170,
                170,
                100,
                255
            ],
            [
                155,
                155,
                80,
                255
            ],
            [
                140,
                140,
                65,
                255
            ],
            [
                125,
                125,
                50,
                255
            ],
            [
                110,
                110,
                40,
                255
            ],
            [
                95,
                95,
                30,
                255
            ],
            [
                80,
                80,
                20,
                255
            ],
            [
                65,
                65,
                15,
                255
            ],
            [
                50,
                50,
                10,
                255
            ],
            [
                40,
                40,
                5,
                255
            ],
            [
                30,
                30,
                0,
                255
            ],
            [
                240,
                230,
                210,
                255
            ],
            [
                220,
                210,
                190,
                255
            ],
            [
                200,
                190,
                170,
                255
            ],
            [
                160,
                150,
                130,
                255
            ]
        ],
        "primary_color": 30,
        "secondary_color": 50
    },
    "SNES Classic": {
        "name": "SNES Classic",
        "type": "snes_classic",
        "colors": [
            [
                0,
                0,
                0,
                255
            ],
            [
                255,
                255,
                255,
                255
            ],
            [
                128,
                128,
                128,
                255
            ],
            [
                255,
                0,
                0,
                255
            ],
            [
                0,
                255,
                0,
                255
            ],
            [
                0,
                0,
                255,
                255
            ],
            [
                255,
                255,
                0,
                255
            ],
            [
                255,
                0,
                255,
                255
            ],
            [
                0,
                255,
                255,
                255
            ],
            [
                128,
                64,
                0,
                255
            ],
            [
                255,
                128,
                0,
                255
            ],
            [
                128,
                0,
                128,
                255
            ],
            [
                0,
                128,
                0,
                255
            ],
            [
                0,
                0,
                128,
                255
            ],
            [
                128,
                128,
                0,
                255
            ],
            [
                192,
                192,
                192,
                255
            ]
        ],
        "primary_color": 0,
        "secondary_color": 1
    }
}

class ColorPalette:
    """Color palette management system"""
    
    def __init__(self):
        self.colors: List[Tuple[int, int, int, int]] = []
        self.primary_color = 0  # Index of primary color
        self.secondary_color = 1  # Index of secondary color
        self.palette_name = "Default"
        self.palette_type = PaletteType.CUSTOM
        
        self._hardcoded_palettes = HARDCODED_PALETTES_DATA
        
        # Load default palette
        self._load_default_palette()
    
    def _load_default_palette(self):
        """Load default SNES-inspired palette"""
        self.load_by_name("SNES Classic")

    def get_available_palette_names(self) -> List[str]:
        """Return available hardcoded palette names, sorted alphabetically."""
        return sorted(list(self._hardcoded_palettes.keys()))
    
    def _load_from_dict(self, data: dict):
        """Internal helper to load from a dictionary"""
        self.palette_name = data.get("name", "Custom")
        self.colors = [tuple(color) for color in data.get("colors", [])]
        self.primary_color = data.get("primary_color", 0)
        self.secondary_color = data.get("secondary_color", 1)
        
        # Set palette type
        palette_type_str = data.get("type", "custom")
        try:
            self.palette_type = PaletteType(palette_type_str)
        except ValueError:
            self.palette_type = PaletteType.CUSTOM

    def load_by_name(self, palette_name: str):
        """Load a hardcoded palette by name."""
        if palette_name in self._hardcoded_palettes:
            data = self._hardcoded_palettes[palette_name]
            self._load_from_dict(data)
            # Ensure valid primary/secondary indices
            if self.primary_color >= len(self.colors):
                self.primary_color = 0
            if self.secondary_color >= len(self.colors):
                self.secondary_color = min(1, len(self.colors) - 1)
            return
        print(f"Palette '{palette_name}' not found among hardcoded palettes.")
    
    def add_color(self, color: Tuple[int, int, int, int]):
        """Add a new color to the palette"""
        if len(self.colors) < 32:  # Limit to 32 colors
            self.colors.append(color)
    
    def remove_color(self, index: int):
        """Remove color at given index"""
        if 0 <= index < len(self.colors) and len(self.colors) > 1:
            self.colors.pop(index)
            
            # Adjust primary/secondary indices
            if self.primary_color >= len(self.colors):
                self.primary_color = len(self.colors) - 1
            if self.secondary_color >= len(self.colors):
                self.secondary_color = len(self.colors) - 1
    
    def set_color(self, index: int, color: Tuple[int, int, int, int]):
        """Set color at given index"""
        if 0 <= index < len(self.colors):
            self.colors[index] = color
    
    def get_primary_color(self) -> Tuple[int, int, int, int]:
        """Get primary color"""
        if self.colors and 0 <= self.primary_color < len(self.colors):
            return self.colors[self.primary_color]
        return (0, 0, 0, 255)
    
    def get_secondary_color(self) -> Tuple[int, int, int, int]:
        """Get secondary color"""
        if self.colors and 0 <= self.secondary_color < len(self.colors):
            return self.colors[self.secondary_color]
        return (255, 255, 255, 255)
    
    def set_primary_color(self, index: int):
        """Set primary color index"""
        if 0 <= index < len(self.colors):
            self.primary_color = index
    
    def set_secondary_color(self, index: int):
        """Set secondary color index"""
        if 0 <= index < len(self.colors):
            self.secondary_color = index
    
    def set_primary_color_by_rgba(self, rgba_color: Tuple[int, int, int, int]):
        """Set primary color by RGBA value (add to palette if not exists)"""
        for i, color in enumerate(self.colors):
            if color == rgba_color:
                self.primary_color = i
                return
        self.colors.append(rgba_color)
        self.primary_color = len(self.colors) - 1
    
    def swap_colors(self):
        """Swap primary and secondary colors"""
        self.primary_color, self.secondary_color = self.secondary_color, self.primary_color
    
    def find_color_in_presets(self, rgb_color: Tuple[int, int, int, int]) -> Optional[Tuple[str, int]]:
        """Search for a color across all hardcoded palettes."""
        for palette_name, data in self._hardcoded_palettes.items():
            try:
                colors = [tuple(c) for c in data.get("colors", [])]
                for i, color in enumerate(colors):
                    if tuple(color[:3]) == tuple(rgb_color[:3]):
                        return (palette_name, i)
            except Exception:
                continue
        return None
    
    def save_palette(self, filename: str):
        """Save palette to JSON file"""
        palette_data = {
            "name": self.palette_name,
            "type": self.palette_type.value,
            "colors": self.colors,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color
        }
        with open(filename, 'w') as f:
            json.dump(palette_data, f, indent=2)
    
    def load_palette(self, filename: str):
        """Load palette from JSON file"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self._load_from_dict(data)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading palette: {e}")
            self._load_default_palette()
    
    def get_color_count(self) -> int:
        """Get number of colors in palette"""
        return len(self.colors)
    
    def is_empty(self) -> bool:
        """Check if palette is empty"""
        return len(self.colors) == 0

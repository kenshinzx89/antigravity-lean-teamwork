# -*- coding: utf-8 -*-
"""
Unified Glass Material System for Cockpit Quota Widget V10 Pro Ultimate
Consolidates all optical properties, caustic reflections, gradient palettes,
and high-contrast status colors for seamless, non-fragmented rendering.
"""

import math


def ARGB(a, r, g, b):
    return ((int(a) & 0xFF) << 24) | ((int(r) & 0xFF) << 16) | ((int(g) & 0xFF) << 8) | (int(b) & 0xFF)


GLASS_MODES = [
    'deep_obsidian',      # 🌌 Kính đen sâu 88%
    'smoked_glass',       # 🌫️ Kính khói mờ 70%
    'frosted_diamond',    # 💎 Kính ngọc trai tuyết 88%
    'pure_frost',         # ❄️ Kính băng tuyết pha lê 82%
    'aurora_borealis',    # 🌈 Kính cực quang chuyển sắc
    'ghost_glass'         # 👻 Kính vô hình neon 94%
]

GLASS_NAMES = {
    'deep_obsidian': "🌌 Deep Obsidian (Kính đen sâu 88%)",
    'smoked_glass': "🌫️ Smoked Glass (Kính khói 70%)",
    'frosted_diamond': "💎 Frosted Diamond (Kính ngọc trai 88%)",
    'pure_frost': "❄️ Pure Frost (Kính băng tuyết pha lê)",
    'aurora_borealis': "🌈 Aurora Borealis (Kính cực quang)",
    'ghost_glass': "👻 Ghost Cyber Glass (Kính vô hình Neon)"
}


def get_material_palette(glass_mode, theme, tick=0):
    """
    Returns a unified, complete color & optical property dictionary
    for any given glass material and theme.
    """
    # 1. Special Cards Theme fallback (if user selects classic cards on dark glass)
    if theme == 'cards' and glass_mode not in ('pure_frost', 'frosted_diamond', 'ghost_glass', 'aurora_borealis'):
        return {
            'text_primary': ARGB(255, 248, 250, 252),
            'text_secondary': ARGB(255, 148, 163, 184),
            'text_shadow': ARGB(120, 0, 0, 0),
            'pill_bg_normal': ARGB(235, 15, 23, 42),
            'pill_bg_hover': ARGB(255, 30, 41, 59),
            'pill_border': ARGB(190, 71, 85, 105),
            'inner_refraction': ARGB(90, 255, 255, 255),
            'shadow_color': ARGB(90, 0, 0, 0),
            'purple_dot': ARGB(255, 168, 85, 247),
            'purple_halo': ARGB(120, 168, 85, 247),
            'ring_track': ARGB(55, 255, 255, 255),
            'shine_alpha': 80,
            'is_dark': True,
            'is_ghost': False
        }

    # 2. Deep Obsidian (🌌 Space Obsidian Glass)
    if glass_mode == 'deep_obsidian':
        return {
            'text_primary': ARGB(255, 250, 252, 255),
            'text_secondary': ARGB(255, 156, 175, 200),
            'text_shadow': ARGB(140, 0, 0, 0),
            'pill_bg_normal': ARGB(230, 10, 14, 26),
            'pill_bg_hover': ARGB(255, 22, 30, 50),
            'pill_border': ARGB(195, 59, 76, 102),
            'inner_refraction': ARGB(85, 255, 255, 255),
            'shadow_color': ARGB(95, 0, 0, 0),
            'purple_dot': ARGB(255, 168, 85, 247),
            'purple_halo': ARGB(130, 168, 85, 247),
            'ring_track': ARGB(50, 255, 255, 255),
            'shine_alpha': 80,
            'is_dark': True,
            'is_ghost': False
        }

    # 3. Smoked Glass (🌫️ Smoked Slate Glass)
    elif glass_mode == 'smoked_glass':
        return {
            'text_primary': ARGB(255, 245, 248, 252),
            'text_secondary': ARGB(255, 160, 176, 198),
            'text_shadow': ARGB(130, 0, 0, 0),
            'pill_bg_normal': ARGB(190, 20, 28, 44),
            'pill_bg_hover': ARGB(230, 30, 41, 62),
            'pill_border': ARGB(180, 80, 96, 120),
            'inner_refraction': ARGB(95, 255, 255, 255),
            'shadow_color': ARGB(75, 0, 0, 0),
            'purple_dot': ARGB(255, 168, 85, 247),
            'purple_halo': ARGB(120, 168, 85, 247),
            'ring_track': ARGB(55, 255, 255, 255),
            'shine_alpha': 75,
            'is_dark': True,
            'is_ghost': False
        }

    # 4. Frosted Diamond (💎 Frosted Diamond Pearlescent Glass)
    elif glass_mode == 'frosted_diamond':
        return {
            'text_primary': ARGB(255, 15, 23, 42),        # Slate 950 (High contrast)
            'text_secondary': ARGB(255, 71, 85, 105),     # Slate 600
            'text_shadow': ARGB(60, 255, 255, 255),       # Soft white relief
            'pill_bg_normal': ARGB(240, 255, 255, 255),   # Pearlescent White
            'pill_bg_hover': ARGB(255, 241, 245, 249),
            'pill_border': ARGB(210, 203, 213, 225),
            'inner_refraction': ARGB(180, 255, 255, 255),
            'shadow_color': ARGB(55, 15, 23, 42),
            'purple_dot': ARGB(255, 139, 92, 246),
            'purple_halo': ARGB(95, 139, 92, 246),
            'ring_track': ARGB(70, 100, 116, 139),
            'shine_alpha': 120,
            'is_dark': False,
            'is_ghost': False
        }

    # 5. Pure Frost (❄️ Pure Crystal Frost Sapphire Glass)
    elif glass_mode == 'pure_frost':
        return {
            'text_primary': ARGB(255, 8, 47, 73),         # Ultra Deep Sapphire Blue (Maximum Contrast)
            'text_secondary': ARGB(255, 3, 105, 161),     # Sky 700
            'text_shadow': ARGB(80, 255, 255, 255),       # Crisp Frost Specular
            'pill_bg_normal': ARGB(225, 238, 248, 255),   # Crystal Ice Translucent
            'pill_bg_hover': ARGB(255, 224, 242, 254),    # Ice Glaze Hover
            'pill_border': ARGB(235, 125, 211, 252),      # Sky 300 Ice Edge
            'inner_refraction': ARGB(210, 255, 255, 255), # Crystal Sparkle
            'shadow_color': ARGB(60, 14, 116, 144),       # Glacier Ambient Shadow
            'purple_dot': ARGB(255, 147, 51, 234),        # Purple Accent
            'purple_halo': ARGB(110, 192, 132, 252),
            'ring_track': ARGB(90, 186, 230, 253),
            'shine_alpha': 90,
            'is_dark': False,
            'is_ghost': False
        }

    # 6. Aurora Borealis (🌈 Northern Lights Glass)
    elif glass_mode == 'aurora_borealis':
        shift = math.sin(tick * math.pi / 18.0)
        r_val = int(18 + 12 * shift)
        g_val = int(24 + 16 * (1.0 - abs(shift)))
        b_val = int(48 + 20 * shift)
        return {
            'text_primary': ARGB(255, 250, 252, 255),
            'text_secondary': ARGB(255, 186, 230, 253),
            'text_shadow': ARGB(150, 0, 0, 0),
            'pill_bg_normal': ARGB(215, r_val, g_val, b_val),
            'pill_bg_hover': ARGB(245, min(255, r_val + 15), min(255, g_val + 15), min(255, b_val + 20)),
            'pill_border': ARGB(215, 56, 189, 248),
            'inner_refraction': ARGB(130, 125, 211, 252),
            'shadow_color': ARGB(85, 2, 6, 23),
            'purple_dot': ARGB(255, 192, 132, 252),
            'purple_halo': ARGB(140, 192, 132, 252),
            'ring_track': ARGB(60, 255, 255, 255),
            'shine_alpha': 80,
            'is_dark': True,
            'is_ghost': False
        }

    # 7. Ghost Cyber Glass (👻 Masterpiece Invisible Neon Glass)
    elif glass_mode == 'ghost_glass':
        pulse = (math.sin(tick * math.pi / 16.0) + 1.0) / 2.0
        border_alpha = int(180 + 60 * pulse)
        return {
            'text_primary': ARGB(255, 56, 189, 248),       # Electric Cyan Neon Text
            'text_secondary': ARGB(255, 148, 163, 184),    # Slate 400
            'text_shadow': ARGB(160, 0, 0, 0),             # Shadow for high readability over bright wallpapers
            'pill_bg_normal': ARGB(45, 15, 23, 42),        # Subtle anti-glare tint
            'pill_bg_hover': ARGB(75, 56, 189, 248),       # Soft Cyan Glow on Hover
            'pill_border': ARGB(border_alpha, 56, 189, 248),# Breathing Neon Border
            'inner_refraction': ARGB(140, 255, 255, 255),  # Crystal Top Specular Line
            'shadow_color': ARGB(50, 2, 6, 23),            # Micro Ambient Drop
            'purple_dot': ARGB(255, 192, 132, 252),        # Purple Neon Dot
            'purple_halo': ARGB(150, 192, 132, 252),
            'ring_track': ARGB(55, 56, 189, 248),
            'shine_alpha': 45,
            'is_dark': True,
            'is_ghost': True
        }

    # Default fallback to Deep Obsidian
    return get_material_palette('deep_obsidian', theme, tick)


def get_status_colors(pct, is_dark, theme='cards', orbit_green='blue', tick=0):
    """
    Returns high-contrast, razor-sharp status fill and text colors with
    smart yellow (20-49%) and red (<20%) threshold warnings on all themes.
    """
    # 1. CRITICAL LOW ALERT (Quota < 20%) -> CRIMSON / NEON RED
    if pct < 20:
        pulse = (math.sin(tick * math.pi / 10.0) + 1.0) / 2.0
        if is_dark:
            # Pulsing Crimson Neon with High Luminescence
            r_boost = int(240 + 15 * pulse)
            fill_col = ARGB(255, r_boost, 68, 68)          # #EF4444 -> #FF5555
            text_col = ARGB(255, 255, 115, 115)          # Bright Coral Red
        else:
            fill_col = ARGB(255, 220, 38, 38)            # Deep Crimson #DC2626
            text_col = ARGB(255, 185, 28, 28)            # Deep Ruby #B91C1C

    # 2. WARNING ALERT (20% <= Quota < 50%) -> VIVID AMBER / GOLD
    elif pct < 50:
        if is_dark:
            fill_col = ARGB(255, 251, 191, 36)           # Amber 400 #FBBF24
            text_col = ARGB(255, 253, 224, 71)           # Bright Gold #FDE047
        else:
            fill_col = ARGB(255, 217, 119, 6)            # Amber 600 #D97706
            text_col = ARGB(255, 180, 83, 9)             # Deep Amber 700 #B45309

    # 3. HEALTHY / PLENTIFUL (Quota >= 50%) -> VIBRANT EMERALD / CYAN
    else:
        if is_dark:
            if theme == 'orbit' and orbit_green == 'blue':
                fill_col = ARGB(255, 56, 189, 248)       # Electric Cyan #38BDF8
                text_col = ARGB(255, 125, 211, 252)      # Sky 300
            else:
                fill_col = ARGB(255, 52, 211, 153)       # Emerald 400 #34D399
                text_col = ARGB(255, 110, 231, 183)      # Mint Green #6EE7B7
        else:
            if theme == 'orbit' and orbit_green == 'blue':
                fill_col = ARGB(255, 2, 132, 199)        # Sky 600
                text_col = ARGB(255, 3, 105, 161)        # Sky 700
            else:
                fill_col = ARGB(255, 5, 150, 105)        # Emerald 600 #059669
                text_col = ARGB(255, 4, 120, 87)         # Emerald 700 #047857

    return fill_col, text_col


def get_model_colors(model_tag, is_dark):
    """Return dedicated branded colors for Gemini (G) and Claude (C)."""
    if str(model_tag).upper().startswith('G'):
        if is_dark:
            return {
                'badge_bg': ARGB(45, 56, 189, 248),
                'badge_text': ARGB(255, 125, 211, 252),
                'accent': ARGB(255, 56, 189, 248),
                'halo': ARGB(80, 56, 189, 248)
            }
        else:
            return {
                'badge_bg': ARGB(40, 2, 132, 199),
                'badge_text': ARGB(255, 3, 105, 161),
                'accent': ARGB(255, 2, 132, 199),
                'halo': ARGB(60, 2, 132, 199)
            }
    else:  # Claude / 3p
        if is_dark:
            return {
                'badge_bg': ARGB(45, 249, 115, 22),
                'badge_text': ARGB(255, 253, 186, 116),
                'accent': ARGB(255, 251, 146, 60),
                'halo': ARGB(80, 249, 115, 22)
            }
        else:
            return {
                'badge_bg': ARGB(40, 194, 65, 12),
                'badge_text': ARGB(255, 154, 52, 18),
                'accent': ARGB(255, 194, 65, 12),
                'halo': ARGB(60, 194, 65, 12)
            }


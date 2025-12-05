# themes.py
import platform
os_name = platform.platform()

# Fonts
if os_name.startswith("Windows"):
    title_font   = ("DejaVu Sans", 18, "bold")
    heading_font = ("DejaVu Sans", 16, "bold")
    body_font    = ("DejaVu Sans", 14)
    mono_font    = ("DejaVu Sans Mono", 10)
elif os_name.startswith("Linux"):
    title_font   = ("Ubuntu", 18, "bold")
    heading_font = ("Ubuntu", 26, "bold")
    body_font    = ("Ubuntu", 14)
    mono_font    = ("Ubuntu Mono", 10)
else:  # macOS or anything else
    title_font   = ("Helvetica Neue", 18, "bold")
    heading_font = ("Helvetica Neue", 16, "bold")
    body_font    = ("Helvetica Neue", 14)
    mono_font    = ("SF Mono", 11)

# Cosmic Sky Colors
sand = "#F5F5DC"       # Sandy beige
sky = "#87CEEB"        # Sky blue
teal = "#4682B4"       # Cool teal
seafoam = "#98FB98"    # Light green
deepsea = "#2F4F4F"    # Deep teal
moonmist = "#E6E6FA"   # Ethereal glow
twilight = "#483D8B"   # Cosmic dust

# Pastel Green Colors
mint = "#ADE9B0"       # Mint Sheen
charcoal = "#121212"   # Charcoal Night
frost = "#E0E0E0"      # Pearl Frost
clementine = "#DD732C" # Clementine Glow
coral = "#FF6F61"      # Coral Blush
crimson = "#D32F2F"    # Crimson Alert
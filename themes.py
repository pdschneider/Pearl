# themes.py
import platform
os_name = platform.platform()

# Fonts
if os_name == "Windows":
    title_font   = ("DejaVu Sans", 12, "bold")
    heading_font = ("DejaVu Sans", 11, "bold")
    body_font    = ("DejaVu Sans", 10)
    mono_font    = ("DejaVu Sans Mono", 10)
elif os_name == "Linux":
    title_font   = ("Ubuntu", 12, "bold")
    heading_font = ("Ubuntu", 11, "bold")
    body_font    = ("Ubuntu", 10)
    mono_font    = ("Ubuntu Mono", 10)
else:  # macOS or anything else
    title_font   = ("Helvetica Neue", 15, "bold")
    heading_font = ("Helvetica Neue", 13, "bold")
    body_font    = ("Helvetica Neue", 11)
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

# GUI styles
styles = {
    # Cosmic Sky Theme
    "cosmic_sky": {
        "TFrame": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "padding": 5,
            }
        },
        "TLabel": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font
            }
        },
        "TButton": {
            "configure": {
                "background": teal,
                "foreground": "white",
                "font": body_font,
                "padding": (10, 5),
                "relief": "raised",
                "focuscolor": "red",
                "bordercolor": "darkblue",
                "lightcolor": "lightblue",
                "darkcolor": "darkblue"
            }
        },
        "TSendbutton.TButton": {
            "configure": {
                "background": teal,
                "foreground": "white",
                "font": body_font,
                "padding": (10, 5),
                "relief": "raised",
                "width": 2,
                "focuscolor": "red",
                "bordercolor": "darkblue",
                "lightcolor": "lightblue",
                "darkcolor": "darkblue"
            }
        },
        "TEntry": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        },
        "TCheckbutton": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        },
        "TRadiobutton": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        },
        "TTreeview": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        },
        "TCombobox": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        },
        "TNotebook.Tab": {
            "configure": {
                "background": sky,
                "foreground": deepsea,
                "font": title_font,
                "bordercolor": sky
            }
        }
    },

    # Pastel Green Theme
    "pastel_green": {
        "TFrame": {
            "configure": {
                "background": mint,
                "foreground": frost,
                "font": title_font,
                "padding": 5,
            }
        },
        "TLabel": {
            "configure": {
                "background": mint,
                "foreground": charcoal,
                "font": title_font
                }
            },
        "TButton": {
            "configure": {
                "background": clementine,
                "foreground": "white",
                "font": body_font,
                "padding": (10, 5),
                "relief": "raised",
                "focuscolor": clementine,
                "bordercolor": clementine,
                "lightcolor": clementine,
                "darkcolor": clementine
                }
            },
        "TSendbutton": {
            "configure": {
                "background": clementine,
                "foreground": "white",
                "font": body_font,
                "padding": (10, 5),
                "relief": "raised",
                "width": 1,
                "focuscolor": clementine,
                "bordercolor": clementine,
                "lightcolor": clementine,
                "darkcolor": clementine
                }
        },
        "TEntry": {
            "configure": {
                "background": mint,
                "foreground": charcoal,
                "font": title_font,
                "bordercolor": mint
                }
        },
        "TCheckbutton": {
            "configure": {
                "background": mint,
                "foreground": frost,
                "font": title_font,
                "bordercolor": mint
                }
            },
        "TRadiobutton": {
            "configure": {
                "background": mint,
                "foreground": charcoal,
                "font": title_font,
                "bordercolor": mint
                }
            },
        "TTreeview": {
            "configure": {
                "background": mint,
                "foreground": frost,
                "font": title_font,
                "bordercolor": mint
                }
            },
        "TCombobox": {
            "configure": {
                "background": mint,
                "foreground": frost,
                "font": title_font,
                "bordercolor": mint
                }
            },
        "TNotebook.Tab": {
            "configure": {
                "background": mint,
                "foreground": charcoal,
                "font": title_font,
                "bordercolor": mint
            }
        }
    }
}
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont


def _apply_base_fonts(root: tk.Misc) -> None:
    """Set pleasant, consistent default fonts across platforms."""
    families = [
        "TkDefaultFont",
        "TkTextFont",
        "TkMenuFont",
        "TkHeadingFont",
        "TkFixedFont",
        "TkIconFont",
        "TkTooltipFont",
    ]
    for name in families:
        try:
            f = tkfont.nametofont(name)
            # Prefer Segoe UI on Windows; fallback gracefully elsewhere
            family = "Segoe UI"
            try:
                # If family isn't available, Tk falls back automatically
                f.configure(family=family)
            except Exception:
                pass
            # Comfortable base size
            if name == "TkHeadingFont":
                f.configure(size=11, weight="bold")
            else:
                f.configure(size=10)
        except Exception:
            # Ignore if a platform doesn't have a particular named font
            pass


def apply_theme(root: tk.Misc, mode: str = "light") -> ttk.Style:
    """Apply a light or dark theme with sane defaults.

    Returns the ttk.Style instance so callers may tweak further if needed.
    """
    _apply_base_fonts(root)
    style = ttk.Style(root)

    # Choose a solid base theme present on most systems
    base = "vista" if "vista" in style.theme_names() else "clam"
    try:
        style.theme_use(base)
    except Exception:
        pass

    if mode == "dark":
        bg = "#1e1e1e"
        bg2 = "#252526"
        fg = "#e0e0e0"
        accent = "#2d7dff"
        select = "#094771"
        border = "#3c3c3c"
    else:
        bg = "#f5f6fa"
        bg2 = "#ffffff"
        fg = "#1f2328"
        accent = "#2d7dff"
        select = "#cfe8ff"
        border = "#e5e7eb"

    # Broad defaults (ttk respects per-style overrides later)
    try:
        style.configure(".", background=bg, foreground=fg)
    except Exception:
        pass

    # Containers and text
    style.configure("TFrame", background=bg)
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TSeparator", background=border)

    # Notebook
    style.configure("TNotebook", background=bg, borderwidth=0, tabmargins=(6, 4, 6, 0))
    style.configure("TNotebook.Tab", padding=(12, 6), background=bg2, foreground=fg)
    style.map(
        "TNotebook.Tab",
        background=[("selected", bg2)],
        foreground=[("selected", fg)],
    )

    # Buttons and inputs
    style.configure("TButton", padding=(10, 6))
    style.configure("TEntry", fieldbackground=bg2)
    style.configure("TCombobox", fieldbackground=bg2)
    style.configure("TCheckbutton", background=bg, foreground=fg)
    style.configure("TRadiobutton", background=bg, foreground=fg)

    # Trees
    style.configure(
        "Treeview",
        background=bg2,
        fieldbackground=bg2,
        foreground=fg,
        rowheight=26,
        bordercolor=border,
        lightcolor=border,
        darkcolor=border,
    )
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.map("Treeview", background=[("selected", select)], foreground=[("selected", fg)])

    # Progress
    style.configure("Horizontal.TProgressbar", background=accent, troughcolor=bg2)

    return style


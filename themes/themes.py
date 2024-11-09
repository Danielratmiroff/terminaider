from rich.theme import Theme, Style

rosewater = "pink1"          # ANSI Code 218
flamingo = "pink3"           # ANSI Code 175
pink = "orchid"               # ANSI Code 170
mauve = "medium_orchid"       # ANSI Code 134
red = "magenta1"              # ANSI Code 201
maroon = "rosy_brown"         # ANSI Code 138
peach = "light_salmon3"       # ANSI Code 173
yellow = "yellow3"            # ANSI Code 184
green = "light_green"         # ANSI Code 120
teal = "cyan3"                # ANSI Code 43
sky = "sky_blue1"             # ANSI Code 117
sapphire = "light_sky_blue1"  # ANSI Code 153
blue = "sky_blue1"            # ANSI Code 117
lavender = "medium_purple1"   # ANSI Code 141
text = "bright_white"         # ANSI Code 15
subtext1 = "light_slate_blue"  # ANSI Code 105
subtext0 = "slate_blue3"      # ANSI Code 62
overlay2 = "grey53"           # ANSI Code 102
overlay1 = "purple4"          # ANSI Code 55
overlay0 = "dark_blue"        # ANSI Code 18
surface2 = "dark_blue"        # ANSI Code 18
surface1 = "dark_slate_gray3"  # ANSI Code 116
surface0 = "dark_slate_gray1"  # ANSI Code 123
base = "black"                # ANSI Code 0
mantle = "dark_slate_gray1"   # ANSI Code 123
crust = "dark_slate_gray1"    # ANSI Code 123

CATPUCCINO_MOCCA = Theme({
    # Headings
    "markdown.h1": f"bold {rosewater}",
    "markdown.h2": f"bold {flamingo}",
    "markdown.h3": f"bold {pink}",
    "markdown.h4": f"bold {pink} dim",
    "markdown.h5": f"underline {flamingo}",
    "markdown.h6": f"italic {mauve}",
    "markdown.h7": f"italic {mauve} dim",  # Optional

    # Text Styles
    "markdown.bold": f"bold {yellow}",
    "markdown.italic": f"{mauve}",
    "markdown.em": f"{mauve} italic",
    "markdown.emph": f"{mauve} italic",  # For commonmark backwards compatibility
    "markdown.strong": f"bold {yellow}",
    "markdown.paragraph": f"{text}",

    # Links
    "markdown.link": f"underline {sapphire}",
    "markdown.link_url": f"{sapphire}",

    # Code
    # "markdown.code": Style(bold=False, color=text, bgcolor=crust),
    "markdown.code": f"{text}",
    # "markdown.code_block": Style(bold=False, color=text, bgcolor=surface0),
    "markdown.code_block": f"{text}",

    # Blockquotes
    "markdown.block_quote": f"{overlay1}",
    "markdown.quote": f"{overlay1}",

    # Lists
    "markdown.list": f"{teal}",
    "markdown.item": f"{text}",
    "markdown.item.bullet": f"bold {yellow}",
    "markdown.item.number": f"bold {yellow}",

    # Horizontal Rules
    "markdown.hr": f"{yellow}",

    # Borders (Optional)
    "markdown.h1.border": f"{rosewater}",

    # Inline Elements
    "markdown.inline": f"{subtext1}",

    # Tables
    "markdown.table": f"{teal}",
    "markdown.table.header": f"{peach}",

    # Regular Text
    "text": f"{text}",
})

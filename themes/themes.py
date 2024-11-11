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
subtext1 = "grey11"  # ANSI Code 105
subtext0 = "grey19"      # ANSI Code 62
overlay2 = "grey27"           # ANSI Code 102
overlay1 = "grey35"          # ANSI Code 55
overlay0 = "grey39"        # ANSI Code 18
surface2 = "grey46"        # ANSI Code 18
surface1 = "grey54"  # ANSI Code 116
surface0 = "grey62"  # ANSI Code 123
base = "grey70"                # ANSI Code 0
mantle = "grey85"   # ANSI Code 123
crust = "grey93"    # ANSI Code 123

CATPUCCINO_MOCCA = Theme({
    # Headings
    "markdown.h1": Style(bold=True, color=rosewater),
    "markdown.h2": Style(bold=True, color=flamingo),
    "markdown.h3": Style(bold=True, color=pink),
    "markdown.h4": Style(bold=True, color=pink, dim=True),
    "markdown.h5": Style(underline=True, color=flamingo),
    "markdown.h6": Style(italic=True, color=mauve),
    "markdown.h7": Style(italic=True, color=mauve, dim=True),  # Optional

    # Text Styles
    "markdown.bold": Style(bold=True, color=yellow),
    "markdown.italic": Style(color=mauve),
    "markdown.em": Style(italic=True, color=mauve),
    "markdown.emph": Style(italic=True, color=mauve),  # For commonmark backwards compatibility
    "markdown.strong": Style(bold=True, color=yellow),
    "markdown.paragraph": Style(color=text),

    # Links
    "markdown.link": Style(underline=True, color=sapphire),
    "markdown.link_url": Style(color=sapphire),

    # Code
    "code": Style(color=text),
    "markdown.code": Style(color=text),
    "markdown.code_block": Style(color=text),

    # Blockquotes
    "markdown.block_quote": Style(color=rosewater),
    "markdown.quote": Style(color=rosewater),

    # Lists
    "markdown.list": Style(color=text),
    "markdown.item": Style(color=text),
    "markdown.item.bullet": Style(bold=True, color=text),
    "markdown.item.number": Style(bold=True, color=text),

    # Horizontal Rules
    "markdown.hr": Style(color=peach),

    # Borders (Optional)
    "markdown.h1.border": Style(color=rosewater),

    # Inline Elements
    "markdown.inline": Style(color=subtext1),

    # Tables
    "markdown.table": Style(color=teal),
    "markdown.table.header": Style(color=peach),

    # Regular Text
    "text": Style(color=text),
})

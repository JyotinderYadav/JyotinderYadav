from pathlib import Path

from PIL import Image


INPUT_FILE = Path("source-prepped.png")
OUTPUT_FILE = Path("jyotinder-ascii.svg")


# ASCII characters from light to dark
RAMP = " .`:-=+*cs#%@"

# Size of the ASCII portrait
COLS = 100
ROWS = 53

# Character dimensions
CHAR_WIDTH = 7
CHAR_HEIGHT = 10

# SVG dimensions
WIDTH = COLS * CHAR_WIDTH
HEIGHT = ROWS * CHAR_HEIGHT


def brightness_to_char(brightness):
    """
    Convert brightness (0-255) to an ASCII character.
    Bright pixels -> sparse characters
    Dark pixels -> dense characters
    """

    index = int(
        (255 - brightness)
        / 255
        * (len(RAMP) - 1)
    )

    return RAMP[index]


def main():

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {INPUT_FILE}"
        )

    print("Loading prepared image...")

    image = Image.open(INPUT_FILE).convert("L")

    print(f"Original image size: {image.size}")

    # Resize to ASCII grid
    image = image.resize(
        (COLS, ROWS)
    )

    pixels = image.load()

    svg = []

    # SVG header
    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">

<style>

.ascii-row {{
    opacity: 0;
    animation: reveal 0.45s ease-out forwards;
}}

@keyframes reveal {{
    from {{
        opacity: 0;
        transform: translateX(-20px);
    }}

    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

</style>

<rect
    width="100%"
    height="100%"
    fill="#0d1117"
/>
'''
    )

    # Generate ASCII rows
    for row in range(ROWS):

        delay = row * 0.045

        svg.append(
            f'''
<g
    class="ascii-row"
    style="animation-delay:{delay:.3f}s"
>
'''
        )

        for col in range(COLS):

            brightness = pixels[col, row]

            char = brightness_to_char(
                brightness
            )

            # Skip spaces to keep SVG smaller
            if char == " ":
                continue

            x = col * CHAR_WIDTH
            y = row * CHAR_HEIGHT

            # Escape special XML characters
            if char == "<":
                char = "&lt;"
            elif char == ">":
                char = "&gt;"
            elif char == "&":
                char = "&amp;"

            svg.append(
                f'''
<text
    x="{x}"
    y="{y + CHAR_HEIGHT}"
    fill="#c9d1d9"
    font-family="monospace"
    font-size="9"
>
    {char}
</text>
'''
            )

        svg.append("</g>")

    svg.append("</svg>")

    OUTPUT_FILE.write_text(
        "".join(svg),
        encoding="utf-8"
    )

    print()
    print("Done!")
    print(f"Created: {OUTPUT_FILE}")
    print(f"Grid: {COLS} x {ROWS}")
    print(f"SVG size: {WIDTH} x {HEIGHT}")


if __name__ == "__main__":
    main()
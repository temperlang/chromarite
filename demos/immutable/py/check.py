"""Tries to change Chromarite's values from Python; see ../../README.md."""

from chromarite import Color, HueMethod, Space

color = Color.from_list_with_alpha(Space.srgb, [0.25, 0.5, 0.75, 0.5])

color.space = Space.oklch  # attempt: color-field
setattr(color, "space", Space.oklch)  # attempt: color-setattr
Space.srgb.name = "changed"  # attempt: space-field
Space.srgb = Space.oklch  # attempt: space-static
HueMethod.shorter = HueMethod.longer  # attempt: hue-static
color.to_list()[0] = 1.0  # attempt: channel-list
color.alpha[0] = 1.0  # attempt: alpha-list

same = (
    color.space.name == "srgb"
    and color.get(0, 0) == 0.25
    and color.alpha_at(0) == 0.5
    and Space.srgb.name == "srgb"
    and HueMethod.shorter.name == "shorter"
)
print("same" if same else "changed")

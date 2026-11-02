-- Tries to change Chromarite's values from Lua; see ../../README.md.

-- The libraries `temper build` generates at the repo's top, from this folder.
package.path = "../../../temper.out/lua/?/init.lua;../../../temper.out/lua/?.lua;" .. package.path

local chromarite = require("chromarite")
local Color, HueMethod, Space = chromarite.Color, chromarite.HueMethod, chromarite.Space

local color = Color.fromListWithAlpha(Space.srgb, { 0.25, 0.5, 0.75, 0.5 })

color.space = Space.oklch -- attempt: color-field
for k, v in pairs(color) do if v == Space.srgb then color[k] = Space.oklch end end -- attempt: pairs-field
Space.srgb.name = "changed" -- attempt: space-field
Space.srgb = Space.oklch -- attempt: space-static
HueMethod.shorter = HueMethod.longer -- attempt: hue-static
color:toList()[1] = 1.0 -- attempt: channel-list
color.alpha[1] = 1.0 -- attempt: alpha-list

local same = color.space.name == "srgb"
  and color:get(0, 0) == 0.25
  and color:alphaAt(0) == 0.5
  and Space.srgb.name == "srgb"
  and HueMethod.shorter.name == "shorter"
print(same and "same" or "changed")

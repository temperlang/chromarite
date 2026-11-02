// Tries to change Chromarite's values from JavaScript; see ../../README.md.

import { Color, HueMethod, Space } from "chromarite";

const color = Color.fromListWithAlpha(Space.srgb, [0.25, 0.5, 0.75, 0.5]);

color.space = Space.oklch; // attempt: color-field
Reflect.set(color, "space", Space.oklch); // attempt: color-setattr
Object.defineProperty(color, "space", { value: Space.oklch }); // attempt: color-define
Space.srgb.name = "changed"; // attempt: space-field
Space.srgb = Space.oklch; // attempt: space-static
HueMethod.shorter = HueMethod.longer; // attempt: hue-static
color.toList()[0] = 1.0; // attempt: channel-list
color.alpha[0] = 1.0; // attempt: alpha-list

const same =
  color.space.name === "srgb" &&
  color.get(0, 0) === 0.25 &&
  color.alphaAt(0) === 0.5 &&
  Space.srgb.name === "srgb" &&
  HueMethod.shorter.name === "shorter";
console.log(same ? "same" : "changed");

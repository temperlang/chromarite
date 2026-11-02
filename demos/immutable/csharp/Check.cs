// Tries to change Chromarite's values from C#; see ../../README.md.

using System;
using System.Collections.Generic;
using Chromarite;

var color = Color.FromListWithAlpha(Space.Srgb, new List<double> { 0.25, 0.5, 0.75, 0.5 });

color.Space = Space.Oklch; // attempt: color-field
Space.Srgb.Name = "changed"; // attempt: space-field
Space.Srgb = Space.Oklch; // attempt: space-static
HueMethod.Shorter = HueMethod.Longer; // attempt: hue-static
color.ToList()[0] = 1.0; // attempt: channel-list
((IList<double>) color.ToList())[0] = 1.0; // attempt: channel-cast
color.Alpha![0] = 1.0; // attempt: alpha-list

bool same = color.Space.Name == "srgb"
    && color.Get(0, 0) == 0.25
    && color.AlphaAt(0) == 0.5
    && Space.Srgb.Name == "srgb"
    && HueMethod.Shorter.Name == "shorter";
Console.WriteLine(same ? "same" : "changed");

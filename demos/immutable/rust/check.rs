//! Tries to change Chromarite's values from Rust; see ../../README.md.

#![allow(unused_mut)]

use chromarite::{Color, HueMethod, Space};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut color = Color::from_list_with_alpha(Space::srgb(), vec![0.25, 0.5, 0.75, 0.5]);

    color.space = Space::oklch(); // attempt: color-field
    Space::srgb().name = "changed".into(); // attempt: space-field
    Space::srgb = Space::oklch; // attempt: space-static
    HueMethod::shorter = HueMethod::longer; // attempt: hue-static
    color.to_list()[0] = 1.0; // attempt: channel-list
    color.alpha().unwrap()[0] = 1.0; // attempt: alpha-list

    let same = *color.space().name() == "srgb"
        && color.get(0, 0)? == 0.25
        && color.alpha_at(0)? == 0.5
        && *Space::srgb().name() == "srgb"
        && *HueMethod::shorter().name() == "shorter";
    println!("{}", if same { "same" } else { "changed" });
    Ok(())
}

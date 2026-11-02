// Tries to change Chromarite's values from C++; see ../../README.md.

#include <iostream>
#include <memory>
#include <vector>

#include "chromarite/init.hpp"

using chromarite::Color;
using chromarite::HueMethod;
using chromarite::Space;

int main() {
  auto color = Color::fromListWithAlpha(
      Space::srgb(), std::make_shared<std::vector<double>>(std::vector<double>{0.25, 0.5, 0.75, 0.5}));

  color->space = Space::oklch();  // attempt: color-field
  Space::srgb()->name = "changed";  // attempt: space-field
  Space::srgb() = Space::oklch();  // attempt: space-static
  HueMethod::shorter() = HueMethod::longer();  // attempt: hue-static
  (*color->toList())[0] = 1.0;  // attempt: channel-list
  (*color->get_alpha())[0] = 1.0;  // attempt: alpha-list

  bool same = color->get_space()->get_name() == "srgb"
      && color->get(0, 0) == 0.25
      && color->alphaAt(0) == 0.5
      && Space::srgb()->get_name() == "srgb"
      && HueMethod::shorter()->get_name() == "shorter";
  std::cout << (same ? "same" : "changed") << std::endl;
}

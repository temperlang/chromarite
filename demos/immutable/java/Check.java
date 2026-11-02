// Tries to change Chromarite's values from Java; see ../../README.md.

import chromarite.Color;
import chromarite.HueMethod;
import chromarite.Space;
import java.util.List;

public class Check {
    public static void main(String[] args) throws Exception {
        Color color = Color.fromListWithAlpha(Space.srgb, List.of(0.25, 0.5, 0.75, 0.5));

        color.space = Space.oklch; // attempt: color-field
        Space.srgb.name = "changed"; // attempt: space-field
        Space.srgb = Space.oklch; // attempt: space-static
        HueMethod.shorter = HueMethod.longer; // attempt: hue-static
        color.toList().set(0, 1.0); // attempt: channel-list
        color.getAlpha().set(0, 1.0); // attempt: alpha-list

        boolean same = color.getSpace().getName().equals("srgb")
            && color.get(0, 0) == 0.25
            && color.alphaAt(0) == 0.5
            && Space.srgb.getName().equals("srgb")
            && HueMethod.shorter.getName().equals("shorter");
        System.out.println(same ? "same" : "changed");
    }
}

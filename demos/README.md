# Demos

## Tour

`tour/` walks through Chromarite's whole public API in each supported
language: making and parsing colors, converting between spaces, formatting,
gamut mapping, mixing, adjusting, contrast, and channels as flat lists. Every
version prints the same text, `tour/expected.txt`, so the tours double as a
cross-language test.

First build the libraries from the repo's top, with
[Temper](https://temperlang.dev/):

    temper build -b cpp -b csharp -b java -b js -b lua -b py -b rust

Each tour uses the generated library in `temper.out/` by relative path. Run
one from its directory:

| Language | In `tour/…` | Commands |
|---|---|---|
| C++ | `cpp` | `cmake -B build && cmake --build build && ./build/tour` |
| C# | `csharp` | `dotnet run` |
| Java | `java` | `./gradlew run` |
| JS | `js` | `npm ci && npm start` |
| Lua | `lua` | `lua -l paths tour.lua` |
| Python | `py` | `uv run tour.py` |
| Rust | `rust` | `cargo run` |

Or run them all and compare each with `expected.txt`:

    uv run demos/run.py [LANGUAGE ...]

Java's Gradle build compiles the generated sources along with the tour,
because the generated Maven projects expect a JDK 8 toolchain and release
signing.

### Snippets for the site

Lines ending in a comment like `# snippet: snap, edges` are also short
snippets in the site's dev mode, which shows the code behind each part of
the page. Each snippet is its marked lines, in order, and must exist in
every tour; `site/build.py` collects them and fails if one is missing. Keep
marked lines plain statements, like `fitted = vivid.fit_chroma(Space.srgb)`,
so they read well on their own.

## Immutability

Chromarite's colors, spaces, and hue methods can't be changed once made, but
that's up to each language's translation. `immutable/` checks it from each
language, with one small program per language that tries changes the
natural way: setting a field or property, reassigning a static like
`Space.srgb`, writing to a list a getter returned, and, where the language
allows, reflection, such as `setattr` in Python, `Object.defineProperty` in
JavaScript, or `pairs` in Lua.

Each change is a line ending in a comment like `// attempt: space-static`.
For every attempt, the runner builds and runs the program with just that
line. In C++, C#, Java, and Rust, most should fail to compile. Elsewhere,
they should throw, or leave the value as it was:

    uv run demos/immutable/run.py [LANGUAGE ...]

It uses the same toolchains as the tour, against the same `temper.out/`, and
compares what happened with `immutable/expected.txt`. A few changes
currently go through, marked `changed` there with the reason. Each is
waiting on a fix in Temper's translation, after which its line flips to
`refused`. Any other change that goes through fails the check.

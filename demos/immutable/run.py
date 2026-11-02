# /// script
# requires-python = ">=3.11"
# ///
"""Checks that Chromarite's values can't be changed from each language.

Usage, from anywhere in the repo, after building the libraries:

    temper build -b cpp -b csharp -b java -b js -b lua -b py -b rust
    uv run demos/immutable/run.py [LANGUAGE ...]

Each `demos/immutable/<language>/` has one check program. Lines ending in a
comment like `// attempt: space-static` each try one change, in that
language's natural way. For each attempt, this writes the program with only
that attempt's lines to `build/`, then builds and runs it. The attempt was
refused if the build fails, the program fails, or it prints `same`, and the
value changed if it prints `changed`. The program must print `same` with no
attempt lines at all, so a broken check can't pass as a refusal.

Results must match `expected.txt`. Exits non-zero on any difference.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Per language: the check program, commands run once first, commands that
# build each attempt, and the command that runs it, all in its directory.
LANGUAGES = {
    "cpp": (
        "check.cpp",
        [],
        [["cmake", "-B", "build", "-DCMAKE_BUILD_TYPE=Release"], ["cmake", "--build", "build", "-j", "2"]],
        ["./build/check"],
    ),
    "csharp": (
        "Check.cs",
        [],
        [["dotnet", "build", "-v", "q", "--nologo"]],
        ["dotnet", "run", "--no-build"],
    ),
    # Plain javac, so each attempt takes a second rather than a Gradle run.
    "java": (
        "Check.java",
        [["sh", "-c", "javac -nowarn -d build/classes $(find ../../../temper.out/java/*/src/main -name '*.java')"]],
        [["javac", "-cp", "build/classes", "-d", "build/classes", "build/Check.java"]],
        ["java", "-cp", "build/classes", "Check"],
    ),
    "js": (
        "check.js",
        # Copies the generated library afresh, rather than linking to it.
        [["npm", "ci", "--install-links", "--silent", "--no-audit", "--no-fund"]],
        [],
        ["node", "build/check.js"],
    ),
    "lua": ("check.lua", [], [], ["lua", "build/check.lua"]),
    "py": ("check.py", [], [], ["uv", "run", "-q", "build/check.py"]),
    "rust": ("check.rs", [], [["cargo", "build", "-q"]], ["./target/debug/check"]),
}

ATTEMPT = re.compile(r"(?://|--|#)\s*attempt:\s*([\w-]+)\s*$")


def run(args, dir):
    """Runs a command, returning (ok, output)."""
    result = subprocess.run(args, cwd=dir, capture_output=True, text=True)
    return result.returncode == 0, result.stdout + result.stderr


def first_error(output):
    """The first line that looks like an error, for a short reason."""
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    for line in lines:
        if match := re.search(r"\S*(error|exception)\S*.*", line, re.IGNORECASE):
            return match[0][:100]
    return lines[-1][:100] if lines else ""


def check(language):
    """Tries each attempt in one language, returning {attempt: (result, why)}."""
    source_name, setup, build, command = LANGUAGES[language]
    dir = HERE / language
    source = (dir / source_name).read_text().splitlines(keepends=True)
    attempts = list(dict.fromkeys(m[1] for line in source if (m := ATTEMPT.search(line))))
    (dir / "build").mkdir(exist_ok=True)
    for args in setup:
        ok, output = run(args, dir)
        if not ok:
            raise RuntimeError(f"{' '.join(args)} failed:\n{output}")
    results = {}
    for attempt in [None, *attempts]:
        kept = [line for line in source if (m := ATTEMPT.search(line)) is None or m[1] == attempt]
        (dir / "build" / source_name).write_text("".join(kept))
        result = None
        for args in build:
            ok, output = run(args, dir)
            if not ok:
                result = ("refused", "build: " + first_error(output))
                break
        if result is None:
            ok, output = run(command, dir)
            printed = output.strip().splitlines()[-1:] if ok else []
            if not ok:
                result = ("refused", "run: " + first_error(output))
            elif printed == ["changed"]:
                result = ("changed", "")
            elif printed == ["same"]:
                result = ("refused", "ignored")
            else:
                raise RuntimeError(f"{attempt}: unexpected output:\n{output}")
        if attempt is None:
            if result != ("refused", "ignored"):
                raise RuntimeError(f"without attempts, the check must print same, but: {result[1]}")
        else:
            results[attempt] = result
    return results


def read_expected():
    """Reads expected.txt as {(language, attempt): result}."""
    expected = {}
    for line in (HERE / "expected.txt").read_text().splitlines():
        fields = line.split("#", 1)[0].split()
        if fields:
            language, attempt, result = fields
            expected[language, attempt] = result
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("languages", nargs="*", metavar="LANGUAGE", help=", ".join(LANGUAGES))
    languages = parser.parse_args().languages or list(LANGUAGES)
    unknown = set(languages) - set(LANGUAGES)
    if unknown:
        parser.error(f"unknown: {', '.join(sorted(unknown))}")
    expected = read_expected()
    failed = []
    for language in languages:
        try:
            results = check(language)
        except (RuntimeError, OSError) as error:
            print(f"{language}: error\n{error}")
            failed.append(language)
            continue
        wanted = {attempt: result for (lang, attempt), result in expected.items() if lang == language}
        for attempt in sorted(set(results) | set(wanted)):
            result, why = results.get(attempt, ("missing", ""))
            want = wanted.get(attempt, "missing")
            mark = "ok" if result == want else f"FAIL, expected {want}"
            print(f"{language:7} {attempt:14} {result:8} {mark:24} {why}".rstrip())
            if result != want and language not in failed:
                failed.append(language)
    if failed:
        print(f"Failed: {' '.join(failed)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

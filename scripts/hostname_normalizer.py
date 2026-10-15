#!/usr/bin/env python3
"""
Normalizes host-list entries so DNS consumers can match them.

Upstream lists occasionally carry entries no consumer can match: a leading
dot (`.example.com`) or an internationalized name in UTF-8 (queries arrive as
punycode). Such entries get the leading dots stripped and the name converted
to punycode with Python's `idna` codec; entries that still are not a
hostname afterwards are dropped, and so are names with a character the
IDNA 2003 codec would map to a different domain than browsers look up.
Every other line is left untouched.
"""

import ipaddress
import re
from typing import Optional

HOSTNAME_RE = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-]*")
ADBLOCK_RE = re.compile(r"^(\s*\|\|)([^\^\s]*)(.*)$", re.DOTALL)
HOSTS_RE = re.compile(r"^(\s*\S+\s+)(\S+)(.*)$", re.DOTALL)
BARE_RE = re.compile(r"^(\s*)(\S+)(.*)$", re.DOTALL)
# ASCII characters a candidate host may hold; anything else (`@`, `|`, `:`,
# `/`, ...) marks a rule or metadata that is left for the format gate.
# IDNA 2003 maps these away (`straße.de` -> `strasse.de`), while IDNA 2008
# and browsers keep them, so converting would block an unrelated domain.
DEVIATIONS = set("\u00df\u03c2\u200c\u200d")
HOST_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")


def is_address(token: str) -> bool:
    try:
        ipaddress.ip_address(token.split("%", 1)[0])
        return True
    except ValueError:
        return False


def normalize_host(host: str) -> Optional[str]:
    """Returns the host as a matchable hostname, or None if it cannot be one."""
    host = host.lstrip(".")
    if not host.isascii():
        if DEVIATIONS & set(host.lower()):
            return None
        try:
            host = host.encode("idna").decode("ascii")
        except UnicodeError:
            return None
    return host if HOSTNAME_RE.fullmatch(host) else None


def normalize_line(line: str) -> Optional[str]:
    """Returns the line, rewritten if its host needed it, or None to drop it."""
    stripped = line.strip()
    if not stripped or stripped[0] in "#!;[/":
        return line

    tokens = stripped.split()
    if stripped.startswith("||"):
        match = ADBLOCK_RE.match(line)
    elif len(tokens) == 1 or tokens[1].startswith("#"):
        match = BARE_RE.match(line)
    elif is_address(tokens[0]):
        match = HOSTS_RE.match(line)
    else:
        return line

    head, host, tail = match.groups()
    wildcard = "*." if host.startswith("*.") else ""
    name = host[len(wildcard):]
    if not name.startswith(".") and name.isascii():
        return line
    if any(c.isascii() and c not in HOST_CHARS for c in name):
        return line

    normalized = normalize_host(name)
    if normalized is None:
        return None
    return f"{head}{wildcard}{normalized}{tail}"


def normalize_file(path: str) -> tuple[int, int]:
    """Normalizes a host-list file in place. Returns (rewritten, dropped)."""
    with open(path, "r", encoding="utf-8", errors="surrogateescape", newline="") as f:
        lines = f.readlines()

    rewritten = dropped = 0
    out = []
    for line in lines:
        normalized = normalize_line(line)
        if normalized is None:
            dropped += 1
            continue
        if normalized != line:
            rewritten += 1
        out.append(normalized)

    if rewritten or dropped:
        with open(path, "w", encoding="utf-8", errors="surrogateescape", newline="") as f:
            f.writelines(out)
    return rewritten, dropped


if __name__ == "__main__":
    import os
    import tempfile
    import unittest

    class TestNormalizeLine(unittest.TestCase):
        def test_valid_lines_are_untouched(self):
            for line in (
                "example.com\n",
                "0.0.0.0 example.com\n",
                "127.0.0.1\tads.example.com # tracker\n",
                "||example.com^\n",
                "*.example.com\n",
                "# comment with ünïcode\n",
                "! Title: list\n",
                "[Adblock Plus]\n",
                "\n",
                "::1 localhost\n",
                "// comment with ünïcode\n",
                "Title: schöne Liste\n",
                "Feed: straße.de\n",
                "dead bücher.de\n",
                "@@||bücher.de^\n",
                ".example.com/path\n",
            ):
                self.assertEqual(normalize_line(line), line)

        def test_leading_dots_are_stripped(self):
            self.assertEqual(normalize_line(".betway.ug\n"), "betway.ug\n")
            self.assertEqual(normalize_line("..betway.ug\n"), "betway.ug\n")
            self.assertEqual(normalize_line("0.0.0.0 .betway.ug\n"), "0.0.0.0 betway.ug\n")
            self.assertEqual(normalize_line("fe80::1%lo0 .betway.ug\n"), "fe80::1%lo0 betway.ug\n")
            self.assertEqual(normalize_line("||.betway.ug^\n"), "||betway.ug^\n")
            self.assertEqual(normalize_line("*..betway.ug\n"), "*.betway.ug\n")

        def test_idn_becomes_punycode(self):
            self.assertEqual(
                normalize_line("najboljšionlinecasinos.si\n"),
                "xn--najboljionlinecasinos-wbe.si\n",
            )
            self.assertEqual(
                normalize_line("0.0.0.0 bücher.de\r\n"),
                "0.0.0.0 xn--bcher-kva.de\r\n",
            )
            self.assertEqual(normalize_line("||bücher.de^\n"), "||xn--bcher-kva.de^\n")
            self.assertEqual(normalize_line(".bücher.de"), "xn--bcher-kva.de")
            self.assertEqual(normalize_line("BÜCHER.de.\n"), "xn--bcher-kva.de.\n")
            self.assertEqual(normalize_line("||bücher.de\n"), "||xn--bcher-kva.de\n")

        def test_idn_with_deviation_characters_is_dropped(self):
            self.assertIsNone(normalize_line("straße.de\n"))
            self.assertIsNone(normalize_line("0.0.0.0 STRAẞE.de\n"))
            self.assertIsNone(normalize_line("ελληνικός.gr\n"))

        def test_unusable_entries_are_dropped(self):
            self.assertIsNone(normalize_line(".\n"))
            self.assertIsNone(normalize_line("0.0.0.0 ..\n"))
            self.assertIsNone(normalize_line("bad..ü.de\n"))
            self.assertIsNone(normalize_line("a" * 64 + "ü.de\n"))

    class TestNormalizeFile(unittest.TestCase):
        def test_rewrites_in_place(self):
            content = "# header\n.betway.ug\nnajboljšionlinecasinos.si\nexample.com\n.\n"
            with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as f:
                f.write(content)
            try:
                self.assertEqual(normalize_file(f.name), (2, 1))
                with open(f.name, encoding="utf-8") as f2:
                    self.assertEqual(
                        f2.read(),
                        "# header\nbetway.ug\nxn--najboljionlinecasinos-wbe.si\nexample.com\n",
                    )
            finally:
                os.unlink(f.name)

        def test_invalid_utf8_entry_is_dropped(self):
            with tempfile.NamedTemporaryFile("wb", delete=False) as f:
                f.write(b"example.com\nb\xfccher.de\n")
            try:
                self.assertEqual(normalize_file(f.name), (0, 1))
                with open(f.name, "rb") as f2:
                    self.assertEqual(f2.read(), b"example.com\n")
            finally:
                os.unlink(f.name)

    unittest.main()

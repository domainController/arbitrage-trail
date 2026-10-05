import io
import json
import os
import tempfile
import unittest
import zipfile
from pathlib import Path

from arbitrage_trail import markdown
from arbitrage_trail.cli import main
from arbitrage_trail.export import to_zip, write_dir
from arbitrage_trail.loader import load_bytes, load_path

FIX = Path(__file__).parent / "fixtures"


class TestMarkdown(unittest.TestCase):
    def setUp(self):
        self.conv = load_path(str(FIX / "claude_conversations.json"))[0]

    def test_frontmatter_is_valid_and_first(self):
        md = markdown.render(self.conv)
        self.assertTrue(md.startswith("---\n"))
        head = md.split("---\n")[1]
        fields = dict(line.split(": ", 1) for line in head.strip().splitlines())
        # Les valeurs sont du JSON, donc du YAML valide.
        self.assertEqual(json.loads(fields["title"]), "Régime borné / non borné")
        self.assertEqual(json.loads(fields["messages"]), 3)
        self.assertEqual(fields["tags"], "[arbitrage-trail, claude]")

    def test_body(self):
        md = markdown.render(self.conv)
        self.assertIn("# Régime borné / non borné", md)
        self.assertIn("## Utilisateur · 2026-10-03 18:00 UTC", md)
        self.assertIn("## Assistant (Claude)", md)
        self.assertIn("Pièces jointes : `fondation.md`", md)
        self.assertIn("> [!warning] Export incomplet", md)

    def test_filename_is_deterministic_and_safe(self):
        name = markdown.filename(self.conv)
        self.assertEqual(name, "2026-10-03_claude_regime-borne-non-borne_c0ffee00.md")
        self.assertEqual(name, markdown.filename(self.conv))

    def test_slugify_edge_cases(self):
        self.assertEqual(markdown.slugify("   "), "sans-titre")
        self.assertEqual(markdown.slugify("../../etc/passwd"), "etc-passwd")


class TestExport(unittest.TestCase):
    def test_write_dir_is_idempotent(self):
        convs = load_path(str(FIX / "chatgpt_conversations.json"))
        with tempfile.TemporaryDirectory() as d:
            first = write_dir(convs, d)
            second = write_dir(convs, d)
            self.assertEqual(first, second)
            self.assertEqual(len(os.listdir(d)), 2)
            self.assertFalse([f for f in os.listdir(d) if f.endswith(".tmp")])

    def test_zip_roundtrip(self):
        convs = load_path(str(FIX / "chatgpt_conversations.json"))
        with zipfile.ZipFile(io.BytesIO(to_zip(convs))) as zf:
            self.assertEqual(len(zf.namelist()), 2)

    def test_load_from_export_zip(self):
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w") as zf:
            zf.writestr("export/conversations.json", (FIX / "claude_conversations.json").read_bytes())
            zf.writestr("export/users.json", "[]")
        convs = load_bytes(buf.getvalue())
        self.assertEqual(convs[0].source, "claude")


class TestCli(unittest.TestCase):
    def test_convert_with_match(self):
        with tempfile.TemporaryDirectory() as d:
            code = main(["convert", str(FIX / "chatgpt_conversations.json"), "-o", d, "--match", "stack"])
            self.assertEqual(code, 0)
            self.assertEqual(len(os.listdir(d)), 1)

    def test_bad_file(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
            fh.write("pas du json")
        try:
            self.assertEqual(main(["list", fh.name]), 2)
        finally:
            os.unlink(fh.name)


if __name__ == "__main__":
    unittest.main()

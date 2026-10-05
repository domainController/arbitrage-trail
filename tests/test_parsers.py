import json
import unittest
from pathlib import Path

from arbitrage_trail.parsers import UnknownFormat, chatgpt, claude, detect

FIX = Path(__file__).parent / "fixtures"


def load(name):
    return json.loads((FIX / name).read_text(encoding="utf-8"))


class TestDetect(unittest.TestCase):
    def test_detects_both_platforms(self):
        self.assertEqual(detect(load("chatgpt_conversations.json")), "chatgpt")
        self.assertEqual(detect(load("claude_conversations.json")), "claude")

    def test_rejects_unknown(self):
        with self.assertRaises(UnknownFormat):
            detect([{"foo": 1}])
        with self.assertRaises(UnknownFormat):
            detect("texte")


class TestChatGPT(unittest.TestCase):
    def setUp(self):
        self.convs = chatgpt.parse(load("chatgpt_conversations.json"))
        self.main = self.convs[0]

    def test_follows_displayed_branch_only(self):
        texts = [m.text for m in self.main.messages]
        self.assertIn("Version retenue : le schéma est cohérent.", texts)
        self.assertNotIn("Première version (régénérée ensuite).", texts)

    def test_warns_about_ignored_branches(self):
        self.assertTrue(any("bifurcation" in w for w in self.main.warnings))

    def test_skips_hidden_system_message(self):
        self.assertEqual([m.role for m in self.main.messages], ["user", "assistant", "user", "assistant", "assistant"])

    def test_renders_code_and_images(self):
        self.assertIn("```python\nprint('hello')\n```", self.main.messages[3].text)
        self.assertIn("[image jointe]", self.main.messages[2].text)
        self.assertEqual(self.main.messages[2].attachments, ["schema.png"])

    def test_metadata(self):
        self.assertEqual(self.main.id, "6a1f0c2e-1111-4a2b-9c3d-aaaaaaaaaaaa")
        self.assertEqual(self.main.created.year, 2025)

    def test_without_current_node_and_unknown_type(self):
        other = self.convs[1]
        self.assertEqual(other.id, "7b2e1d3f-2222-4b3c-8d4e-bbbbbbbbbbbb")
        self.assertEqual(len(other.messages), 2)
        self.assertIn("tether_browsing_display", other.messages[1].text)
        self.assertTrue(any("tether_browsing_display" in w for w in other.warnings))


class TestClaude(unittest.TestCase):
    def setUp(self):
        self.convs = claude.parse(load("claude_conversations.json"))
        self.main = self.convs[0]

    def test_roles_and_order(self):
        self.assertEqual([m.role for m in self.main.messages], ["user", "assistant", "user"])

    def test_content_blocks(self):
        text = self.main.messages[1].text
        self.assertIn("## Oui et non", text)
        self.assertIn("> [!note]- Raisonnement", text)
        self.assertIn("appel d'outil : web_search", text)
        self.assertTrue(any("mystery_block" in w for w in self.main.warnings))

    def test_text_fallback_and_attachments(self):
        self.assertEqual(self.main.messages[2].text, "Merci.")
        self.assertEqual(self.main.messages[0].attachments, ["fondation.md"])

    def test_empty_title_and_conversation(self):
        empty = self.convs[1]
        self.assertEqual(empty.title, "Sans titre")
        self.assertEqual(empty.messages, [])


if __name__ == "__main__":
    unittest.main()

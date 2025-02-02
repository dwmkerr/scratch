import unittest
from flow import format_heading, format_line_item, format_section, Section, LineItem

class TestFlowFormatter(unittest.TestCase):
    def test_format_heading(self):
        self.assertEqual(format_heading("Global"), "\033[1;34mGlobal\033[0m")

    def test_format_line_item(self):
        item = LineItem("⌘ + Enter", "Toggle iTerm fullscreen", True)
        self.assertEqual(format_line_item(item), "  \033[1;32;1m⌘ + Enter\033[0m: Toggle iTerm fullscreen")

    def test_format_section(self):
        section = Section("Test Section")
        section.add_item("Ctrl + P", "fzf search", True)
        section.hidden_count = 2
        expected_output = (
            "\033[1;34mTest Section\033[0m\n"
            "  \033[1;32;1mCtrl + P\033[0m: fzf search\n"
            "  \033[1;36m+2 hidden\033[0m"
        )
        self.assertEqual(format_section(section), expected_output)

if __name__ == "__main__":
    unittest.main()


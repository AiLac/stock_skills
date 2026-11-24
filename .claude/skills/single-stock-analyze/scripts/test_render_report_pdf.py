"""Regression checks for Markdown-to-PDF export and optional charts."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from render_report_pdf import render, report_html


def sample_report():
    sections = [f"## Section {index}\n\nSection text {index}." for index in range(1, 14)]
    sections[1] += "\n\n| Factor | Score (0-5) |\n|---|---:|\n| Growth | 4 |\n| Moat | 3 |"
    sections[2] += "\n\n| Segment | % of revenue |\n|---|---:|\n| A | 60% |\n| B | 40% |"
    # Long prose before the final chart should flow across ordinary page breaks.
    sections[4] += "\n\n" + "\n\n".join(f"Evidence note {n}. " * 4 for n in range(45))
    sections[5] += "\n\n| Expense | % of revenue |\n|---|---:|\n| Labour | 30% |\n| Rent | 5% |"
    return "# Report\n\n> Preface\n\n# Body title\n\n" + "\n\n".join(sections)


@unittest.skipUnless(shutil.which("pandoc"), "requires Pandoc")
class ReportPdfTests(unittest.TestCase):
    def test_incomplete_series_retains_table_and_omits_its_chart(self):
        report = sample_report().replace("| B | 40% |", "| B | undisclosed |")
        html = report_html(report, "pandoc", "en")
        self.assertIn("undisclosed", html)
        self.assertNotIn("Share of consolidated revenue</figcaption>", html)
        self.assertIn("Factor ratings (0–5)</figcaption>", html)
        self.assertIn("Operating costs and expenses as a share of revenue</figcaption>", html)
        self.assertIn("Preface", html)
        self.assertIn("Body title", html)
        for section in range(1, 14):
            self.assertIn(f'href="#s{section:02}"', html)
            self.assertIn(f'id="s{section:02}"', html)

    def test_missing_section_preserves_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "report.md", Path(tmp) / "report.pdf"
            source.write_text(sample_report().split("## Section 13")[0], encoding="utf-8")
            output.write_bytes(b"existing copy")
            with self.assertRaisesRegex(ValueError, "13.*12"):
                render(source, output, "pandoc", "weasyprint", "en")
            self.assertEqual(output.read_bytes(), b"existing copy")

    @unittest.skipUnless(shutil.which("weasyprint") and shutil.which("pdftotext"),
                         "requires WeasyPrint and pdftotext")
    def test_multipage_pdf_preserves_figures_and_final_section(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp) / "Example report.md", Path(tmp) / "Example report.pdf"
            source.write_text(sample_report(), encoding="utf-8")
            render(source, output, "pandoc", "weasyprint", "en")
            text = subprocess.check_output(["pdftotext", str(output), "-"], encoding="utf-8")
            pages = [" ".join(p.split()) for p in text.split("\f") if p.strip()]
            self.assertIn("Section text 13.", pages[-1])
            score_page = next(i for i, p in enumerate(pages) if "Factor ratings" in p)
            expense_page = next(i for i, p in enumerate(pages) if "Operating costs and expenses" in p)
            self.assertLess(score_page, expense_page)
            self.assertIn("Share of consolidated revenue", " ".join(pages))


if __name__ == "__main__":
    unittest.main()

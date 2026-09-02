#!/usr/bin/env python3
"""Generate the copyright-free PDF fixture used by prepare_paper tests."""

from __future__ import annotations

from io import BytesIO
from pathlib import Path
import struct
import zlib

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas


WIDTH, HEIGHT = letter
DOI = "10.12345/paper-to-paradigm.synthetic-fixture"


def png_chunk(kind: bytes, payload: bytes) -> bytes:
    return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", zlib.crc32(kind + payload) & 0xFFFFFFFF)


def synthetic_chart_png(width: int = 480, height: int = 180) -> bytes:
    """Build a deterministic RGB bar-chart PNG using only the standard library."""
    background = (247, 249, 252)
    blue = (50, 103, 174)
    orange = (226, 122, 63)
    axis = (45, 55, 72)
    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            color = background
            if (55 <= x <= 430 and 135 <= y <= 138) or (55 <= x <= 58 and 25 <= y <= 138):
                color = axis
            if 115 <= x <= 205 and 65 <= y <= 134:
                color = blue
            if 275 <= x <= 365 and 40 <= y <= 134:
                color = orange
            row.extend(color)
        rows.append(bytes(row))
    raw = b"".join(rows)
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + png_chunk(b"IHDR", header) + png_chunk(b"IDAT", zlib.compress(raw, 9)) + png_chunk(b"IEND", b"")


def draw_footer(pdf: canvas.Canvas, page_number: int) -> None:
    pdf.setFont("Helvetica", 8)
    pdf.setFillColor(colors.HexColor("#5A6472"))
    pdf.drawCentredString(WIDTH / 2, 28, f"Synthetic fixture - PDF page {page_number}")


def draw_heading(pdf: canvas.Canvas, text: str, y: float, size: int = 15) -> float:
    pdf.setFillColor(colors.HexColor("#173B57"))
    pdf.setFont("Helvetica-Bold", size)
    pdf.drawString(54, y, text)
    return y - size - 8


def draw_lines(pdf: canvas.Canvas, lines: list[str], y: float, leading: int = 15) -> float:
    pdf.setFillColor(colors.HexColor("#202A34"))
    pdf.setFont("Helvetica", 10)
    for line in lines:
        pdf.drawString(54, y, line)
        y -= leading
    return y


def build_pdf(output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=letter, invariant=1, pageCompression=1)
    pdf.setTitle("Synthetic Behavioral Study for PDF Grounding Tests")
    pdf.setAuthor("paper-to-paradigm test generator")
    pdf.setSubject("Copyright-free synthetic fixture with no human participant data")

    pdf.setFillColor(colors.HexColor("#173B57"))
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(54, 730, "Synthetic Behavioral Study for PDF Grounding Tests")
    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(colors.HexColor("#5A6472"))
    pdf.drawString(54, 708, "Programmatically generated fixture - no human participants or copyrighted source material")
    y = draw_heading(pdf, "Abstract", 670)
    y = draw_lines(
        pdf,
        [
            "This synthetic paper tests page, section, figure, table, DOI, and material-link extraction.",
            "All values, labels, and graphics are generated solely for automated software testing.",
        ],
        y,
    )
    y = draw_heading(pdf, "1. Introduction", y - 12)
    y = draw_lines(
        pdf,
        [
            "The fictional task compares two color-coded conditions using generated response-time values.",
            "No claim in this document is intended as scientific evidence or advice.",
            f"Synthetic DOI: {DOI}",
            "Supplement: https://example.org/synthetic-supplement.pdf",
            "Code: https://example.org/synthetic-code",
        ],
        y,
    )
    draw_footer(pdf, 1)
    pdf.showPage()

    y = draw_heading(pdf, "2. Methods", 730)
    y = draw_heading(pdf, "2.1 Participants", y - 4, size=12)
    y = draw_lines(pdf, ["No participants were recruited. The fixture contains synthetic labels only."], y)
    y = draw_heading(pdf, "2.2 Procedure", y - 8, size=12)
    y = draw_lines(
        pdf,
        [
            "A generated timeline contains instruction, practice, and formal phases.",
            "Condition A and Condition B are balanced in a deterministic synthetic schedule.",
        ],
        y,
    )
    y = draw_heading(pdf, "Figure 1. Synthetic response pattern", y - 8, size=11)
    chart = ImageReader(BytesIO(synthetic_chart_png()))
    pdf.drawImage(chart, 84, y - 170, width=420, height=157.5, preserveAspectRatio=True, mask="auto")
    pdf.setFont("Helvetica", 9)
    pdf.setFillColor(colors.HexColor("#384452"))
    pdf.drawString(112, y - 184, "Condition A")
    pdf.drawString(282, y - 184, "Condition B")
    draw_footer(pdf, 2)
    pdf.showPage()

    y = draw_heading(pdf, "3. Results", 730)
    y = draw_lines(
        pdf,
        [
            "Generated values are included only to exercise extraction and locator logic.",
            "The synthetic difference must not be interpreted as an empirical effect.",
        ],
        y,
    )
    y = draw_heading(pdf, "Table 1. Synthetic condition summary", y - 10, size=11)
    table_y = y - 8
    pdf.setStrokeColor(colors.HexColor("#8B97A6"))
    pdf.setFillColor(colors.HexColor("#EAF0F5"))
    pdf.rect(54, table_y - 22, 450, 22, fill=1, stroke=1)
    pdf.setFillColor(colors.HexColor("#202A34"))
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(66, table_y - 15, "Condition")
    pdf.drawString(210, table_y - 15, "Synthetic mean")
    pdf.drawString(360, table_y - 15, "Synthetic N")
    pdf.setFont("Helvetica", 9)
    for row, values in enumerate((("A", "510 ms", "40"), ("B", "475 ms", "40")), start=1):
        row_y = table_y - 22 - row * 22
        pdf.rect(54, row_y, 450, 22, fill=0, stroke=1)
        pdf.drawString(66, row_y + 7, values[0])
        pdf.drawString(210, row_y + 7, values[1])
        pdf.drawString(360, row_y + 7, values[2])
    y = table_y - 88
    y = draw_heading(pdf, "4. Discussion", y, size=15)
    y = draw_lines(
        pdf,
        [
            "This fixture demonstrates a source-grounded layout without reproducing any published paper.",
            "Expected use is limited to automated and visual testing of prepare_paper.py.",
        ],
        y,
    )
    y = draw_heading(pdf, "Appendix", y - 12, size=15)
    draw_lines(pdf, ["The appendix intentionally occupies the same PDF as the synthetic main text."], y)
    draw_footer(pdf, 3)
    pdf.save()


def build_proceedings_pdf(output: Path) -> None:
    """Build a two-paper proceedings fixture for article-boundary tests."""
    output.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(output), pagesize=letter, invariant=1, pageCompression=1)
    pdf.setTitle("Synthetic Two-Paper Proceedings")
    pdf.setAuthor("paper-to-paradigm test generator")

    def first_page(title: str, doi: str, paper_number: int) -> None:
        pdf.setFillColor(colors.HexColor("#173B57"))
        pdf.setFont("Helvetica-Bold", 19)
        pdf.drawString(54, 730, title)
        pdf.setFont("Helvetica", 10)
        pdf.drawString(54, 706, f"Synthetic Author {paper_number}")
        y = draw_heading(pdf, "Abstract", 670)
        y = draw_lines(pdf, ["A generated abstract for deterministic proceedings indexing.", f"DOI: {doi}"], y)
        y = draw_heading(pdf, "1. Introduction", y - 10)
        draw_lines(pdf, ["A synthetic theoretical rationale with no scientific claims."], y)

    first_page("First Synthetic Proceedings Paper", "10.12345/synthetic.proceedings.1", 1)
    draw_footer(pdf, 1)
    pdf.showPage()
    y = draw_heading(pdf, "2. Methods", 730)
    y = draw_lines(pdf, ["The design uses generated labels and no participants."], y)
    y = draw_heading(pdf, "3. Results", y - 12)
    y = draw_lines(pdf, ["All values are synthetic."], y)
    y = draw_heading(pdf, "4. Discussion", y - 12)
    draw_lines(pdf, ["The paper exists only to test indexing."], y)
    draw_footer(pdf, 2)
    pdf.showPage()

    first_page("Second Synthetic Proceedings Paper", "10.12345/synthetic.proceedings.2", 2)
    draw_footer(pdf, 3)
    pdf.showPage()
    y = draw_heading(pdf, "2. Research Design", 730)
    y = draw_lines(pdf, ["The design is another generated fixture."], y)
    y = draw_heading(pdf, "3. Data Analysis", y - 12)
    y = draw_lines(pdf, ["No inferential claim is made."], y)
    y = draw_heading(pdf, "4. Conclusions", y - 12)
    draw_lines(pdf, ["The second paper closes the synthetic collection."], y)
    draw_footer(pdf, 4)
    pdf.showPage()
    y = draw_heading(pdf, "Author Index", 730)
    draw_lines(pdf, ["Synthetic Author 1", "Synthetic Author 2"], y)
    draw_footer(pdf, 5)
    pdf.save()


if __name__ == "__main__":
    build_pdf(Path(__file__).with_name("synthetic_paper.pdf"))

"""Render paper.en.md as a readable PDF using the bundled ReportLab runtime.

The Markdown manuscript is the source of the PDF. This script handles the small
subset of Markdown used by that file; it is not a general Markdown renderer.
"""

from __future__ import annotations

import html
import re
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


HERE = Path(__file__).resolve().parent
SOURCE = HERE / "paper.en.md"
OUTPUT = HERE / "schur-radius33-note.pdf"
INK = colors.HexColor("#183042")
ACCENT = colors.HexColor("#176689")
GRAY = colors.HexColor("#5b6570")


def setup_fonts() -> None:
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("ArialPack", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("ArialPackBold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("ArialPackItalic", str(fonts / "ariali.ttf")))
    pdfmetrics.registerFontFamily(
        "ArialPack", normal="ArialPack", bold="ArialPackBold", italic="ArialPackItalic"
    )


def inline(text: str) -> str:
    value = html.escape(text)
    value = re.sub(r"`([^`]+)`", r'<font name="ArialPackBold">\1</font>', value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", value)
    return value.replace("  \n", "<br/>").replace("\n", " ")


def make_styles() -> dict[str, ParagraphStyle]:
    return {
        "title": ParagraphStyle(
            "TitlePack", fontName="ArialPackBold", fontSize=17.5,
            leading=21.5, textColor=INK, spaceAfter=11, alignment=TA_LEFT,
        ),
        "byline": ParagraphStyle(
            "BylinePack", fontName="ArialPack", fontSize=9.2, leading=13,
            textColor=GRAY, spaceAfter=12,
        ),
        "heading": ParagraphStyle(
            "HeadingPack", fontName="ArialPackBold", fontSize=11.2,
            leading=14, textColor=ACCENT, spaceBefore=13, spaceAfter=6,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "BodyPack", fontName="ArialPack", fontSize=9.15, leading=13.25,
            textColor=INK, spaceAfter=8, splitLongWords=True,
        ),
        "tablehead": ParagraphStyle(
            "TableHeadPack", fontName="ArialPackBold", fontSize=8.2,
            leading=11, textColor=colors.white,
        ),
        "table": ParagraphStyle(
            "TablePack", fontName="ArialPack", fontSize=8.2,
            leading=11, textColor=INK,
        ),
        "code": ParagraphStyle(
            "CodePack", fontName="Courier", fontSize=8.5,
            leading=11.5, textColor=INK,
        ),
    }


def page_frame(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    canvas.setStrokeColor(colors.HexColor("#cbd8de"))
    canvas.setLineWidth(0.5)
    canvas.line(22 * mm, height - 18 * mm, width - 22 * mm, height - 18 * mm)
    canvas.setFont("ArialPack", 8)
    canvas.setFillColor(GRAY)
    canvas.drawString(22 * mm, height - 16 * mm, "Beedbyte  |  Schur number six")
    canvas.drawRightString(width - 22 * mm, 16 * mm, str(doc.page))
    canvas.restoreState()


def parse_blocks(source: str) -> list[str]:
    return [block.strip() for block in re.split(r"\n\s*\n", source.strip()) if block.strip()]


def build() -> None:
    setup_fonts()
    styles = make_styles()
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=23 * mm, rightMargin=23 * mm,
        topMargin=25 * mm, bottomMargin=23 * mm,
        title="A 34-Recoloring Obstruction Near a Published Six-Color Schur Partition of [1,536]",
        author="Beedbyte (School Scotty)",
    )
    story = []
    for block in parse_blocks(SOURCE.read_text(encoding="utf-8")):
        if block.startswith("# "):
            story.append(Paragraph(inline(block[2:]), styles["title"]))
            story.append(HRFlowable(width="100%", thickness=1.2, color=ACCENT, spaceAfter=8))
        elif block.startswith("## "):
            story.append(Paragraph(inline(block[3:]), styles["heading"]))
        elif block.startswith("|"):
            rows = []
            for number, line in enumerate(block.splitlines()):
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if all(re.fullmatch(r"-+", cell) for cell in cells):
                    continue
                style = styles["tablehead"] if number == 0 else styles["table"]
                rows.append([Paragraph(inline(cell), style) for cell in cells])
            table = Table(rows, colWidths=[39 * mm, 59 * mm, 59 * mm], repeatRows=1, hAlign="LEFT")
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f6f8")]),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, -1), (-1, -1), 0.6, colors.HexColor("#cbd8de")),
            ]))
            story.extend([Spacer(1, 3 * mm), KeepTogether([table]), Spacer(1, 4 * mm)])
        elif block.startswith("```text\n"):
            commands = block.removeprefix("```text\n").removesuffix("\n```")
            story.append(Preformatted(commands, styles["code"]))
            story.append(Spacer(1, 3 * mm))
        elif block.startswith("**Beedbyte"):
            story.append(Paragraph(inline(block), styles["byline"]))
        else:
            story.append(Paragraph(inline(block), styles["body"]))
    doc.build(story, onFirstPage=page_frame, onLaterPages=page_frame)
    print(OUTPUT)


if __name__ == "__main__":
    build()

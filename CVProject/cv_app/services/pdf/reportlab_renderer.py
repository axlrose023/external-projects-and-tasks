from __future__ import annotations
from io import BytesIO
from typing import Any, List, Iterable, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, ListFlowable, ListItem, KeepTogether,
)

from .interfaces import PdfRenderer, CVPdfData


def _on_page(title: str):
    def draw(canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(colors.lightgrey)
        canvas.setLineWidth(0.5)
        canvas.line(22 * mm, height - 28 * mm, width - 22 * mm, height - 28 * mm)
        canvas.line(22 * mm, 18 * mm, width - 22 * mm, 18 * mm)
        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(22 * mm, height - 22 * mm, title)
        canvas.drawRightString(width - 22 * mm, 12 * mm, f"Page {doc.page}")
        canvas.restoreState()
    return draw


class ReportLabRenderer(PdfRenderer):

    def __init__(self) -> None:
        self.styles = self._build_styles()

    def render(self, data: CVPdfData) -> bytes:
        buf = BytesIO()
        doc = BaseDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=22 * mm, rightMargin=22 * mm,
            topMargin=34 * mm, bottomMargin=26 * mm,
            title=f"CV {data.full_name}", author=data.full_name,
        )
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
        doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=_on_page(data.full_name))])

        story: List[Any] = []
        self._title_block(story, data)
        self._skills(story, data.skills)
        self._projects(story, data.projects)
        self._contacts(story, dict(data.contacts))

        doc.build(story)
        pdf = buf.getvalue()
        buf.close()
        return pdf

    def _build_styles(self):
        ss = getSampleStyleSheet()
        return {
            "title": ParagraphStyle(
                "TitleBig", parent=ss["Title"], fontName="Helvetica",
                fontSize=24, leading=28, spaceAfter=6, textColor=colors.HexColor("#111111"),
            ),
            "subtitle": ParagraphStyle(
                "Subtitle", parent=ss["BodyText"], fontName="Helvetica",
                fontSize=11, leading=15, textColor=colors.HexColor("#555555"), spaceAfter=4,
            ),
            "section": ParagraphStyle(
                "Section", parent=ss["Heading2"], fontName="Helvetica-Bold",
                fontSize=13, leading=16, spaceBefore=14, spaceAfter=8,
                textColor=colors.HexColor("#111111"),
            ),
            "body": ParagraphStyle(
                "Body", parent=ss["BodyText"], fontName="Helvetica",
                fontSize=11, leading=15, textColor=colors.HexColor("#222222"), spaceAfter=6,
            ),
            "small": ParagraphStyle(
                "Small", parent=ss["BodyText"], fontName="Helvetica",
                fontSize=9.5, leading=13, textColor=colors.HexColor("#666666"),
            ),
        }

    def _divider(self, top: float = 6, bottom: float = 6):
        tbl = Table([[""]], colWidths=["*"], rowHeights=[2])
        tbl.setStyle(TableStyle([
            ("LINEABOVE", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e2e2")),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return [Spacer(1, top), tbl, Spacer(1, bottom)]

    def _title_block(self, story: List[Any], data: CVPdfData):
        s = self.styles
        story.append(Paragraph(data.full_name, s["title"]))
        if data.bio:
            story.append(Paragraph(data.bio, s["subtitle"]))
        story.extend(self._divider(8, 10))

    def _skills(self, story: List[Any], skills: Iterable[str]):
        skills = [str(x) for x in (skills or []) if x]
        if not skills:
            return
        s = self.styles
        story.append(Paragraph("Skills", s["section"]))
        bullets = [ListItem(Paragraph(x, s["body"]), leftIndent=8) for x in skills]
        story.append(ListFlowable(bullets, bulletType="bullet", bulletChar="•"))

    def _projects(self, story: List[Any], projects):
        projects = list(projects or [])
        if not projects:
            return
        s = self.styles
        story.append(Paragraph("Projects", s["section"]))
        data: List[List[Any]] = []
        for p in projects:
            name = (p.name or "Project").strip()
            year = f" — {p.year}" if p.year else ""
            head = Paragraph(f"<b>{name}</b>{year}", s["body"])
            desc = Paragraph(p.description or "", s["small"]) if p.description else Paragraph("", s["small"])
            data.append([head, desc])
        table = Table(
            data, colWidths=[70 * mm, None],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]),
        )
        story.append(KeepTogether(table))

    def _contacts(self, story: List[Any], contacts: Dict[str, Any]):
        if not contacts:
            return
        s = self.styles
        story.append(Paragraph("Contacts", s["section"]))
        rows: List[List[Any]] = []
        for k, v in contacts.items():
            key = Paragraph(f"<b>{str(k).capitalize()}:</b>", s["body"])
            val = Paragraph(str(v), s["body"])
            rows.append([key, val])
        table = Table(
            rows, colWidths=[35 * mm, None],
            style=TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]),
        )
        story.append(table)

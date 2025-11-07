from __future__ import annotations
from typing import List
from cv_app.models import CV
from .interfaces import CVPdfData, ProjectDTO, PdfRenderer, get_renderer


class CVPdfService:

    def __init__(self, renderer: PdfRenderer | None = None) -> None:
        self.renderer = renderer or get_renderer()

    def build_for_pk(self, pk: int) -> bytes:
        cv = self._qs().get(pk=pk)
        data = self._to_dto(cv)
        return self.renderer.render(data)

    def _qs(self):
        return CV.objects.only(
            "id", "firstname", "lastname", "bio", "skills", "projects", "contacts"
        )

    def _to_dto(self, cv: CV) -> CVPdfData:
        projects: List[ProjectDTO] = []
        for p in (cv.projects or []):
            p = p or {}
            projects.append(
                ProjectDTO(
                    name=(p.get("name") or "Project"),
                    year=str(p.get("year")) if p.get("year") else None,
                    description=p.get("description"),
                )
            )
        return CVPdfData(
            id=cv.id,
            firstname=cv.firstname or "",
            lastname=cv.lastname or "",
            bio=cv.bio or "",
            skills=[str(s) for s in (cv.skills or []) if s],
            projects=projects,
            contacts=dict(cv.contacts or {}),
        )

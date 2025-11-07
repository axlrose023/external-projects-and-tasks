from cv_app.models import CV

def build_translation_prompt(cv: CV, target_language: str) -> str:
    parts: list[str] = []
    parts.append(f"Name: {cv.firstname} {cv.lastname}")
    if cv.bio:
        parts.append(f"Bio: {cv.bio}")
    if cv.skills:
        parts.append("Skills: " + ", ".join(cv.skills))
    if cv.projects:
        proj_lines = []
        for p in cv.projects:
            name = p.get("name", "Project")
            year = f" ({p['year']})" if p.get("year") else ""
            desc = p.get("description", "")
            line = f"- {name}{year}"
            if desc:
                line += f": {desc}"
            proj_lines.append(line)
        parts.append("Projects:\n" + "\n".join(proj_lines))
    if cv.contacts:
        contact_lines = [f"{k}: {v}" for k, v in cv.contacts.items()]
        parts.append("Contacts:\n" + "\n".join(contact_lines))

    raw = "\n\n".join(parts)
    return (
        f"Please translate the following CV content into {target_language}:\n\n"
        f"{raw}"
    )

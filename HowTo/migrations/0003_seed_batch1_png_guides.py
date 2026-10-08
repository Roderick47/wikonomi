"""Seed five PNG community guides from their reviewed Markdown source files.

Only new titles are inserted; existing community guides are not overwritten.
"""
import re
from pathlib import Path
from django.conf import settings
from django.db import migrations

FILENAMES = (
    "register-company-ipa-png.md",
    "transfer-vehicle-ownership-png.md",
    "file-monthly-swt-png.md",
    "register-for-gst-irc-png.md",
    "open-business-bank-account-png.md",
)

def _plain(markdown):
    markdown = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r"\1 — \2", markdown)
    markdown = re.sub(r"(?m)^\s*-\s*\[\s*\]\s*", "☐ ", markdown)
    markdown = re.sub(r"(?m)^\s*-\s+", "• ", markdown)
    markdown = re.sub(r"\*\*(.*?)\*\*", r"\1", markdown)
    return markdown.strip()

def _extract(markdown):
    chunks = re.split(r"^##\s+(.+?)\s*$", markdown, flags=re.MULTILINE)
    intro = chunks[0].splitlines()
    title = next(line[2:].strip() for line in intro if line.startswith("# "))
    description = "\n".join(
        line.strip() for line in intro if line.strip()
        and not line.startswith(("# ", "> "))
    )
    sections = {chunks[i].strip(): chunks[i+1].strip()
                for i in range(1, len(chunks), 2)}
    mandatory = (
        "Fees, deadlines and important notes",
        "Before you start — checklist",
        "Step-by-step instructions",
        "Common mistakes to avoid",
        "Official and supporting sources",
    )
    missing = [name for name in mandatory if name not in sections]
    if missing:
        raise ValueError(f"{title}: missing sections {missing}")
    steps = [
        (mandatory[0], _plain(sections[mandatory[0]])),
        (mandatory[1], _plain(sections[mandatory[1]])),
    ]
    parts = re.split(
        r"^###\s+Step\s+\d+\.\s+(.+?)\s*$",
        sections[mandatory[2]], flags=re.MULTILINE,
    )
    if len(parts) < 3 or parts[0].strip():
        raise ValueError(f"{title}: no valid numbered process steps")
    steps.extend(
        (parts[i].strip(), _plain(parts[i+1]))
        for i in range(1, len(parts), 2)
    )
    steps.extend([
        (mandatory[3], _plain(sections[mandatory[3]])),
        ("Official sources and last-checked date",
         _plain(sections[mandatory[4]]) +
         "\n\nLast researched: 8 October 2026. Confirm current fees, forms and requirements with the relevant agency before applying."),
    ])
    if not description or any(not body for _, body in steps):
        raise ValueError(f"{title}: empty description or step")
    return title, description, steps

def seed_batch1(apps, schema_editor):
    db = schema_editor.connection.alias
    HowTo = apps.get_model("HowTo", "HowTo")
    Step = apps.get_model("HowTo", "HowToStep")
    History = apps.get_model("HowTo", "HowToHistory")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))
    folder = Path(__file__).resolve().parents[1] / "guide_content" / "batch1"
    parsed = [_extract((folder / name).read_text(encoding="utf-8"))
              for name in FILENAMES]
    # Parse everything before beginning writes. This migration is atomic.
    for title, description, steps in parsed:
        if HowTo.objects.using(db).filter(title=title).exists():
            continue
        author, _ = User.objects.using(db).get_or_create(
            username="wikonomi_guides_editorial",
            defaults={
                "first_name": "Wikonomi",
                "last_name": "Guides",
                "password": "!non-login-editorial-identity",
                "is_active": False,
                "is_staff": False,
                "is_superuser": False,
            },
        )
        guide = HowTo.objects.using(db).create(
            title=title, description=description,
            author_id=author.pk, last_editor_id=author.pk,
            is_official=False, is_public=True,
        )
        for order, (heading, body) in enumerate(steps, 1):
            Step.objects.using(db).create(
                how_to_id=guide.pk, order=order,
                title=heading, content=body,
            )
        History.objects.using(db).create(
            how_to_id=guide.pk, editor_id=author.pk,
            version=1, title=title, description=description,
            change_summary="Initial PNG guide; researched 8 October 2026",
            steps_snapshot=[
                {"order": order, "title": heading, "content": body, "image": None}
                for order, (heading, body) in enumerate(steps, 1)
            ],
        )

class Migration(migrations.Migration):
    dependencies = [
        ("HowTo", "0002_howto_last_editor_howto_version_alter_howto_author_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [migrations.RunPython(seed_batch1, migrations.RunPython.noop)]

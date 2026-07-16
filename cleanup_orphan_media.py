"""
One-time script to delete media files not referenced by any DB record.
Run: python cleanup_orphan_media.py [--dry-run]
"""
import asyncio
import sys
from pathlib import Path
from sqlalchemy import select
from db.session import AsyncSessionLocal
from db.models import City, Excursion, Point

MEDIA_DIR = Path(__file__).parent / "media"
DRY_RUN = "--dry-run" in sys.argv


async def get_referenced_paths() -> set[str]:
    async with AsyncSessionLocal() as session:
        cities = (await session.execute(select(City))).scalars().all()
        excursions = (await session.execute(select(Excursion))).scalars().all()
        points = (await session.execute(select(Point))).scalars().all()

    paths = set()
    for c in cities:
        if c.image: paths.add(c.image)
    for e in excursions:
        if e.image: paths.add(e.image)
        if e.video: paths.add(e.video)
    for p in points:
        if p.image: paths.add(p.image)
        if p.audio: paths.add(p.audio)
        if p.video: paths.add(p.video)
    return paths


async def main():
    referenced = await get_referenced_paths()

    all_files = [f for f in MEDIA_DIR.rglob("*") if f.is_file()]
    orphans = [f for f in all_files if "media/" + "/".join(f.parts[f.parts.index("media")+1:]) not in
               {p.split("media/", 1)[1] for p in referenced}]

    # Rebuild as relative paths matching DB format: "media/subdir/file"
    referenced_rel = referenced  # already stored as "media/images/foo.jpg"
    root = MEDIA_DIR.parent

    deleted = skipped = 0
    for f in all_files:
        rel = str(f.relative_to(root))  # e.g. "media/images/foo.jpg"
        if rel not in referenced_rel:
            if DRY_RUN:
                print(f"[dry-run] would delete: {rel}")
            else:
                f.unlink()
                print(f"deleted: {rel}")
            deleted += 1
        else:
            skipped += 1

    print(f"\n{'[dry-run] ' if DRY_RUN else ''}Done — {deleted} orphan(s) {'found' if DRY_RUN else 'deleted'}, {skipped} in use.")


asyncio.run(main())

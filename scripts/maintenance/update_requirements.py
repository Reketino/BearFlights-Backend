
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
REQUIREMENTS = ROOT / "requirements.txt"
BACKUP = ROOT / "requirements.txt.bak"

PATTERN = re.compile(
    r"^(?P<name>[A-Za-z0-9_.-]+)==(?P<version>[^;\s]+)(?P<suffix>.*)$"
)


def main() -> None:
    if not REQUIREMENTS.exists():
        raise FileNotFoundError(REQUIREMENTS)

    if not BACKUP.exists():
        shutil.copy2(REQUIREMENTS, BACKUP)

    updated_lines = []
    changes = []

    content = REQUIREMENTS.read_text(encoding="utf-16")
    for line in content.splitlines():
        match = PATTERN.match(line.strip())

        if not match:
            updated_lines.append(line)
            continue

        name = match.group("name")
        old_version = match.group("version")

        try:
            installed_version = version(name)
        except PackageNotFoundError:
            updated_lines.append(line)
            continue

        if old_version != installed_version:
            changes.append((name, old_version, installed_version))
            line = (
                f"{name}=={installed_version}"
                f"{match.group('suffix')}"
            )

        updated_lines.append(line)

    if changes:
        REQUIREMENTS.write_text(
            "\n".join(updated_lines) + "\n",
            encoding="utf-8",
        )

    print(f"Oppdaterte {len(changes)} pakkeversjoner:")
    for name, old, new in changes:
        print(f"  {name}: {old} -> {new}")

    print(f"\nSikkerhetskopi: {BACKUP}")


if __name__ == "__main__":
    main()

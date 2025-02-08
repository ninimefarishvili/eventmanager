from pathlib import Path

def generate_migrations_modules(base_dir: Path):

    APPS_DIR = base_dir / "apps"
    MIGRATIONS_DIR = base_dir / "migrations"

    data = {}

    for path in APPS_DIR.iterdir():
        name = path.name

        data[name] = f"migrations.{path.name}"

        (MIGRATIONS_DIR / name).mkdir(exist_ok=True, parents=True)
        (MIGRATIONS_DIR / name / "__init__.py").touch(exist_ok=True)

    return data



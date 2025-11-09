import time
import hashlib
from pathlib import Path

from wire_screenshots import wire


def fingerprint(dir_path: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(dir_path.glob("**/*")):
        if p.is_file():
            h.update(p.name.encode())
            try:
                stat = p.stat()
                h.update(str(int(stat.st_mtime)).encode())
                h.update(str(stat.st_size).encode())
            except Exception:
                # If file disappears mid-scan, skip
                continue
    return h.hexdigest()


def main():
    repo_root = Path(__file__).resolve().parent.parent
    screens_dir = repo_root / "static" / "screenshots"
    screens_dir.mkdir(parents=True, exist_ok=True)

    print("Watching static/screenshots for changes. Press Ctrl+C to stop.")
    last_fp = None
    while True:
        try:
            fp = fingerprint(screens_dir)
            if fp != last_fp:
                wire()
                last_fp = fp
            time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped watching.")
            break


if __name__ == "__main__":
    main()
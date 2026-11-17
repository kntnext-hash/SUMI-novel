"""Archive only the verified manifest entries, excluding runtime test artifacts."""
import argparse
import json
import zipfile
from pathlib import Path
from build_windows_review import digest


def package(build, archive):
    build, archive = build.resolve(), archive.resolve()
    if archive.exists():
        raise ValueError("Archive already exists; choose a new name.")
    manifest_path = build / "build_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = []
    for record in manifest["files"]:
        path = (build / record["path"]).resolve()
        if build not in path.parents:
            raise ValueError("Manifest entry escapes the build directory.")
        if path.stat().st_size != record["bytes"] or digest(path) != record["sha256"]:
            raise ValueError("Build changed after assembly: " + record["path"])
        files.append(path)
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED, compresslevel=6) as output:
        for path in files + [manifest_path]:
            output.write(path, (Path(build.name) / path.relative_to(build)).as_posix())
    with zipfile.ZipFile(archive) as check:
        bad = check.testzip()
        if bad:
            raise ValueError("ZIP verification failed: " + bad)
        if len(check.namelist()) != len(files) + 1:
            raise ValueError("Unexpected ZIP entry count.")
    report = {"archive": archive.name, "bytes": archive.stat().st_size,
              "sha256": digest(archive), "entries": len(files) + 1,
              "crc_verified": True, "status": "REVIEW"}
    archive.with_suffix(".zip.sha256.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("build", type=Path)
    parser.add_argument("archive", type=Path)
    args = parser.parse_args()
    package(args.build, args.archive)

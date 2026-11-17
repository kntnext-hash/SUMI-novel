"""Assemble a fresh Windows review distribution from the bundled runtime."""
import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def build(runtime, project, output):
    runtime, project, output = (p.resolve() for p in (runtime, project, output))
    if output.exists():
        raise ValueError("Output must be a new directory; existing builds are never overwritten.")
    for source in (runtime, project):
        if output == source or source in output.parents or output in source.parents:
            raise ValueError("Output must be separate from the runtime and source project.")
    game = project / "game"
    required = [runtime / "kaononaiharu.exe", runtime / "kaononaiharu.py",
                runtime / "lib", runtime / "renpy", game / "script.rpy",
                game / "movies/opening.webm", game / "fonts/NotoSerifJP-Regular.otf",
                game / "licenses/NotoSerifCJK-OFL.txt"]
    missing = [str(p) for p in required if not p.exists()]
    for name in re.findall(r'=\s*"(images/[^"\n]+)"', (game / "images.rpy").read_text(encoding="utf-8")):
        if not (game / name).is_file():
            missing.append(name)
    if missing:
        raise FileNotFoundError("Required distribution inputs missing: " + repr(missing))
    helper = (game / "guisupport.rpy").read_text(encoding="utf-8")
    if "gui7" in helper or "import generate" in helper:
        raise ValueError("SDK GUI generation code must not be shipped.")

    output.mkdir(parents=True)
    for directory in ("lib", "renpy"):
        shutil.copytree(runtime / directory, output / directory)
    for name in ("kaononaiharu.exe", "kaononaiharu.py"):
        shutil.copy2(runtime / name, output / name)
    ignored_dirs = {"saves", "cache", "tests", "__pycache__"}
    allowed_assets = {"audio", "fonts", "gui", "images", "licenses", "movies", "ui"}
    copied_sources = {}
    for source in sorted(game.rglob("*")):
        if not source.is_file():
            continue
        rel = source.relative_to(game)
        if any(part.startswith(".") or part in ignored_dirs for part in rel.parts):
            continue
        if source.suffix.lower() in {".rpyc", ".bak", ".log", ".tmp"} or source.name.startswith("qa_"):
            continue
        if len(rel.parts) == 1:
            if source.suffix != ".rpy":
                continue
        elif rel.parts[0] not in allowed_assets:
            continue
        destination = output / "game" / rel
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        copied_sources[rel.as_posix()] = digest(source)
        if copied_sources[rel.as_posix()] != digest(destination):
            raise ValueError("Copy hash mismatch: " + str(rel))
    (output / "game/release_settings.rpy").write_text(
        "# Distribution-only settings.\ndefine config.developer = False\n", encoding="utf-8")
    (output / "README_はじめに.txt").write_text(
        "顔のない春 ――きみの色が見えるまで。\n\n"
        "制作中の確認版です。音響などの仕上げ作業を継続しています。\n"
        "kaononaiharu.exe を起動してください。Ren’Py SDKの導入は不要です。\n\n"
        "クリック：文章を進める／OPをスキップ\n"
        "右クリック・Esc：ゲームメニュー\n"
        "本文上のホイール：長い文章を上下に読む\n"
        "セーブ・ロード：ゲームメニューまたは画面下のボタン\n"
        "いずれかのエンディング後、タイトルに「全彩再読」が現れます。\n\n"
        "保存先：%APPDATA%\\RenPy\\kaononaiharu-long-1\n"
        "旧縦切りデモ・旧0.9版とは別の保存先です。\n"
        "フォントの利用条件：game/licenses/NotoSerifCJK-OFL.txt\n"
        "Ren’Pyと関連ソフトウェア：ゲーム内の作品情報をご覧ください。\n",
        encoding="utf-8")
    files = [{"path": p.relative_to(output).as_posix(), "bytes": p.stat().st_size,
              "sha256": digest(p)} for p in sorted(output.rglob("*")) if p.is_file()]
    manifest = {"status": "REVIEW", "game_sources": copied_sources, "files": files}
    (output / "build_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(output), "files": len(files), "bytes": sum(f["bytes"] for f in files)}, ensure_ascii=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--project", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    build(args.runtime, args.project, args.output)

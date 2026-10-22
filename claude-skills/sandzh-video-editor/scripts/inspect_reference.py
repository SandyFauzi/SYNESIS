"""Read-only video / Premiere inspection. Writes only inside --out-dir."""
import argparse
import collections
import gzip
import json
import math
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET


def inspect_project(path):
    result = {"source": str(path), "sequences": [], "media": [], "effects": [],
              "note": "Project inventory; not a flattened final timeline or proof of rendered effects."}
    effects = collections.Counter()
    with path.open("rb") as stream:
        compressed = stream.read(2) == b"\x1f\x8b"
    with (gzip.open if compressed else open)(path, "rb") as stream:
        root, depth = None, 0
        for event, element in ET.iterparse(stream, events=("start", "end")):
            if event == "start":
                depth += 1
                if root is None:
                    root = element
                continue
            if depth == 2:
                if element.tag == "Sequence" and element.get("ObjectUID"):
                    result["sequences"].append({"name": element.findtext("Name"),
                        "preview_width": element.findtext(".//MZ.Sequence.PreviewFrameSizeWidth"),
                        "preview_height": element.findtext(".//MZ.Sequence.PreviewFrameSizeHeight")})
                if element.tag == "Media" and element.get("ObjectUID"):
                    media = element.findtext("ActualMediaFilePath") or element.findtext("FilePath")
                    if media:
                        result["media"].append(media)
                if element.tag.endswith("FilterComponent") and element.get("ObjectID"):
                    component = element.find(".//Component")
                    if component is not None and component.findtext("Intrinsic") != "true":
                        name = component.findtext("DisplayName")
                        if name:
                            effects[(name, component.findtext("Bypass"))] += 1
                root.remove(element)
            depth -= 1
    result["media"] = sorted(set(result["media"]))
    result["effects"] = [{"name": name, "bypass": bypass, "count": count}
                         for (name, bypass), count in effects.most_common()]
    return result


def timestamps(duration, start=0.0, span=None, frames=6):
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError("Video duration must be positive and finite")
    if not math.isfinite(start) or start < 0 or start >= duration:
        raise ValueError("--start must be inside the video")
    if span is not None and (not math.isfinite(span) or span <= 0):
        raise ValueError("--span must be positive and finite")
    if not 1 <= frames <= 48:
        raise ValueError("--frames must be between 1 and 48")
    end = min(duration, start + span) if span is not None else duration
    # Keep the final sample inside the valid range, including very short videos.
    stop = max(start, end - min(0.05, (end - start) / 2))
    if frames == 1:
        return [start]
    return [start + (stop - start) * i / (frames - 1) for i in range(frames)]


def run_json(args):
    run = subprocess.run(args, capture_output=True, timeout=60, check=True)
    return json.loads(run.stdout)


def inspect_video(path, out, start, span, frames):
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg and FFprobe must be available on PATH")
    result = run_json(["ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels",
        "-of", "json", str(path)])
    result["source"] = str(path)
    duration = float(result.get("format", {}).get("duration", 0))
    sample_times = timestamps(duration, start, span, frames)
    result["frames"] = []
    prefix = f"{path.stem}-s{start:g}-span{span if span is not None else 'full'}-n{frames}"
    for index, time in enumerate(sample_times):
        frame = out / f"{prefix}-{index:02d}.jpg"
        # No -y: a repeated run cannot silently overwrite existing output.
        subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin", "-n",
            "-threads", "1", "-ss", f"{time:.6f}", "-i", str(path), "-frames:v", "1",
            "-vf", "scale=960:540:force_original_aspect_ratio=decrease,pad=960:540:(ow-iw)/2:(oh-ih)/2",
            "-threads", "1", "-q:v", "3", str(frame)], capture_output=True, timeout=90, check=True)
        result["frames"].append({"seconds": round(time, 6), "file": str(frame)})
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        result["contact_sheet"] = "Pillow unavailable; inspect the individual frame files."
        return result
    columns = min(3, frames)
    sheet = Image.new("RGB", (columns * 480, math.ceil(frames / columns) * 296), "#141414")
    draw = ImageDraw.Draw(sheet)
    for index, sample in enumerate(result["frames"]):
        with Image.open(sample["file"]) as frame:
            frame = frame.resize((480, 270))
            x, y = index % columns * 480, index // columns * 296
            sheet.paste(frame, (x, y))
            draw.text((x + 6, y + 275), f"{sample['seconds']:.3f} s", fill="white")
    destination = out / f"{prefix}-contact-sheet.jpg"
    if destination.exists():
        raise FileExistsError(destination)
    sheet.save(destination, quality=92)
    result["contact_sheet"] = str(destination)
    return result


def self_test():
    assert timestamps(10, 2, 4, 3) == [2.0, 3.975, 5.95]
    assert len(timestamps(.01, 0, None, 4)) == 4
    for kwargs in ({"duration": 0}, {"duration": 10, "start": 10},
                   {"duration": 10, "frames": 0}, {"duration": 10, "span": -1}):
        try:
            timestamps(**kwargs)
        except ValueError:
            pass
        else:
            raise AssertionError(kwargs)
    xml = b'''<PremiereData><Sequence ObjectURef="s"/>
      <Sequence ObjectUID="s"><Name>Test sequence</Name></Sequence>
      <Media ObjectUID="m"><FilePath>D:\\source.mp4</FilePath></Media>
      <VideoFilterComponent ObjectID="1"><Component><DisplayName>Glow</DisplayName>
      <Intrinsic>false</Intrinsic><Bypass>true</Bypass></Component></VideoFilterComponent>
      <VideoFilterComponent ObjectID="2"><Component><DisplayName>Motion</DisplayName>
      <Intrinsic>true</Intrinsic></Component></VideoFilterComponent></PremiereData>'''
    with tempfile.TemporaryDirectory(prefix="sandzh-skill-check-") as directory:
        for compressed in (False, True):
            path = Path(directory) / f"test-{compressed}.prproj"
            path.write_bytes(gzip.compress(xml) if compressed else xml)
            result = inspect_project(path)
            assert result["sequences"] == [{"name": "Test sequence", "preview_width": None, "preview_height": None}]
            assert result["media"] == ["D:\\source.mp4"]
            assert result["effects"] == [{"name": "Glow", "bypass": "true", "count": 1}]
    print("Self-test passed: compressed/plain projects, references, bypass, and timestamps")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?")
    parser.add_argument("--out-dir")
    parser.add_argument("--start", type=float, default=0)
    parser.add_argument("--span", type=float)
    parser.add_argument("--frames", type=int, default=6)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    if not args.input or not args.out_dir:
        parser.error("input and --out-dir are required")
    path, out = Path(args.input).resolve(strict=True), Path(args.out_dir).resolve()
    if not path.is_file():
        parser.error("input must be a file")
    if out == path.parent:
        parser.error("Use a separate output directory, outside the source file's directory")
    out.mkdir(parents=True, exist_ok=True)
    report = out / f"{path.stem}-inspection.json"
    if report.exists():
        raise FileExistsError(f"Use a new --out-dir; report already exists: {report}")
    if path.suffix.lower() == ".prproj":
        result = inspect_project(path)
    elif path.suffix.lower() in {".mp4", ".mov", ".avi", ".m4v", ".mkv", ".webm"}:
        result = inspect_video(path, out, args.start, args.span, args.frames)
    else:
        parser.error("Expected a video or .prproj; binary .aep inspection is not supported")
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"report": str(report), "contact_sheet": result.get("contact_sheet")}, ensure_ascii=False))


if __name__ == "__main__":
    main()

from __future__ import annotations
import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import subprocess
from typing import List, Tuple

# Paths
ROOT = Path(__file__).resolve().parent
MEDIA_DIR = ROOT / "media"
MUSIC_DIR = ROOT / "Music"
OUTPUT_DIR = ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Change this if melt.exe lives elsewhere
MELT_EXE = r"C:\\Program Files\\Shotcut\\melt.exe"

# Video settings
TARGET_W, TARGET_H, FPS = 1080, 1920, 30
FADE = 0.5  # seconds of crossfade
DO_CROSSFADES = True
DO_WATERMARK = True
DO_CAPTIONS = True

WATERMARK = os.environ.get("WATERMARK_TEXT", "@YourBrand")
CAPTIONS = os.environ.get("CAPTIONS_TEXT", "")
DO_DUCK = True

VIDEO_EXT = {".mp4",".mov",".m4v",".mkv",".webm",".MP4",".MOV",".M4V",".MKV",".WEBM"}
IMAGE_EXT = {".png",".jpg",".jpeg",".PNG",".JPG",".JPEG"}


def discover() -> List[Path]:
    """Return media files from MEDIA_DIR."""
    MEDIA_DIR.mkdir(exist_ok=True, parents=True)
    return [p for p in sorted(MEDIA_DIR.iterdir()) if p.is_file() and (p.suffix in VIDEO_EXT or p.suffix in IMAGE_EXT)]


def choose(items: List[Path], target: float) -> List[Tuple[Path, float]]:
    """Pick files and durations to roughly fill the target length."""
    out: List[Tuple[Path, float]] = []
    remain = target
    for p in items:
        if remain <= 0:
            break
        if p.suffix in IMAGE_EXT:
            dur = min(3.0, remain)
        else:
            dur = min(10.0, remain)
        out.append((p, dur))
        remain -= dur
    imgs = [p for p, _ in out if p.suffix in IMAGE_EXT]
    while remain > 0.2 and imgs:
        d = min(3.0, remain)
        out.append((imgs[0], d))
        remain -= d
    return out


def mk_mlt(chosen: List[Tuple[Path, float]], out_path: Path) -> Path:
    """Generate an MLT XML project."""
    mlt = ET.Element("mlt", version="7.22.0")
    ET.SubElement(
        mlt,
        "profile",
        width=str(TARGET_W),
        height=str(TARGET_H),
        progressive="1",
        sample_aspect_num="1",
        sample_aspect_den="1",
        display_aspect_num=str(TARGET_W),
        display_aspect_den=str(TARGET_H),
        frame_rate_num=str(FPS),
        frame_rate_den="1",
        colorspace="709",
    )

    tractor = ET.SubElement(mlt, "tractor", id="tractor0")
    multitrack = ET.SubElement(tractor, "multitrack")
    ET.SubElement(multitrack, "track", producer="plist")
    ET.SubElement(multitrack, "track", producer="plist")

    playlist = ET.SubElement(mlt, "playlist", id="plist")

    frame = lambda t: int(round(t * FPS))
    fadef = frame(FADE) if DO_CROSSFADES else 0
    pos_frames = 0

    for i, (p, d) in enumerate(chosen):
        length = frame(d)
        entry = ET.SubElement(playlist, "entry", producer=f"clip{i}")
        entry.set("in", "0")
        entry.set("out", str(max(0, length - 1)))
        start = pos_frames - fadef if i > 0 and DO_CROSSFADES else pos_frames
        entry.set("start", str(max(0, start)))
        pos_frames += length

        prod = ET.SubElement(mlt, "producer", id=f"clip{i}")
        ET.SubElement(prod, "property", name="resource").text = str(p)
        if p.suffix in IMAGE_EXT:
            ET.SubElement(prod, "property", name="mlt_service").text = "pixbuf"
            ET.SubElement(prod, "property", name="length").text = str(length)
        else:
            ET.SubElement(prod, "property", name="mlt_service").text = "avformat"
            ET.SubElement(prod, "property", name="video_delay").text = "0"

        filt = ET.SubElement(prod, "filter")
        ET.SubElement(filt, "property", name="mlt_service").text = "avfilter"
        scale = (
            f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease,"\
            f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:color=black,"\
            f"fps={FPS},format=yuv420p,setsar=1"
        )
        ET.SubElement(filt, "property", name="argument").text = scale

    if DO_WATERMARK and WATERMARK.strip():
        f = ET.SubElement(tractor, "filter")
        ET.SubElement(f, "property", name="mlt_service").text = "avfilter"
        fontfile = r"C:/Windows/Fonts/arial.ttf" if Path(r"C:/Windows/Fonts/arial.ttf").exists() else None
        if fontfile:
            arg = (
                "drawtext=fontfile='" + fontfile + "':text='" + WATERMARK.replace(":", "\\:").replace("'", "\\'") +
                "':fontsize=48:fontcolor=white@0.9:x=(w-tw)-40:y=40:box=1:boxcolor=black@0.35:boxborderw=12"
            )
        else:
            arg = (
                "drawtext=font=Arial:text='" + WATERMARK.replace(":", "\\:").replace("'", "\\'") +
                "':fontsize=48:fontcolor=white@0.9:x=(w-tw)-40:y=40:box=1:boxcolor=black@0.35:boxborderw=12"
            )
        ET.SubElement(f, "property", name="argument").text = arg

    if DO_CAPTIONS and CAPTIONS.strip():
        f = ET.SubElement(tractor, "filter")
        ET.SubElement(f, "property", name="mlt_service").text = "avfilter"
        cap = CAPTIONS.replace("\n", " ").replace(":", "\\:").replace("'", "\\'")
        fontfile = r"C:/Windows/Fonts/arial.ttf" if Path(r"C:/Windows/Fonts/arial.ttf").exists() else None
        if fontfile:
            arg = (
                "drawtext=fontfile='" + fontfile + "':text='" + cap +
                "':fontsize=58:fontcolor=white@0.98:x=(w-tw)/2:y=h-th-120:box=1:boxcolor=black@0.45:boxborderw=16"
            )
        else:
            arg = (
                "drawtext=font=Arial:text='" + cap +
                "':fontsize=58:fontcolor=white@0.98:x=(w-tw)/2:y=h-th-120:box=1:boxcolor=black@0.45:boxborderw=16"
            )
        ET.SubElement(f, "property", name="argument").text = arg

    music = None
    if MUSIC_DIR.exists():
        for m in sorted(MUSIC_DIR.iterdir()):
            if m.suffix.lower() in {".mp3", ".m4a", ".aac", ".wav", ".flac", ".ogg"}:
                music = m
                break
    if music:
        mus = ET.SubElement(mlt, "producer", id="bgm")
        ET.SubElement(mus, "property", name="mlt_service").text = "avformat"
        ET.SubElement(mus, "property", name="resource").text = str(music)
        f = ET.SubElement(mus, "filter")
        ET.SubElement(f, "property", name="mlt_service").text = "volume"
        ET.SubElement(f, "property", name="gain").text = "0.15"
        ET.SubElement(multitrack, "track", producer="bgm")
        if DO_DUCK:
            df = ET.SubElement(tractor, "filter")
            ET.SubElement(df, "property", name="mlt_service").text = "avfilter"
            ET.SubElement(df, "property", name="argument").text = "dynaudnorm=f=250:g=10:n=0.5"

    out_mlt = OUTPUT_DIR / (out_path.stem + ".mlt")
    ET.ElementTree(mlt).write(out_mlt, encoding="utf-8", xml_declaration=True)
    return out_mlt


def main() -> int:
    goal = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "make tiktok video 60"
    target = 60.0
    for t in goal.split():
        if t.isdigit():
            target = float(t)
            break

    items = discover()
    if not items:
        print("No media in ./media")
        return 1
    chosen = choose(items, target)
    total = sum(d for _, d in chosen)
    print(f"Chosen {len(chosen)} items ~{total:.1f}s")

    out_path = OUTPUT_DIR / f"draft_{os.getpid()}.mp4"
    mlt_path = mk_mlt(chosen, out_path)

    cmd = [
        MELT_EXE,
        str(mlt_path),
        "-profile",
        "vertical_1080p_30",
        "-consumer",
        f"avformat:{out_path}",
        "vcodec=libx264",
        "acodec=aac",
        "vb=8000k",
        "ab=192k",
        "threads=0",
        "real_time=-1",
    ]
    print("Running:", " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        print(proc.stderr[-2000:])
        print("Render failed")
        return 2
    print(f"Saved: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

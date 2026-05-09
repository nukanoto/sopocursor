#!/usr/bin/env python3
import argparse
import shutil
import struct
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
DIST = ROOT / "dist"
WINDOWS_BUILD = DIST / "windows"

CURSORS = {
    "arrow": {"png": "arrow.png", "hotspot": (3, 5), "roles": ["Arrow"]},
    "pointer": {"png": "pointer.png", "hotspot": (0, 0), "roles": ["Hand"]},
    "row-resize": {"png": "row-resize.png", "hotspot": (4, 16), "roles": ["SizeNS"]},
    "col-resize": {"png": "col-resize.png", "hotspot": (4, 3), "roles": ["SizeWE"]},
    "not-allowed": {"png": "not-allowed.png", "hotspot": (16, 19), "roles": ["No"]},
}

ROLE_FILES = {
    role: f"{name}.cur"
    for name, config in CURSORS.items()
    for role in config["roles"]
}

SCHEME_ROLES = [
    "Arrow",
    "Help",
    "AppStarting",
    "Wait",
    "Crosshair",
    "IBeam",
    "NWPen",
    "No",
    "SizeNS",
    "SizeWE",
    "SizeNWSE",
    "SizeNESW",
    "SizeAll",
    "UpArrow",
    "Hand",
    "Pin",
    "Person",
]


def read_png_size(png: bytes) -> tuple[int, int]:
    if png[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if png[12:16] != b"IHDR":
        raise ValueError("PNG is missing IHDR")
    return struct.unpack(">II", png[16:24])


def write_cur(png_path: Path, cur_path: Path, hotspot: tuple[int, int]) -> None:
    png = png_path.read_bytes()
    width, height = read_png_size(png)
    if width > 256 or height > 256:
        raise ValueError(f"{png_path} is too large for a cursor entry")

    header = struct.pack("<HHH", 0, 2, 1)
    directory = struct.pack(
        "<BBBBHHII",
        0 if width == 256 else width,
        0 if height == 256 else height,
        0,
        0,
        hotspot[0],
        hotspot[1],
        len(png),
        len(header) + 16,
    )
    cur_path.write_bytes(header + directory + png)


def write_inf(path: Path) -> None:
    entries = "\n".join(
        f'"{role}" = "{file_name}"'
        for role, file_name in sorted(ROLE_FILES.items())
    )
    scheme = ",".join(
        f"%10%\\%CUR_DIR%\\{ROLE_FILES[role]}" if role in ROLE_FILES else ""
        for role in SCHEME_ROLES
    )
    path.write_text(
        f"""[Version]
signature="$CHICAGO$"

[DefaultInstall]
CopyFiles=CursorFiles
AddReg=SchemeReg

[DestinationDirs]
CursorFiles=10,"%CUR_DIR%"

[CursorFiles]
arrow.cur
pointer.cur
row-resize.cur
col-resize.cur
not-allowed.cur

[SchemeReg]
HKCU,"Control Panel\\Cursors\\Schemes","SopoCursor",0x00000000,"{scheme}"

[Strings]
CUR_DIR="Cursors\\SopoCursor"

[SopoCursor]
{entries}
""",
        encoding="utf-8",
    )


def write_readme(path: Path) -> None:
    path.write_text(
        """SopoCursor for Windows

Install:
1. Extract this ZIP file.
2. Right-click install.inf and choose Install.
3. Open Windows Settings > Bluetooth & devices > Mouse > Additional mouse settings.
4. In the Pointers tab, select the SopoCursor scheme and apply it.

Included cursor roles:
- Normal Select
- Link Select
- Vertical Resize
- Horizontal Resize
- Unavailable
""",
        encoding="utf-8",
    )


def build() -> Path:
    DIST.mkdir(exist_ok=True)
    if WINDOWS_BUILD.exists():
        shutil.rmtree(WINDOWS_BUILD)
    WINDOWS_BUILD.mkdir(parents=True)

    for name, config in CURSORS.items():
        write_cur(
            ASSETS / config["png"],
            WINDOWS_BUILD / f"{name}.cur",
            config["hotspot"],
        )

    write_inf(WINDOWS_BUILD / "install.inf")
    write_readme(WINDOWS_BUILD / "README.txt")

    zip_path = DIST / "sopocursor-windows.zip"
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(WINDOWS_BUILD.iterdir()):
            if path.is_file():
                archive.write(path, arcname=path.name)
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Windows cursor package.")
    parser.add_argument(
        "--copy-to-web",
        action="store_true",
        help="Copy the Windows ZIP into web/ for deployment.",
    )
    args = parser.parse_args()

    zip_path = build()
    if args.copy_to_web:
        shutil.copy2(zip_path, ROOT / "web" / zip_path.name)
    print(zip_path.relative_to(ROOT))


if __name__ == "__main__":
    main()

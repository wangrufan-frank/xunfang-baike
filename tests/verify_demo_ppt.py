from pathlib import Path
import sys
import zipfile
import xml.etree.ElementTree as ET


PRESENTATION = Path("deliverables/巡防百科网站项目汇报.pptx")
PLACEHOLDERS = ("添加标题", "占位", "Lorem", "案件汇报", "扫黑除恶")


def slide_text(archive: zipfile.ZipFile, name: str) -> str:
    root = ET.fromstring(archive.read(name))
    return "".join(node.text or "" for node in root.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"))


def main() -> int:
    if not PRESENTATION.exists():
        print(f"missing presentation: {PRESENTATION}")
        return 1

    with zipfile.ZipFile(PRESENTATION) as archive:
        slides = sorted(
            name for name in archive.namelist()
            if name.startswith("ppt/slides/slide") and name.endswith(".xml")
        )
        if len(slides) != 9:
            print(f"expected 9 slides, found {len(slides)}")
            return 1
        text = "\n".join(slide_text(archive, slide) for slide in slides)

    found = [word for word in PLACEHOLDERS if word in text]
    if found:
        print("placeholder text found: " + ", ".join(found))
        return 1

    print("presentation verified: 9 slides, no template placeholders")
    return 0


if __name__ == "__main__":
    sys.exit(main())

from pathlib import Path
import statistics
import sys
from PIL import Image


RENDER_DIR = Path.home() / 'AppData' / 'Local' / 'Temp' / 'xunfang-ppt-qa'


def detail_region_has_content(filename: str) -> bool:
    image = Image.open(RENDER_DIR / filename).convert('RGB')
    width, height = image.size
    crop = image.crop((int(width * 0.57), int(height * 0.14), int(width * 0.91), int(height * 0.75)))
    pixels = [channel for pixel in crop.get_flattened_data() for channel in pixel]
    return statistics.pstdev(pixels) > 18


def main() -> int:
    files = ('slide-5.jpg', 'slide-7.jpg')
    missing = [name for name in files if not (RENDER_DIR / name).exists()]
    if missing:
        print('missing rendered slides: ' + ', '.join(missing))
        return 1
    blank = [name for name in files if not detail_region_has_content(name)]
    if blank:
        print('screenshot region is blank: ' + ', '.join(blank))
        return 1
    print('rendered screenshot regions contain visual content')
    return 0


if __name__ == '__main__':
    sys.exit(main())

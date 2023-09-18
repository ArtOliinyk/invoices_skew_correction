import argparse
import os
import re
from time import time

import bs4
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import pytesseract
import PIL
from PIL import Image


def tesseract_init(tesseract_path: str) -> None:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def get_rotation_angle(image_path: str, hocr_path: str = 'hocr_output') -> float:
    pytesseract.pytesseract.run_tesseract(image_path, hocr_path, extension='png',
                                          lang='ukr+eng', config="--psm 6 -c tessedit_create_hocr=1")

    xml_input = open(hocr_path + '.hocr', "r", encoding="utf-8")
    soup = bs4.BeautifulSoup(xml_input, 'html.parser')
    ocr_lines = soup.findAll("span", {"class": "ocr_line"})
    lines_skew = []
    pattern = r'baseline\s+(-?\d+\.\d+)'
    for line in ocr_lines:
        match = re.search(pattern, str(line))
        if match is not None:
            lines_skew.append(match.group(1))

    lines_skew = np.array(lines_skew, dtype='float')
    rt_angle = -np.degrees(np.mean(lines_skew))

    return rt_angle


def rotate_image(image_path: str, angle: float) -> Image:
    image = Image.open(image_path)
    image = image.rotate(-angle, PIL.Image.NEAREST, expand=1, fillcolor='white')
    return image


def validate_photo_exists(photo_path: str) -> None:
    if photo_path is None:
        raise ValueError("filepath argument should not be None!")

    if not os.path.exists(photo_path):
        raise FileNotFoundError(f"Please validate photo exists within path: {photo_path}")


def show_results(before_path: str, after_path: str) -> None:
    image_before = mpimg.imread(before_path)
    image_after = mpimg.imread(after_path)

    plt.subplot(1, 2, 1)
    plt.imshow(image_before)
    plt.title(os.path.basename(before_path))

    plt.subplot(1, 2, 2)
    plt.imshow(image_after)
    plt.title(os.path.basename(after_path))

    plt.show()


def process_image(filepath: str, res_filename: str = None, compare: bool = False) -> Image:
    t_start = time()
    print(f"processing file within path: {filepath}")

    validate_photo_exists(filepath)

    angle = get_rotation_angle(filepath)
    print(f"Estimated rotation angle: {angle}")
    
    if res_filename is None:
        res_filename = filepath.replace(".png", f"__rotated_{round(angle)}_deg.png")

    rotated_img = rotate_image(filepath, angle)
    rotated_img.save(res_filename)

    print(f"Inference time: {round(time() - t_start, 2)}s.")

    if compare:
        show_results(filepath, res_filename)

    return rotated_img


def process_bulk_dir(dir_path: str) -> None:
    files_in_dir = os.listdir(dir_path)
    files_in_dir = [f for f in files_in_dir if f.endswith(".png")]
    for file in files_in_dir:
        filepath = os.path.join(dir_path, file)
        process_image(filepath)


def main() -> None:
    parser = argparse.ArgumentParser(prog='Estimate angle, rotate image and save')
    parser.add_argument('-f', '--filepath')
    parser.add_argument('-r', '--resname', required=False, type=str, default=None)
    parser.add_argument('-c', '--compare', action='store_true')
    args = parser.parse_args()
    process_image(args.filepath, args.resname, args.compare)


if __name__ == '__main__':
    # process_bulk_dir("invoices_rotated")
    main()

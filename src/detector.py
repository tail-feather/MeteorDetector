import argparse
import math
import os
import sys
import typing

import cv2
import numpy


def load_binary(filepath: str, input_threshold: float = 127, input_maxvalue: float = 255) -> numpy.array:
    """
    しきい値適用済み2値画像読み込み
    :param filepath: 入力ファイルパス
    :param input_threshold: 入力閾値
    :param input_maxvalue: 閾値最大値
    :return: 2値画像データ
    """
    filepath = str(filepath)
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE | cv2.IMREAD_IGNORE_ORIENTATION)
    _, thr = cv2.threshold(img, input_threshold, 255, cv2.ADAPTIVE_THRESH_MEAN_C)
    return thr


def detect_lines(img: numpy.array, min_length: float = 20, line_gap: float = 3) -> list[numpy.array]:
    """
    直線検出
    :param img: 入力画像（2値画像）
    :return: 検出直線リスト
    """
    lines = cv2.HoughLinesP(img, rho=1, theta=math.pi/180, threshold=200, minLineLength=min_length, maxLineGap=line_gap)
    return lines


def detect_area(img: numpy.array, area_threshold: float = 0.0001) -> list[numpy.array]:
    """
    閾値を超える面積を持つ輪郭の検出
    :param img: 入力画像
    :param area_threshold: 面積閾値（画像全体の何%を`(0, 1]`で指定）
    :return: 閾値を超えた面積の領域リスト
    """
    height, width = img.shape
    img_area = width * height
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    contours = [cnt for cnt in contours if (cv2.contourArea(cnt) / img_area) > area_threshold]
    return contours


T = typing.TypeVar("T")


def clamp(v: T, min_v: T, max_v: T) -> T:
    """
    clamp関数
    入力値を`[min_v, max_v]`の範囲に収める
    :param T v: 入力値
    :param T min_v: 最小値
    :param T max_v: 最大値
    :return: `[min_v, max_v]`内に収めた値
    """
    return min(max_v, max(v, min_v))


BoundingRect = tuple[tuple[float, float], tuple[float, float]]


def fill_area(img: numpy.array, contours: list[numpy.array], buffer_ratio: float = 1.1, color: typing.Optional[float] = None) -> numpy.array:
    """
    領域の外接矩形で塗りつぶす
    :param img: 入力画像
    :param contours: 領域リスト
    :param buffer_ratio: バッファ拡張率
    :param color: 塗りつぶしの色（未指定の場合は入力画像の中央値で塗りつぶす）
    :return: 塗りつぶし後の画像
    """
    height, width = img.shape
    x_buffer = int(width * buffer_ratio)
    y_buffer = int(height * buffer_ratio)
    # detect fill color
    if color is None:
        color = numpy.median(img)
    # fill bounding rect
    for cnt in contours:
        hull = cv2.convexHull(cnt)
        M = cv2.moments(hull)
        cx = M["m10"] / M["m00"]
        cy = M["m01"] / M["m00"]
        temp = []
        for c in hull:
            x, y = c[0]
            vx = x - cx
            vy = y - cy
            x = clamp(vx * buffer_ratio + cx, 0, width)
            y = clamp(vy * buffer_ratio + cy, 0, height)
            temp.append([int(x), int(y)])
        img = cv2.fillPoly(img, pts=[numpy.asarray(temp)], color=(color,))
    return img


def line_length(line: numpy.array) -> float:
    """
    直線の長さの算出
    `cv2.HoughLinesP()`の返り値は`[ [ [start_x, start_y, end_x, end_y] ], ... ]`形式になっている
    :param line: `[ [start_x, start_y, end_x, end_y] ]`であること
    :return: 直線の長さ
    """
    assert len(line) == 1
    sx, sy, ex, ey = line[0]
    dx = ex - sx
    dy = ey - sy
    return math.sqrt(dx * dx + dy * dy)


def detect_meteor(filepath: str, input_threshold: float = 127, input_maxvalue: float = 255, area_threshold: float = 0.0001, buffer_ratio: float = 1.1, line_threshold: float = 100) -> typing.Optional[tuple[list[numpy.array], list[BoundingRect], tuple[int, int]]]:
    """
    流星の検出
    :param str filepath: 入力画像ファイルパス
    :param float input_threshold: 画像のしきい値処理
    :param float input_maxvalue: 画像のしきい値処理最大値
    :param float area_threshold: 面積のある領域検知用閾値（`detect_area()`関数`threshold`参照）
    :param float buffer_ratio: 面積拡張率
    :param float line_threshold: 検出した直線を流星と判定する最小の長さ
    :return: (検出した直線 or None, 塗りつぶした領域 or None)
    """
    img = load_binary(filepath, input_threshold, input_maxvalue)
    area_contours = detect_area(img, area_threshold)
    if area_contours:
        img = fill_area(img, area_contours, buffer_ratio=buffer_ratio, color=0)
    lines = detect_lines(img)
    if lines is not None:
        line_lengthes = [line_length(x) for x in lines]
        length = max(line_lengthes)
        if length > line_threshold:
            filtered_lines = [x for x, y in zip(lines, line_lengthes) if y > line_threshold]
            return filtered_lines, area_contours, img.shape
    return None, area_contours, img.shape


def main(argv: list[str]) -> int:
    from tqdm import tqdm
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--input-threshold", type=float, default=127)
    parser.add_argument("--input-maxvalue", type=float, default=255)
    parser.add_argument("--area-threshold", type=float, default=0.0001)
    parser.add_argument("--buffer-ratio", type=float, default=1.1)
    parser.add_argument("--line-threshold", type=float, default=100)

    args = parser.parse_args(argv[1:])

    # 拡張子が`.jpg`の画像リストを作成
    image_list = []
    for dirname, _, filenames in os.walk(args.directory):
        image_list.extend([os.path.join(dirname, x) for x in filenames if x.lower().endswith(".jpg") or x.lower().endswith(".jpeg")])
    image_list.sort()

    # 流星の写っていると思われる画像を抽出
    result = []
    for filepath in tqdm(image_list):
        filepath = str(filepath)
        lines, _, _ = detect_meteor(
            filepath,
            args.input_threshold,
            args.input_maxvalue,
            args.area_threshold,
            args.buffer_ratio,
            args.line_threshold
        )
        if lines is not None:
            result.append((filepath, lines))
    print("detected: {}/{}".format(len(result), len(image_list)))
    if result:
        print("files:")
        for filepath, lines in result:
            print(filepath)

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

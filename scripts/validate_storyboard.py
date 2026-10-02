#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""宫格分镜 JSON 机检（manju-video 技能）。

校验宫格分镜智能体产出的 JSON 是否满足约束：
  C1 可解析的 JSON（容忍 ```json 围栏包裹）
  C2 shots 数量与宫格数一致（5x5=25 / 3x3=9，可用 --n 覆盖）
  C3 每条 prompt_text 词数在 20-30（超出计警告）
  C5 必含 "no timecode" 与 "no subtitles"
  C4/C6 禁用句式（"A scene showing" / "There is a" / "in corner"）

用法:
    python validate_storyboard.py <story.json> [--n 25|9]
    python validate_storyboard.py --selftest
退出码: 0=无错误, 1=存在错误, 2=用法/文件错误
"""
import argparse
import json
import re
import sys

FORBIDDEN = ["A scene showing", "There is a", "in corner"]
REQUIRED = ["no timecode", "no subtitles"]
WORD_RANGE = (20, 30)
LAYOUT_N = {"5x5": 25, "3x3": 9}


def strip_fences(text):
    m = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    return m.group(1) if m else text


def check(data, expect_n):
    errors, warnings = [], []
    layout = str(data.get("grid_layout", ""))
    shots = data.get("shots")
    if not isinstance(shots, list):
        errors.append("缺少 shots 数组")
        return errors, warnings

    n = expect_n or LAYOUT_N.get(layout)
    if n is None:
        warnings.append(f"grid_layout={layout!r} 无法推断数量，跳过数量检查")
    elif len(shots) != n:
        errors.append(f"shots 数量 {len(shots)} != 应为 {n}（grid_layout={layout or '未填'}）")

    for i, shot in enumerate(shots, 1):
        tag = f"分镜{i}"
        if not isinstance(shot, dict):
            errors.append(f"{tag}: 不是对象")
            continue
        prompt = shot.get("prompt_text", "")
        if not shot.get("shot_number"):
            warnings.append(f"{tag}: 缺 shot_number")
        words = len(prompt.split())
        if not WORD_RANGE[0] <= words <= WORD_RANGE[1]:
            warnings.append(f"{tag}: 词数 {words} 超出 {WORD_RANGE[0]}-{WORD_RANGE[1]}")
        for req in REQUIRED:
            if req not in prompt:
                errors.append(f"{tag}: 缺必含排除词 {req!r}")
        for bad in FORBIDDEN:
            if bad.lower() in prompt.lower():
                errors.append(f"{tag}: 含禁用句式 {bad!r}")
    return errors, warnings


def selftest():
    good_prompt = ("Medium Shot, the woman from image_1.png grips her sword tightly, "
                   "intense expression, snow background, cinematic lighting, "
                   "no timecode, no subtitles.")
    bad_prompt = ("A scene showing a village in the mountains at dawn, "
                  "beautiful warm light over the rooftops, highly detailed.")
    good = {"grid_layout": "3x3", "grid_aspect_ratio": "16:9",
            "shots": [{"shot_number": str(i), "prompt_text": good_prompt} for i in range(1, 10)]}
    bad = {"grid_layout": "3x3",
           "shots": [{"shot_number": "1", "prompt_text": bad_prompt}] * 8}
    e1, _ = check(good, None)
    e2, _ = check(bad, None)
    assert not e1, f"正例误报: {e1}"
    assert len(e2) >= 3, f"负例漏报: {e2}"  # 数量 8!=9 + 禁用句式 + 2 个必含词缺失
    print("selftest PASS（正例 0 错，负例抓到 %d 错）" % len(e2))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="分镜 JSON 文件（容忍 ```json 围栏）")
    ap.add_argument("--n", type=int, choices=(9, 25), help="期望 shots 数量，默认按 grid_layout 推断")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not args.file:
        ap.print_help()
        return 2
    try:
        raw = Path(args.file).read_text(encoding="utf-8")
        data = json.loads(strip_fences(raw))
    except FileNotFoundError:
        print(f"文件不存在: {args.file}")
        return 2
    except (json.JSONDecodeError, ValueError) as exc:
        print(f"C1 JSON 解析失败: {exc}")
        return 1

    errors, warnings = check(data, args.n)
    for w in warnings:
        print(f"警告: {w}")
    for e in errors:
        print(f"错误: {e}")
    print("PASS" if not errors else f"FAIL（{len(errors)} 错误 / {len(warnings)} 警告）")
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

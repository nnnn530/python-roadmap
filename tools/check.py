"""摸底题自检脚本。

用法（在 D:\\code\\python-roadmap 下）：
    python tools\\check.py

它会用 3 组数据运行 src\\baseline.py，比对最大值/最小值/平均值。
答案写对了就三组全绿，否则会告诉你哪一组不对（但不会给你答案）。
"""

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "src" / "baseline.py"

CASES = [
    [87, 12, 45, 66, 3, 99, 21, 8, 54, 30],
    [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
    [-10, -3, -77, 0, 42, -1, 8, -25, 100, 6],
]

PATTERNS = {
    "最大值": r"(?:最大值|max)\s*[:：=]\s*(-?\d+(?:\.\d+)?)",
    "最小值": r"(?:最小值|min)\s*[:：=]\s*(-?\d+(?:\.\d+)?)",
    "平均值": r"(?:平均值|avg|average)\s*[:：=]\s*(-?\d+(?:\.\d+)?)",
}


def expected(numbers: list[int]) -> dict[str, float]:
    return {
        "最大值": float(max(numbers)),
        "最小值": float(min(numbers)),
        "平均值": round(sum(numbers) / len(numbers), 2),
    }


def run_case(numbers: list[int]) -> tuple[str, int]:
    stdin = "\n".join(str(n) for n in numbers) + "\n"
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [sys.executable, str(TARGET)],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=30,
        env=env,
    )
    return proc.stdout + proc.stderr, proc.returncode


def main() -> int:
    if not TARGET.exists():
        print(f"[X] 找不到 {TARGET}")
        return 2

    passed = 0
    for idx, numbers in enumerate(CASES, 1):
        out, code = run_case(numbers)
        if code != 0:
            print(f"[X] 第 {idx} 组：程序异常退出（exit {code}）")
            print("    最后几行输出：")
            for line in out.strip().splitlines()[-5:]:
                print(f"    {line}")
            continue

        want = expected(numbers)
        got = {}
        for name, pattern in PATTERNS.items():
            m = re.search(pattern, out)
            if m:
                got[name] = float(m.group(1))

        missing = [k for k in want if k not in got]
        if missing:
            print(f"[X] 第 {idx} 组：输出里找不到 {', '.join(missing)}（格式没照要求写？）")
            continue

        wrong = [
            f"{k}: 你写的 {got[k]:g}，应为 {want[k]:g}"
            for k in want
            if abs(got[k] - want[k]) > 0.011
        ]
        if wrong:
            print(f"[X] 第 {idx} 组：")
            for line in wrong:
                print(f"    {line}")
        else:
            passed += 1
            print(f"[OK] 第 {idx} 组通过（{numbers[0]}, {numbers[1]}, ... 共 10 个）")

    print()
    if passed == len(CASES):
        print(f"全部 {len(CASES)} 组通过 —— 摸底题完成，可以 git commit 了。")
        return 0
    print(f"通过 {passed}/{len(CASES)} 组。先自己debug，卡住了再喊我。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

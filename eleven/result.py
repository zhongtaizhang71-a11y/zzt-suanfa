"""生成第 11 课报告交付物：比较次数表（n=100/200/400/800）+ 一句结论。

运行方式（必须用 3.11+，老师脚手架的 dataclass(slots=True) 需要）:
    py -3.11 result.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

SRC = Path(__file__).resolve().parent / "学生作业包" / "src"
sys.path.insert(0, str(SRC))

from herodungeon.m2_equip_search import run_sort_benchmark

COLUMNS = (
    "n",
    "quick_comparisons",
    "bubble_comparisons",
    "selection_comparisons",
    "bubble_over_quick",
)

def build_markdown(rows: list[dict[str, object]]) -> str:
    lines = ["## 比较次数表（seed=42，按 power 升序）", ""]
    lines.append("| " + " | ".join(COLUMNS) + " |")
    lines.append("|" + " --- |" * len(COLUMNS))
    for row in rows:
        lines.append("| " + " | ".join(str(row[c]) for c in COLUMNS) + " |")

    first, last = rows[0], rows[-1]
    lines += [
        "",
        "## 一句结论",
        "",
        f"随机大规模数据下快排比较次数远少于冒泡"
        f"（比值随 n 从 {first['bubble_over_quick']} 升至 {last['bubble_over_quick']}，"
        f"因冒泡 O(n^2)、快排 O(n log n)），"
        "但数据已有序时冒泡提前退出仅 n-1 次比较反而更快——"
        "选型取决于数据分布与规模。",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    rows = run_sort_benchmark()
    markdown = build_markdown(rows)
    print(markdown)

    out_path = Path(__file__).resolve().parent / "比较次数表与结论.md"
    out_path.write_text(markdown, encoding="utf-8")
    print(f"已写入: {out_path}")


if __name__ == "__main__":
    main()
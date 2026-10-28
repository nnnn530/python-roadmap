"""命令行入口：这个文件只负责「跟用户打交道」。

顺序永远是：解析参数 → 调别人干活 → 打印 / 写文件 → 决定退出码（0 成功 / 1 出错）。

统计逻辑在 counter.py，读文件在 io_utils.py，这里一行统计代码都不该有。
"""

import argparse
import sys

from counter import count_words, top_n
from io_utils import read_text, write_json


def build_parser():
    """把「用户能敲什么」定义出来，-h 的说明文字就是从这儿来的。"""
    parser = argparse.ArgumentParser(
        description="词频统计器：统计一个 txt 里出现最多的词"
    )
    # required=True：不给 --file 就直接报错，不用我们自己判空
    parser.add_argument("--file", required=True, help="要统计的 txt 文件路径")
    # 可选参数：有横杠，可不给；type=int 很关键，不写拿到的是字符串 '5'
    parser.add_argument("--top", type=int, default=10, help="输出前 N 个词，默认 10")
    parser.add_argument("--output", help="把结果写成 JSON 文件；不给就打印到屏幕")
    return parser


def main():
    """返回退出码：0 = 成功，1 = 出错。"""
    args = build_parser().parse_args()

    try:
        text = read_text(args.file)
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.file}")
        return 1
    except (IsADirectoryError, PermissionError):
        # Windows 上传一个目录会报 PermissionError，不是 IsADirectoryError，两个都接
        print(f"错误：{args.file} 是个文件夹（或者我没有权限读），请给一个 txt 文件")
        return 1
    except UnicodeDecodeError:
        print(f"错误：{args.file} 不是 UTF-8 编码的文本，读不了")
        return 1

    counts = count_words(text)
    rows = top_n(counts, args.top)

    if not rows:
        print(f"提示：{args.file} 里没有可统计的词")
        return 0

    if args.output:
        # JSON 里用 {单词: 次数} 的对象形式，比 [[单词, 次数]] 更好读
        data = {"file": args.file, "top": {word: count for word, count in rows}}
        write_json(args.output, data)
        print(f"已写入 {args.output}")
    else:
        for word, count in rows:
            print(f"{word:<12}{count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

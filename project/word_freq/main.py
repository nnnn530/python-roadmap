r"""命令行入口：解析参数 → 调别人干活 → 打印 / 写文件 → 决定退出码。

三条规矩：
1. 日志只在这里配置（setup_logging）。库只广播，入口装喇叭。
2. 正常结果走 stdout（print），错误走 stderr（fail），诊断走 logging。
   这样别人 `python main.py ... > 结果.txt` 时，结果进文件、错误还在屏幕上。
3. 每一层只处理自己认识的错，认不出的往上抛，最外层兜底。
"""

import argparse
import logging
import sys

from counter import count_words, top_n
from io_utils import read_text, write_json

log = logging.getLogger("word_freq")

OFF = logging.CRITICAL + 1      # 比最高级别还高一级 = 谁都不许说话（默认安静）


def positive_int(text):
    """给 --top 用的校验函数：必须是 ≥1 的整数。

    argparse 的 type= 可以填任意函数。函数里抛 ArgumentTypeError 时，
    argparse 会自动打印那句错误 + 退出码 2，比我们手写检查省事。
    """
    try:
        value = int(text)
    except ValueError:
        raise argparse.ArgumentTypeError(f"「{text}」不是整数")
    if value < 1:
        raise argparse.ArgumentTypeError("N 必须是正整数（≥1）")
    return value


def setup_logging(verbose, log_file):
    """只在入口配置一次日志。

    - 默认：级别 OFF，什么都不打（用户只该看到结果）
    - -v   ：DEBUG，全打
    - --log-file：写文件，永远是 DEBUG（事后排查用）
    """
    if log_file:
        handlers = [logging.FileHandler(log_file, encoding="utf-8")]
        level = logging.DEBUG
    else:
        handlers = [logging.StreamHandler()]        # 默认流向 stderr
        level = logging.DEBUG if verbose else OFF

    logging.basicConfig(
        level=level,
        # %(name)s 就是 getLogger(__name__) 传进去的模块名 —— 一眼看出是哪个文件在说话
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
        force=True,     # 重复调用时重置；不加的话第二次 basicConfig 会被忽略（pytest 里很坑）
    )


def build_parser():
    """规定「用户能敲什么」，-h 的内容全部由这里自动生成。"""
    parser = argparse.ArgumentParser(
        description="词频统计器：统计一个 txt 里出现最多的词"
    )
    parser.add_argument("--file", required=True, help="要统计的 txt 文件路径")
    parser.add_argument("--top", type=positive_int, default=10, help="输出前 N 个词，默认 10")
    parser.add_argument("--output", help="把结果写成 JSON 文件；不给就打印到屏幕")
    parser.add_argument("-v", "--verbose", action="store_true", help="打印调试日志（排错时用）")
    parser.add_argument("--log-file", help="把日志写进这个文件（DEBUG 级别，方便事后查）")
    return parser


def fail(message, code=1):
    """统一的出错出口：错误走 stderr，退出码 1。"""
    print(f"错误：{message}", file=sys.stderr)
    log.error(message)
    return code


def main():
    args = build_parser().parse_args()

    try:
        setup_logging(args.verbose, args.log_file)
    except OSError as exc:
        print(f"错误：日志文件写不了（{exc}）", file=sys.stderr)
        return 1

    log.debug("参数：file=%s top=%s output=%s", args.file, args.top, args.output)

    # ---- 读 ----
    try:
        text = read_text(args.file)
    except FileNotFoundError:
        return fail(f"找不到文件 {args.file}")
    except (IsADirectoryError, PermissionError):
        return fail(f"{args.file} 是个文件夹，或者没有读取权限")
    except UnicodeDecodeError:
        return fail(f"{args.file} 不是 UTF-8 编码的文本，请先另存为 UTF-8")
    except OSError as exc:
        # 兜底：上面没覆盖到的系统级错误。
        # 必须写在所有子类之后 —— FileNotFoundError 本身就是 OSError 的子类，
        # 顺序反了的话，具体的错误永远轮不到，全被这条吞掉。
        return fail(f"读 {args.file} 失败：{exc}")

    # ---- 算 ----
    counts = count_words(text)
    rows = top_n(counts, args.top)
    log.debug("共 %d 个不同的词，取前 %d 个", len(counts), args.top)

    if not rows:
        # 空文件不是「错误」，是「结果就是空」，所以走 stdout + 退出码 0
        print(f"提示：{args.file} 里没有可统计的词")
        return 0

    # ---- 写 ----
    if args.output:
        data = {"file": args.file, "top": {word: count for word, count in rows}}
        try:
            write_json(args.output, data)
        except FileNotFoundError:
            return fail(f"写出失败：{args.output} 所在的文件夹不存在")
        except PermissionError:
            return fail(f"写出失败：没有权限写 {args.output}（文件可能被别的程序占用）")
        except OSError as exc:
            return fail(f"写出失败：{exc}")
        print(f"已写入 {args.output}")
    else:
        for word, count in rows:
            print(f"{word:<12}{count}")

    log.debug("完工")
    return 0


if __name__ == "__main__":
    sys.exit(main())

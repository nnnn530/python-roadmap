# 词频统计器 v1

给一个 txt 文件，告诉里面出现最多的词。

## 用法

在仓库根目录 `D:\code\python-roadmap` 下执行：

```bash
python project\word_freq\main.py -h

python project\word_freq\main.py --file data\sample.txt --top 5
```

输出：

```
the         5
a           4
you         3
quick       2
fox         2
```

```bash
python project\word_freq\main.py --file data\sample.txt --top 3 --output out.json
```

`out.json`：

```json
{
  "file": "data\\sample.txt",
  "top": {
    "the": 5,
    "a": 4,
    "you": 3
  }
}
```

## 参数

| 参数 | 必填 | 默认 | 说明 |
|---|---|---|---|
| `--file` | 是 | — | 要统计的 txt 文件路径 |
| `--top` | 否 | `10` | 输出前 N 个词，必须是 ≥1 的整数 |
| `--output` | 否 | 无（打印到屏幕） | 把结果写成 JSON 文件 |
| `-v` / `--verbose` | 否 | 关 | 打印调试日志（排错时用） |
| `--log-file` | 否 | 无 | 把日志写进文件（DEBUG 级别，事后排查用） |

## 三种输出走三条路

| 走哪条 | 内容 | 例子 |
|---|---|---|
| **stdout**（`print`） | 结果 | `the 5`、`已写入 out.json` |
| **stderr**（`print(..., file=sys.stderr)`） | 用户能看懂的错 | `错误：找不到文件 xxx.txt` |
| **logging**（默认关，`-v` 打开） | 给开发者看的诊断 | `DEBUG io_utils: 读到 304 个字符` |

这个分流的直接好处：`> 结果.txt` 重定向时，**结果进文件、错误还在屏幕上**，不会混在一起。

## 日志

```bash
# 打开日志，看它每一步在干什么
python project\word_freq\main.py --file data\sample.txt -v

# 日志写文件，事后查
python project\word_freq\main.py --file data\sample.txt --log-file run.log
```

日志长这样（格式 `%(asctime)s %(levelname)s %(name)s: %(message)s`）：

```
12:32:55 DEBUG   word_freq: 参数：file=data\sample.txt top=3 output=None
12:32:55 DEBUG   io_utils: 准备读取：data\sample.txt
12:32:55 DEBUG   io_utils: 读到 304 个字符
12:32:55 DEBUG   counter: 统计完成：42 个不同的词
```

中间那个 `word_freq` / `io_utils` / `counter` 是模块名 —— 一眼看出**是哪个文件在说话**，
这就是每个模块写 `getLogger(__name__)` 的意义。

级别：`DEBUG(10) < INFO(20) < WARNING(30) < ERROR(40) < CRITICAL(50)`。
默认级别设成 `CRITICAL + 1`（比最高还高一级）= **全关**；`-v` 才放行到 `DEBUG`。

## 文件分工

```
project/word_freq/
├── main.py      # 跟用户打交道：参数、日志配置、打印、退出码
├── counter.py   # 只管算：count_words / top_n（只有 getLogger，不配置日志）
├── io_utils.py  # 只管读写：read_text / write_json（同上）
└── README.md    # 就是你正在看的这个
```

`counter.py` 和 `io_utils.py` 里没有一句 `print`、`sys.exit`，也**不配置日志**（只 `getLogger`）。
**日志配置只允许出现在 `main.py`** —— 库不知道使用者要把日志打屏幕还是写文件，那是入口的话语权。

## 出错时

| 情况 | 提示（走 stderr） | 退出码 |
|---|---|---|
| 文件不存在 | `错误：找不到文件 xxx.txt` | 1 |
| 传的是文件夹 / 没权限 | `错误：xxx 是个文件夹，或者没有读取权限` | 1 |
| 不是 UTF-8 文本 | `错误：xxx 不是 UTF-8 编码的文本，请先另存为 UTF-8` | 1 |
| 输出目录不存在 | `错误：写出失败：xxx 所在的文件夹不存在` | 1 |
| 输出文件被占用 | `错误：写出失败：没有权限写 xxx（文件可能被别的程序占用）` | 1 |
| 其他系统级错误 | `错误：读/写 xxx 失败：<原始信息>` | 1 |
| 没给 `--file` | argparse 自动报 `required: --file` | 2 |
| `--top 0` | argparse 自动报 `N 必须是正整数（≥1）` | 2 |
| `--top abc` | argparse 自动报 `「abc」不是整数` | 2 |
| 空文件（没有词） | `提示：xxx 里没有可统计的词`（走 stdout） | 0 |

退出码约定：**0 成功 / 1 业务错误 / 2 用法错误**，写脚本串流程时靠它判断。

## 自测

```bash
python project\word_freq\counter.py     # counter.py 全部通过
python project\word_freq\io_utils.py    # io_utils.py 全部通过
```

## 已知限制（v1 故意不做）

- 按空白切词，标点跟着单词走：`dog,` 和 `dog` 算两个词
- 区分大小写：`The` 和 `the` 算两个词
- 次数相同时，按首次出现的先后排（`sorted` 是稳定排序）
- 大文件一次性读进内存（几个 G 的日志会爆，需要用逐行流式处理）

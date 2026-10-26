r"""day04 函数练习（2026-10-25）

主题：函数定义 / 返回值 / 参数 / 纯函数可测

任务：把 10-22 的摸底程序（src\baseline.py）拆成 3 个函数。

为什么要拆？摸底版的 main() 里混了两件事：
    读输入  → 必须人肉敲 10 个数，没法自动测
    算结果  → 换个数据就该能自动测（assert）
把「算」抽成纯函数（只靠参数、只靠返回值），才能写 assert。
这和后端写接口是同一件事：核心逻辑和输入输出分离。

运行方式：
    cd D:\code\python-roadmap
    python src\day04_func.py

提交：
    git add . && git commit -m "day04: LC1 哈希表版 + 摸底程序拆函数" && git push
"""


def read_numbers(n):
    """读入 n 个数字（每行一个），返回 list[float]。

    注意：这个函数里有 input()，自测时没法 assert，只手动跑一遍。
    提示：照 baseline.py 里 for i in range(10) 那段改写，把 10 换成 n。
    """
    nums = []
    for i in range(n):
        num = input()
        nums.append(float(num))
    return nums


def stats(numbers):
    """返回 (最大值, 最小值, 平均值)，平均值保留 2 位小数。

    例：stats([1, 2, 3]) -> (3, 1, 2.0)
    空列表返回 None（先不抛异常，下周讲 try/except 时再补）
    """
    # TODO: 自己写
    if not numbers:
        return None
    ma = max(numbers)
    mi = min(numbers)
    average = round(sum(numbers)/len(numbers), 2)
    return ma, mi, average



def main():
    """读 10 个数，按 baseline.py 的格式打印三行：

        最大值: 87
        最小值: 12
        平均值: 45.30
    """
    # TODO: 自己写（调 read_numbers + stats，然后 print）
    numbers = read_numbers(10)
    ma, mi ,average = stats(numbers)
    print(f"最大值: {ma}")
    print(f"最小值: {mi}")
    print(f"平均值: {average:.2f}")


if __name__ == "__main__":
    assert stats([1, 2, 3]) == (3, 1, 2.0)
    assert stats([5]) == (5, 5, 5.0)
    assert stats([]) is None          # 边界：空列表返回 None
    print("统计函数全部通过")

    # 手动跑一遍读输入（不想敲 10 个数就把下面这行注释掉）
    main()

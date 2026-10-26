r"""day04 递归入门（2026-10-25 加练）

递归 = 不要在函数里想「怎么一步步做完」，只回答两个问题：
    1. 什么时候停？（终止条件 / base case）
    2. 大问题能变成哪个「更小的同类问题」？（递归调用）

写完对照：任何一个递归函数，先写 1，再写 2。顺序反了就会写不出来。

运行方式：
    cd D:\code\python-roadmap
    python src\day04_recursion.py
"""


def sum_list(nums):
    """递归求列表所有元素之和，不许用 sum()，不许用 for/while。

    例：sum_list([1, 2, 3]) -> 6
        sum_list([]) -> 0

    提示：空列表是终止条件；否则 = 第一个元素 + 剩下的和（nums[1:]）
    """
    # TODO: 两行就够——先写 if，再写 return ... + sum_list(...)
    if not nums:
        return 0
    return nums[0] + sum_list(nums[1:])


def factorial(n):
    """递归求 n!，n 为 0 或 1 时返回 1。

    例：factorial(0) -> 1
        factorial(5) -> 120
    """
    # TODO
    if n == 0 or n==1:
        return 1
    return n*factorial(n-1)


def count_down(n):
    """递归打印 n, n-1, ..., 1，每个一行，不返回值。

    例：count_down(3) 输出
        3
        2
        1

    关键对比：先 print 再递归 → 输出 3 2 1
              先递归再 print → 输出 1 2 3
    两种都写成两个版本对比一下（count_down / count_up）。
    """
    # TODO
    if n == 0:
        return
    print(n)
    return(count_down(n-1))
    


def count_up(n):
    """和 count_down 一样要打印 1..n，但用「先递归、后 print」的顺序。

    例：count_up(3) 输出
        1
        2
        3
    """
    # TODO
    if n == 0:
        return
    count_up(n - 1)   # 先把 1..n-1 打完（相信它已经对了）
    print(n)          # 我补最后一个


if __name__ == "__main__":
    assert sum_list([]) == 0
    assert sum_list([1, 2, 3]) == 6
    assert sum_list([10]) == 10

    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120

    print("--- count_down(3) ---")
    count_down(3)
    print("--- count_up(3) ---")
    count_up(3)

    print("递归全部通过")

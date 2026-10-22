"""摸底题（2026-10-22）——不许查资料，自己写完。

要求：
    连续读入 10 个数字（每行一个），输出最大值、最小值、平均值（保留 2 位小数）。

输出格式必须完全照下面（中英文冒号都行，数字后面不要加单位）：
    最大值: 87
    最小值: 12
    平均值: 45.30

写完后在 D:\code\python-roadmap 下运行自检：
    python tools\check.py
"""


def main() -> None:
    numbers = []
    for i in range(10):
        # input() 返回的是字符串，要自己转成数字
        raw = input(f"第 {i + 1} 个数字: ")
        numbers.append(float(raw))

    # TODO: 从这里开始自己写
    # 提示：最大值可以用循环比较，也可以用内置函数；平均值注意 10 个整数时结果要对
    maximum = 0
    minimum = 0
    average = 0.0
    maximum = max(numbers)
    minimum = min(numbers)
    average = sum(numbers)/10
    print(f"最大值: {maximum}")
    print(f"最小值: {minimum}")
    print(f"平均值: {average:.2f}")


if __name__ == "__main__":
    main()

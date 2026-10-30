r"""栈/队列随机压测（2026-10-30）

不依赖 src\day08_stack_queue.py 里的断言，用随机数据独立对拍：
    栈  push 序列 [..] → pop 出来必须是它的**倒序**
    队列 enqueue 序列 [..] → dequeue 出来必须是**原序**

跑法：
    cd D:\code\python-roadmap
    python tools\check_stack_queue.py
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from day08_stack_queue import Queue, Stack


def main():
    rng = random.Random(20261030)          # 固定种子，失败能复现
    trials = 500
    for _ in range(trials):
        n = rng.randint(0, 50)
        values = [rng.randint(-99, 99) for _ in range(n)]

        s = Stack()
        for v in values:
            s.push(v)
        assert len(s) == n, f"栈长度错：压了 {n} 个，len 拿到 {len(s)}"
        popped = [s.pop() for _ in range(n)]
        assert popped == values[::-1], f"栈顺序错（应倒序）\n  压入 {values}\n  弹出 {popped}"
        assert s.is_empty() is True, "弹光之后栈应该是空的"

        q = Queue()
        for v in values:
            q.enqueue(v)
        assert len(q) == n, f"队列长度错：入队 {n} 个，len 拿到 {len(q)}"
        dequeued = [q.dequeue() for _ in range(n)]
        assert dequeued == values, f"队列顺序错（应原序）\n  入队 {values}\n  出队 {dequeued}"
        assert q.is_empty() is True, "出光之后队列应该是空的"

    # 空结构必须抛 IndexError，而不是返回 None
    for cls, take in ((Stack, "pop"), (Queue, "dequeue")):
        obj = cls()
        try:
            getattr(obj, take)()
        except IndexError:
            pass
        else:
            raise AssertionError(f"{cls.__name__}.{take}() 在空的时候没有抛 IndexError")

    print(f"{trials} 组随机压测通过：栈 LIFO ✓  队列 FIFO ✓  空结构抛 IndexError ✓")


if __name__ == "__main__":
    main()

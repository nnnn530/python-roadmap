r"""day08 栈 / 队列（2026-10-30，50 分钟降级版）

昨天链表是「自己造格子、自己接箭头」；今天这两个结构**底层数据你来挑**，
真正要记的只有一句话：**从哪一头进出**。

    栈 Stack（LIFO，后进先出）—— 只在一头动
        底部 [ 1 | 2 | 3 ] 顶部        push 3 → pop 拿到 3
        场景：撤销 Ctrl+Z、浏览器后退、括号匹配、递归展开

    队列 Queue（FIFO，先进先出）—— 一头进、另一头出
        出 ←[ 1 | 2 | 3 ]← 进          enqueue 3 → dequeue 拿到 1
        场景：任务排队、消息队列、BFS 层序遍历、打印队列

**今天唯一要改的旧习惯**：队列不要用 list 写。
    list.pop(0)   是 O(n) —— 删掉第一个元素后，后面全部元素要整体往前挪一格
    deque.popleft() 是 O(1)  —— 两头都能 O(1) 进出，这才是为队列准备的
栈用 list 就很好（append / pop 都在尾巴上，O(1)），不用换。

复杂度小结（面试必问）：
    栈 / 队列 的 push / pop / 进出 —— 都是 O(1)
    数组 O(1) 随机访问、O(n) 中间插入删除；链表反过来（O(n) 查、已知位置 O(1) 改）

运行：
    cd D:\code\python-roadmap
    python src\day08_stack_queue.py
"""

from collections import deque


class Stack:
    """后进先出。只在一头（尾巴）进出，用 list 就够。"""

    def __init__(self):
        self._data = []          # 前面的下划线 = 约定「自己用，外面别碰」

    def push(self, value):
        """压栈：放到最上面（list 的尾巴就是"最上面"）。一行。"""
        # TODO
        self._data.append(value)

    def pop(self):
        """弹栈：拿走最上面那个并返回它。

        空栈时怎么办？**不要自己写 if + return None**，直接让它抛 IndexError。
        原因：调用方拿到 None 分不清是"弹出来就是 None"还是"栈空了"，
        异常才能把"出错了"和"值就是 None"分开。
        list 的 pop() 空表时本来就抛 IndexError，所以这里一行就够。
        """
        # TODO
        return self._data.pop()

    def peek(self):
        """只看最上面那个，不拿走。同样一行。"""
        # TODO
        return self._data[-1]

    def is_empty(self):
        """空了吗？返回 bool。一行。"""
        # TODO
        return not self._data 

    def __len__(self):
        """昨天学的 dunder，len(stack) 就能用。"""
        # TODO
        return len(self._data)

class Queue:
    """先进先出。一头进（右边）、另一头出（左边），用 deque。"""

    def __init__(self):
        self._data = deque()     # 别写 deque，写 deque() —— 括号 = 造一个

    def enqueue(self, value):
        """入队：排到队尾（deque 的右边，append）。"""
        # TODO
        self._data.append(value)

    def dequeue(self):
        """出队：从队头拿走并返回（deque 的左边，popleft）。

        注意是 popleft 不是 pop —— pop 拿的是右边（队尾），那就成栈了。
        空队列时 popleft 同样抛 IndexError，不用自己处理。
        """
        # TODO
        return self._data.popleft()

    def is_empty(self):
        """一行。"""
        # TODO
        return not self._data

    def __len__(self):
        """一行。"""
        # TODO
        return len(self._data)


if __name__ == "__main__":
    # ---------- 1) 空结构 ----------
    s = Stack()
    assert s.is_empty() is True, "新建的栈应该是空的"
    assert len(s) == 0, f"空栈长度应该是 0，拿到 {len(s)}"

    q = Queue()
    assert q.is_empty() is True, "新建的队列应该是空的"
    assert len(q) == 0, f"空队列长度应该是 0，拿到 {len(q)}"

    # ---------- 2) 单元素：进一个、出一个 ----------
    s.push(1)
    assert s.is_empty() is False, "push 之后不该是空的"
    assert len(s) == 1, f"push 一个后长度应该是 1，拿到 {len(s)}"
    assert s.peek() == 1, f"peek 应该看到 1，拿到 {s.peek()}"
    assert len(s) == 1, "peek 只看不拿，长度不该变"
    assert s.pop() == 1, "pop 应该拿到 1"
    assert s.is_empty() is True, "pop 光之后应该是空的"

    q.enqueue(1)
    assert q.is_empty() is False and len(q) == 1
    assert q.dequeue() == 1, "单元素队列出队应该拿到 1"
    assert q.is_empty() is True and len(q) == 0

    # ---------- 3) 多元素：栈倒着出，队列正着出（这是唯一的区别）----------
    s2 = Stack()
    for v in (1, 2, 3):
        s2.push(v)
    assert len(s2) == 3, f"压了 3 个，长度应该是 3，拿到 {len(s2)}"
    assert s2.peek() == 3, f"最后压进去的是 3，栈顶应该看到 3，拿到 {s2.peek()}"
    assert s2.pop() == 3, "栈：后进先出，第一个弹出的应该是 3"
    assert s2.pop() == 2, "第二个弹出的应该是 2"
    assert s2.pop() == 1, "第三个弹出的应该是 1"
    assert s2.is_empty() is True

    q2 = Queue()
    for v in (1, 2, 3):
        q2.enqueue(v)
    assert len(q2) == 3, f"入队 3 个，长度应该是 3，拿到 {len(q2)}"
    assert q2.dequeue() == 1, "队列：先进先出，第一个出队的应该是 1"
    assert q2.dequeue() == 2, "第二个出队的应该是 2"
    assert q2.dequeue() == 3, "第三个出队的应该是 3"
    assert q2.is_empty() is True

    # 交错进出的经典用例：看顺序对不对
    s3 = Stack()
    s3.push("a")
    s3.push("b")
    assert s3.pop() == "b", "先弹 b（后进的先走）"
    s3.push("c")
    assert s3.pop() == "c", "c 是最后进的，先走"
    assert s3.pop() == "a", "最后剩 a"

    # ---------- 4) 空的时候 pop / dequeue 必须抛 IndexError ----------
    empty_s = Stack()
    try:
        empty_s.pop()
        raise AssertionError("空栈 pop 应该抛 IndexError，但它没抛（是不是你自己 return None 了）")
    except IndexError:
        pass

    empty_q = Queue()
    try:
        empty_q.dequeue()
        raise AssertionError("空队列 dequeue 应该抛 IndexError")
    except IndexError:
        pass

    # ---------- 5) 两条结构互不串味 ----------
    sa, sb = Stack(), Stack()
    sa.push(1)
    assert sb.is_empty() is True, "两个栈共享了数据 —— _data 是不是写成了类属性"

    print(f"栈顶 peek = {s2.peek() if not s2.is_empty() else '空'}")
    print("全部通过（5 组断言）")

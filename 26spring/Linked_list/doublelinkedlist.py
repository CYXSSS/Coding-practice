class DoubleListNode:
    """双链表节点类"""
    def __init__(self, val=0, prev=None, next=None):
        self.val = val    # 节点值
        self.prev = prev  # 前驱节点指针
        self.next = next  # 后继节点指针

class DoublyLinkedList:
    """双链表类（带尾节点，提升尾操作效率）"""
    def __init__(self):
        self.head = None  # 头节点
        self.tail = None  # 尾节点
        self.size = 0     # 链表长度（直接维护，无需遍历计算）

    def is_empty(self):
        """判断链表是否为空"""
        return self.size == 0

    def traverse_forward(self):
        """正向遍历（头→尾），返回值列表"""
        res = []
        cur = self.head
        while cur:
            res.append(cur.val)
            cur = cur.next
        return res

    def traverse_backward(self):
        """反向遍历（尾→头），双链表特有"""
        res = []
        cur = self.tail
        while cur:
            res.append(cur.val)
            cur = cur.prev
        return res

    def add_at_head(self, val):
        """头插法：在表头添加节点"""
        new_node = DoubleListNode(val)
        if self.is_empty():  # 空链表，头、尾节点均为新节点
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head  # 新节点后继指向原头
            self.head.prev = new_node  # 原头前驱指向新节点
            self.head = new_node       # 更新头节点
        self.size += 1

    def add_at_tail(self, val):
        """尾插:在表尾添加节点(双链表高效操作,O(1))"""
        new_node = DoubleListNode(val)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail  # 新节点前驱指向原尾
            self.tail.next = new_node  # 原尾后继指向新节点
            self.tail = new_node       # 更新尾节点
        self.size += 1

    def _get_node(self, index):
        """辅助方法：根据索引找节点（内部使用，优化查找效率）"""
        if index < 0 or index >= self.size:
            raise IndexError("Index out of range")
        # 优化：索引在前半段，从头部找；后半段从尾部找（双向遍历优势）
        if index < self.size // 2:
            cur = self.head
            for _ in range(index):
                cur = cur.next
        else:
            cur = self.tail
            for _ in range(self.size - 1 - index):
                cur = cur.prev
        return cur

    def add_at_index(self, index, val):
        """指定索引插入节点(索引从0开始)"""
        if index < 0 or index > self.size:
            raise IndexError("Index out of range")
        if index == 0:
            self.add_at_head(val)
            return
        if index == self.size:
            self.add_at_tail(val)
            return
        # 找到插入位置的节点（cur），新节点插在cur前面
        cur = self._get_node(index)
        pre = cur.prev
        new_node = DoubleListNode(val, pre, cur)
        pre.next = new_node
        cur.prev = new_node
        self.size += 1

    def remove_by_val(self, val):
        """按值删除节点（删除第一个匹配的）"""
        if self.is_empty():
            raise ValueError("Linked list is empty")
        cur = self.head
        while cur:
            if cur.val == val:
                pre = cur.prev
                nxt = cur.next
                # 情况1：删除的是头节点
                if pre is None:
                    self.head = nxt
                else:
                    pre.next = nxt
                # 情况2：删除的是尾节点
                if nxt is None:
                    self.tail = pre
                else:
                    nxt.prev = pre
                self.size -= 1
                return
            cur = cur.next
        raise ValueError(f"Value {val} not found in linked list")

    def remove_by_index(self, index):
        """按索引删除节点(索引从0开始)"""
        if self.is_empty():
            raise IndexError("Linked list is empty")
        cur = self._get_node(index)  # 直接通过辅助方法找节点
        pre = cur.prev
        nxt = cur.next
        # 维护前驱指针
        if pre:
            pre.next = nxt
        else:
            self.head = nxt  # 无先驱，说明是头节点
        # 维护后继指针
        if nxt:
            nxt.prev = pre
        else:
            self.tail = pre  # 无后继，说明是尾节点
        self.size -= 1

    def find(self, val):
        """按值查找，返回第一个匹配的索引，未找到返回-1"""
        cur = self.head
        index = 0
        while cur:
            if cur.val == val:
                return index
            cur = cur.next
            index += 1
        return -1

# 双链表测试
if __name__ == "__main__":
    dll = DoublyLinkedList()
    dll.add_at_tail(1)
    dll.add_at_head(0)
    dll.add_at_index(2, 2)
    print("双链表正向遍历：", dll.traverse_forward())  # [0,1,2]
    print("双链表反向遍历：", dll.traverse_backward())  # [2,1,0]
    print("链表长度：", dll.size)                     # 3
    print("查找值1的索引:", dll.find(1))             # 1
    dll.remove_by_val(1)
    print("删除值1后正向遍历:", dll.traverse_forward()) # [0,2]
    dll.remove_by_index(1)
    print("删除索引1后反向遍历:", dll.traverse_backward()) # [0]
class ListNode:
    """单链表节点类"""
    def __init__(self, val=0, next=None):
        self.val = val  # 节点存储的值
        self.next = next  # 后继节点指针

class SinglyLinkedList:
    """单链表类"""
    def __init__(self):
        self.head = None  # 头节点，初始为空

    def is_empty(self):
        """判断链表是否为空"""
        return self.head is None

    def length(self):
        """获取链表长度"""
        count = 0
        cur = self.head  # 游标，从表头开始遍历
        while cur:
            count += 1
            cur = cur.next
        return count

    def traverse(self):
        """遍历链表，返回值列表（方便查看）"""
        res = []
        cur = self.head
        while cur:
            res.append(cur.val)
            cur = cur.next
        return res

    def add_at_head(self, val):
        """头插法：在表头添加节点"""
        new_node = ListNode(val)
        new_node.next = self.head  # 新节点指向原头节点
        self.head = new_node  # 头节点更新为新节点

    def add_at_tail(self, val):
        """尾插法：在表尾添加节点"""
        new_node = ListNode(val)
        if self.is_empty():  # 空链表，直接作为头节点
            self.head = new_node
            return
        # 非空链表，遍历到最后一个节点
        cur = self.head
        while cur.next:
            cur = cur.next
        cur.next = new_node  # 最后一个节点指向新节点

    def add_at_index(self, index, val):
        """指定索引插入节点(索引从0开始)"""
        if index < 0 or index > self.length():  # 索引越界判断
            raise IndexError("Index out of range")
        if index == 0:  # 索引0，等价头插
            self.add_at_head(val)
            return
        # 找到索引前一个节点（pre）
        pre = self.head
        for _ in range(index - 1):
            pre = pre.next
        new_node = ListNode(val)
        new_node.next = pre.next  # 新节点指向pre的后继
        pre.next = new_node  # pre指向新节点

    def remove_by_val(self, val):
        """按值删除节点（删除第一个匹配的）"""
        if self.is_empty():
            raise ValueError("Linked list is empty")
        # 特殊情况：头节点是目标节点
        if self.head.val == val:
            self.head = self.head.next
            return
        # 遍历找目标节点的前驱（pre）
        pre, cur = self.head, self.head.next
        while cur:
            if cur.val == val:
                pre.next = cur.next  # pre跳过cur，指向cur的后继
                return
            pre, cur = pre.next, cur.next
        # 遍历结束未找到
        raise ValueError(f"Value {val} not found in linked list")

    def remove_by_index(self, index):
        """按索引删除节点(索引从0开始)"""
        if self.is_empty():
            raise IndexError("Linked list is empty")
        if index < 0 or index >= self.length():
            raise IndexError("Index out of range")
        # 特殊情况：删除头节点
        if index == 0:
            self.head = self.head.next
            return
        # 找到索引前一个节点
        pre = self.head
        for _ in range(index - 1):
            pre = pre.next
        pre.next = pre.next.next  # 跳过目标节点

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

# 单链表测试
if __name__ == "__main__":
    sll = SinglyLinkedList()
    sll.add_at_tail(1)
    sll.add_at_head(0)
    sll.add_at_index(2, 2)
    print("单链表遍历:", sll.traverse())  # [0,1,2]
    print("链表长度:", sll.length())     # 3
    print("查找值2的索引:", sll.find(2)) # 2
    sll.remove_by_val(1)
    print("删除值1后遍历:", sll.traverse()) # [0,2]
    sll.remove_by_index(1)
    print("删除索引1后遍历:", sll.traverse()) # [0]
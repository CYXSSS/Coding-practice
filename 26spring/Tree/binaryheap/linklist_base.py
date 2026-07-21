class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.parent = None

class ReferenceMinHeap:
    def __init__(self):
        self.root = None
        self.size = 0

    def push(self, val):
        new_node = Node(val)
        self.size += 1
        if not self.root:
            self.root = new_node
            return

        # 1. 寻找插入点的父节点
        parent = self._find_parent_of(self.size)
        new_node.parent = parent
        
        # 判定是作为左孩子还是右孩子
        if self.size % 2 == 0:
            parent.left = new_node
        else:
            parent.right = new_node

        # 2. 向上调整 (Sift Up)
        self._sift_up(new_node)

    def pop(self):
        if not self.root:
            return None
        
        root_val = self.root.val
        if self.size == 1:
            self.root = None
            self.size = 0
            return root_val

        # 1. 找到最后一个节点
        last_node = self._get_node_at(self.size)
        
        # 2. 将最后节点的值换到根节点
        self.root.val = last_node.val
        
        # 3. 断开最后节点的引用
        parent = last_node.parent
        if parent.left == last_node:
            parent.left = None
        else:
            parent.right = None
        
        self.size -= 1
        
        # 4. 向下调整 (Sift Down)
        self._sift_down(self.root)
        
        return root_val

    def _find_parent_of(self, index):
        """根据索引找父节点：二进制路径查找法"""
        curr = self.root
        # 转换二进制，跳过最高位和最后一位（因为我们要找父节点）
        path = bin(index)[3:-1] 
        for bit in path:
            curr = curr.left if bit == '0' else curr.right
        return curr

    def _get_node_at(self, index):
        """根据索引找特定节点"""
        curr = self.root
        path = bin(index)[3:]
        for bit in path:
            curr = curr.left if bit == '0' else curr.right
        return curr

    def _sift_up(self, node):
        while node.parent and node.val < node.parent.val:
            # 交换值（在引用结构中，交换值比交换节点指针简单得多）
            node.val, node.parent.val = node.parent.val, node.val
            node = node.parent

    def _sift_down(self, node):
        while True:
            smallest = node
            if node.left and node.left.val < smallest.val:
                smallest = node.left
            if node.right and node.right.val < smallest.val:
                smallest = node.right
            
            if smallest == node:
                break
                
            node.val, smallest.val = smallest.val, node.val
            node = smallest
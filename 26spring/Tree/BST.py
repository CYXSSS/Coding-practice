class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
            return

        current = self.root
        while True:
            if val < current.val:
                if current.left is None:
                    current.left = Node(val)
                    return
                current = current.left
            elif val > current.val:
                if current.right is None:
                    current.right = Node(val)
                    return
                current = current.right
            else:
                # val == current.val 时不插入重复值
                return

    def search(self, val):
        current = self.root
        while current is not None:
            if val == current.val:
                return current
            if val < current.val:
                current = current.left
            else:
                current = current.right
        return None

    def delete_by_successor(self, val):
        def delete_node(node, target):
            if node is None:
                return None
            elif target < node.val:
                node.left = delete_node(node.left, target)
                return node
            elif target > node.val:
                node.right = delete_node(node.right, target)
                return node
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    successor = node.right
                    while successor.left is not None:
                        successor = successor.left
                    node.val = successor.val
                    node.right = delete_node(node.right, successor.val)
                    return node

        self.root = delete_node(self.root, val)

    def delete_by_predecessor(self, val):
        def delete_node(node, target):
            if node is None:
                return None
            elif target < node.val:
                node.left = delete_node(node.left, target)
                return node
            elif target > node.val:
                node.right = delete_node(node.right, target)
                return node
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                else:
                    predecessor = node.left
                    while predecessor.right is not None:
                        predecessor = predecessor.right
                    node.val = predecessor.val
                    node.left = delete_node(node.left, predecessor.val)
                    return node

        self.root = delete_node(self.root, val)

    def delete_by_successor_iterative(self, val):
        parent = None
        current = self.root

        # 1) 先找到要删除的节点及其父节点
        while current is not None and current.val != val:
            parent = current
            if val < current.val:
                current = current.left
            else:
                current = current.right

        if current is None:
            return

        # 2) 如果有两个孩子，转化为删除后继节点（后继至多有一个右孩子）
        if current.left is not None and current.right is not None:
            succ_parent = current
            succ = current.right
            while succ.left is not None:
                succ_parent = succ
                succ = succ.left
            current.val = succ.val
            parent = succ_parent
            current = succ

        # 3) 删除 current（此时最多一个孩子）
        child = current.left if current.left is not None else current.right
        if parent is None:
            self.root = child
        elif parent.left == current:
            parent.left = child
        else:
            parent.right = child

    def inorder(self):
        result = []
        stack = []
        current = self.root

        while stack or current is not None:
            while current is not None:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.val)
            current = current.right

        return result


if __name__ == "__main__":
    bst = BinarySearchTree()
    for num in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        bst.insert(num)

    print("Inorder:", bst.inorder())          # [1, 3, 4, 6, 7, 8, 10, 13, 14]
    print("Search 6:", bst.search(6) is not None)   # True
    print("Search 99:", bst.search(99) is not None) # False

    bst.delete_by_successor(3)
    print("After successor-delete 3:", bst.inorder())   # [1, 4, 6, 7, 8, 10, 13, 14]

    bst2 = BinarySearchTree()
    for num in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        bst2.insert(num)
    bst2.delete_by_predecessor(3)
    print("After predecessor-delete 3:", bst2.inorder())   # [1, 4, 6, 7, 8, 10, 13, 14]

    bst3 = BinarySearchTree()
    for num in [8, 3, 10, 1, 6, 14, 4, 7, 13]:
        bst3.insert(num)
    bst3.delete_by_successor_iterative(3)
    print("After iterative-successor-delete 3:", bst3.inorder())   # [1, 4, 6, 7, 8, 10, 13, 14]

# 时间复杂度（n 为节点数，h 为树高）
# 插入：最佳 O(1)，平均 O(log n)，最坏 O(n)
# 删除：最佳 O(1)，平均 O(log n)，最坏 O(n)
# 查找：最佳 O(1)，平均 O(log n)，最坏 O(n)

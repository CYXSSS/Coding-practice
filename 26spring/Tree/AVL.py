class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        return node.height if node else 0

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        node.height = max(self.get_height(node.left), self.get_height(node.right)) + 1

    def right_rotate(self, y):
        x = y.left
        T = x.right

        x.right = y
        y.left = T

        self.update_height(y)
        self.update_height(x)

        return x

    def left_rotate(self, x):
        y = x.right
        T = y.left

        y.left = x
        x.right = T

        self.update_height(x)
        self.update_height(y)

        return y

    def insert(self, val):
        def _insert(node, val):
            if not node:
                return Node(val)

            if val < node.val:
                node.left = _insert(node.left, val)
            elif val > node.val:
                node.right = _insert(node.right, val)
            else:
                return node

            self.update_height(node)
            balance = self.get_balance(node)

            # LL
            if balance > 1 and val < node.left.val:
                return self.right_rotate(node)
            # RR
            if balance < -1 and val > node.right.val:
                return self.left_rotate(node)
            # LR
            if balance > 1 and val > node.left.val:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            # RL
            if balance < -1 and val < node.right.val:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

            return node

        self.root = _insert(self.root, val)

    def delete(self, val):
        def _delete(node, val):
            if not node:
                return node

            if val < node.val:
                node.left = _delete(node.left, val)
            elif val > node.val:
                node.right = _delete(node.right, val)
            else:
                if not node.left:
                    return node.right
                elif not node.right:
                    return node.left
                else:
                    successor = node.right
                    while successor.left:
                        successor = successor.left
                    node.val = successor.val
                    node.right = _delete(node.right, successor.val)

            if not node:
                return node

            self.update_height(node)
            balance = self.get_balance(node)

            # LL
            if balance > 1 and self.get_balance(node.left) >= 0:
                return self.right_rotate(node)
            # LR
            if balance > 1 and self.get_balance(node.left) < 0:
                node.left = self.left_rotate(node.left)
                return self.right_rotate(node)
            # RR
            if balance < -1 and self.get_balance(node.right) <= 0:
                return self.left_rotate(node)
            # RL
            if balance < -1 and self.get_balance(node.right) > 0:
                node.right = self.right_rotate(node.right)
                return self.left_rotate(node)

            return node

        self.root = _delete(self.root, val)

    def search(self, val):
        current = self.root
        while current:
            if val == current.val:
                return current
            if val < current.val:
                current = current.left
            else:
                current = current.right
        return None

    def inorder(self):
        result = []
        stack = []
        current = self.root
        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.val)
            current = current.right
        return result

    def preorder(self):
        result = []
        stack = [self.root]
        while stack:
            node = stack.pop()
            if node:
                result.append(node.val)
                stack.append(node.right)
                stack.append(node.left)
        return result

    def get_root_height(self):
        return self.get_height(self.root)


if __name__ == "__main__":
    avl = AVLTree()
    for num in [30, 20, 40, 10, 25, 35, 50]:
        avl.insert(num)

    print("Inorder:", avl.inorder())
    print("Preorder:", avl.preorder())
    print("Root height:", avl.get_root_height())

    print("Search 25:", avl.search(25) is not None)
    print("Search 99:", avl.search(99) is not None)

    avl.delete(20)
    print("After delete 20, inorder:", avl.inorder())
    print("After delete 20, root height:", avl.get_root_height())

    avl.delete(30)
    print("After delete 30, inorder:", avl.inorder())
    print("After delete 30, root height:", avl.get_root_height())

# 时间复杂度（n 为节点数）
# 插入：O(log n)，旋转 O(1)
# 删除：O(log n)，旋转 O(1)
# 查找：O(log n)

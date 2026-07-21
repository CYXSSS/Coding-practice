class TreeNode:
    def __init__(self, value):
        self.val = value
        self.left = None
        self.right = None

    # 1. 前序遍历 (Root -> Left -> Right)
    def pre_order(self):
        if not self:
            return []
        return [self.val] + self.pre_order(self.left) + self.pre_order(self.right)

    def pre_order_iterative(self):
        result = []
        stack = [self]
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
        return result

    # 2. 中序遍历 (Left -> Root -> Right)
    def in_order(self):
        if not self:
            return []
        return self.in_order(self.left) + [self.val] + self.in_order(self.right)

    def in_order_iterative(self):
        result = []
        stack = []
        node = self
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append(node.val)
            node = node.right
        return result

    # 3. 后序遍历 (Left -> Right -> Root)
    def post_order(self):
        if not self:
            return []
        return self.post_order(self.left) + self.post_order(self.right) + [self.val]

    def post_order_iterative(self):
        result = []
        stack = [self]
        while stack:
            node = stack.pop()
            result.append(node.val)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
        result.reverse()
        return result

    # 4. 层序遍历 (Level Order Traversal)
    def level_order(self):
        if not self:
            return []
        result = []
        queue = [self]
        while queue:
            current_node = queue.pop(0)
            result.append(current_node.val)
            if current_node.left:
                queue.append(current_node.left)
            if current_node.right:
                queue.append(current_node.right)
        return result
    # T(n) = O(n)
    # S(n) = O(n)
    
    
def count_height(node):
    if node is None:
        return 0
    left_h = count_height(node.left)
    right_h = count_height(node.right)
    return max(left_h, right_h) + 1
# T(n) = O(n)
# S(n) = O(n)
  
def count_nodes(node, result=None):
    if result is None:
        result = {}
    if node is None:
        return 0, result
    left_count, _ = count_nodes(node.left, result)
    right_count, _ = count_nodes(node.right, result)
    total = 1 + left_count + right_count
    result[node.val] = total
    return total, result
# T(n) = O(n)
# S(n) = O(n)

if __name__ == '__main__':
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    root.right.left = TreeNode(6)
    root.right.right = TreeNode(7)
    print(count_height(root))
    total, sizes = count_nodes(root)
    for val, size in sorted(sizes.items()):
        print(f"节点 {val} 的子节点数（含自身）: {size}")
   

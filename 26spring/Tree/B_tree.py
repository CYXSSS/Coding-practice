class BTreeNode:
    def __init__(self, leaf=True):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, t):
        self.root = BTreeNode(leaf=True)
        self.t = t

    def insert(self, key):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
        self.insert_non_full(self.root, key)

    def insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, i):
        t = self.t
        child = parent.children[i]
        new_node = BTreeNode(leaf=child.leaf)

        parent.keys.insert(i, child.keys[t - 1])
        parent.children.insert(i + 1, new_node)

        new_node.keys = child.keys[t:]
        child.keys = child.keys[:t - 1]

        if not child.leaf:
            new_node.children = child.children[t:]
            child.children = child.children[:t]

    def search(self, key, node=None):
        if node is None:
            node = self.root
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and node.keys[i] == key:
            return node, i
        if node.leaf:
            return None, -1
        return self.search(key, node.children[i])

    def delete(self, key):
        if not self.root:
            return
        self.delete_key(self.root, key)
        if len(self.root.keys) == 0 and not self.root.leaf:
            self.root = self.root.children[0]

    def delete_key(self, node, key):
        t = self.t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                node.keys.pop(i)
                return
            return self.delete_internal(node, key, i)
        else:
            if node.leaf:
                return
            flag = (i == len(node.keys))
            if len(node.children[i].keys) < t:
                self.fill(node, i)
            if flag and i > len(node.keys):
                self.delete_key(node.children[i - 1], key)
            else:
                self.delete_key(node.children[i], key)

    def delete_internal(self, node, key, i):
        t = self.t
        if len(node.children[i].keys) >= t:
            pred = self.get_predecessor(node.children[i])
            node.keys[i] = pred
            self.delete_key(node.children[i], pred)
        elif len(node.children[i + 1].keys) >= t:
            succ = self.get_successor(node.children[i + 1])
            node.keys[i] = succ
            self.delete_key(node.children[i + 1], succ)
        else:
            self.merge(node, i)
            self.delete_key(node.children[i], key)

    def get_predecessor(self, node):
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1]

    def get_successor(self, node):
        while not node.leaf:
            node = node.children[0]
        return node.keys[0]

    def fill(self, node, i):
        t = self.t
        if i != 0 and len(node.children[i - 1].keys) >= t:
            self.borrow_from_prev(node, i)
        elif i != len(node.keys) and len(node.children[i + 1].keys) >= t:
            self.borrow_from_next(node, i)
        else:
            if i != len(node.keys):
                self.merge(node, i)
            else:
                self.merge(node, i - 1)

    def borrow_from_prev(self, node, i):
        child = node.children[i]
        sibling = node.children[i - 1]

        child.keys.insert(0, node.keys[i - 1])
        node.keys[i - 1] = sibling.keys.pop()

        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_next(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys[i])
        node.keys[i] = sibling.keys.pop(0)

        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def merge(self, node, i):
        child = node.children[i]
        sibling = node.children[i + 1]

        child.keys.append(node.keys.pop(i))
        child.keys.extend(sibling.keys)

        if not child.leaf:
            child.children.extend(sibling.children)

        node.children.pop(i + 1)

    def inorder(self, node=None, result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.inorder(node.children[i], result)
            result.append(node.keys[i])
        if not node.leaf:
            self.inorder(node.children[-1], result)
        return result

    def level_order(self):
        if not self.root or len(self.root.keys) == 0:
            return []
        result = []
        queue = [self.root]
        while queue:
            node = queue.pop(0)
            result.append(node.keys)
            if not node.leaf:
                for child in node.children:
                    queue.append(child)
        return result


if __name__ == "__main__":
    btree = BTree(t=2)

    print("Inserting: 10, 20, 5, 6, 12, 30, 7, 17")
    for val in [10, 20, 5, 6, 12, 30, 7, 17]:
        btree.insert(val)

    print("Inorder:", btree.inorder())
    print("Level order:")
    for i, level_keys in enumerate(btree.level_order()):
        print(f"  Node {i}: {level_keys}")

    print("\nSearch 6:", btree.search(6)[0] is not None)
    print("Search 99:", btree.search(99)[0] is not None)

    print("\nDeleting 6...")
    btree.delete(6)
    print("Inorder after delete 6:", btree.inorder())

    print("Deleting 20...")
    btree.delete(20)
    print("Inorder after delete 20:", btree.inorder())

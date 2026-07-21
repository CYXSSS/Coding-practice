# ================================================================
# 方法一：链地址法（Chaining with Python list buckets）
# 每个槽位是一个列表,冲突的键值对追加到列表中
# ================================================================
class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTableWithChaining:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return
        self.table[index].append((key, value))

    def get(self, key):
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

    def __str__(self):
        result = []
        for i, slot in enumerate(self.table):
            result.append(f"slot{i}: {slot}")
        return "\n".join(result)


# ================================================================
# 方法二：链表拉链法（Separate Chaining with Linked List Nodes）
# 每个槽位是一个单向链表的头节点
# ================================================================
class HashTableWithLinkedListChaining:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                current.value = value
                return
            current = current.next
        new_node = ListNode(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.count += 1

    def get(self, key):
        index = self._hash(key)
        current = self.table[index]
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        return None

    def delete(self, key):
        index = self._hash(key)
        head = self.table[index]
        if head is None:
            return False
        if head.key == key:
            self.table[index] = head.next
            self.count -= 1
            return True
        prev = head
        current = head.next
        while current is not None:
            if current.key == key:
                prev.next = current.next
                self.count -= 1
                return True
            prev = current
            current = current.next
        return False

    def __str__(self):
        result = []
        for i in range(self.size):
            chain = []
            current = self.table[i]
            while current is not None:
                chain.append(f"({current.key}:{current.value})")
                current = current.next
            result.append(f"slot{i}: {' -> '.join(chain) if chain else 'None'}")
        return "\n".join(result)


# ================================================================
# 方法三：线性探测（Linear Probing）
# 冲突时依次检查下一个槽位: index = (hash + i) % size
# ================================================================
class HashTableWithLinearProbing:
    _TOMBSTONE = object()

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        if self.count >= self.size:
            raise Exception("hash table full")
        index = self._hash(key)
        first_tombstone = -1
        for i in range(self.size):
            probe_idx = (index + i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                target = probe_idx if first_tombstone == -1 else first_tombstone
                self.table[target] = (key, value)
                self.count += 1
                return
            if slot is self._TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = probe_idx
            elif slot[0] == key:
                self.table[probe_idx] = (key, value)
                return
        if first_tombstone != -1:
            self.table[first_tombstone] = (key, value)
            self.count += 1

    def get(self, key):
        index = self._hash(key)
        for i in range(self.size):
            probe_idx = (index + i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return None
            if slot is not self._TOMBSTONE and slot[0] == key:
                return slot[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        for i in range(self.size):
            probe_idx = (index + i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return False
            if slot is not self._TOMBSTONE and slot[0] == key:
                self.table[probe_idx] = self._TOMBSTONE
                self.count -= 1
                return True
        return False

    def __str__(self):
        result = []
        for i, slot in enumerate(self.table):
            if slot is None:
                result.append(f"slot{i}: None")
            elif slot is self._TOMBSTONE:
                result.append(f"slot{i}: TOMBSTONE")
            else:
                result.append(f"slot{i}: {slot}")
        return "\n".join(result)


# ================================================================
# 方法四：二次探测（Quadratic Probing）
# 冲突时跳跃距离递增: index = (hash + i^2) % size
# ================================================================
class HashTableWithQuadraticProbing:
    _TOMBSTONE = object()

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        if self.count >= self.size:
            raise Exception("hash table full")
        index = self._hash(key)
        first_tombstone = -1
        for i in range(self.size):
            probe_idx = (index + i * i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                target = probe_idx if first_tombstone == -1 else first_tombstone
                self.table[target] = (key, value)
                self.count += 1
                return
            if slot is self._TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = probe_idx
            elif slot[0] == key:
                self.table[probe_idx] = (key, value)
                return
        if first_tombstone != -1:
            self.table[first_tombstone] = (key, value)
            self.count += 1

    def get(self, key):
        index = self._hash(key)
        for i in range(self.size):
            probe_idx = (index + i * i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return None
            if slot is not self._TOMBSTONE and slot[0] == key:
                return slot[1]
        return None

    def delete(self, key):
        index = self._hash(key)
        for i in range(self.size):
            probe_idx = (index + i * i) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return False
            if slot is not self._TOMBSTONE and slot[0] == key:
                self.table[probe_idx] = self._TOMBSTONE
                self.count -= 1
                return True
        return False

    def __str__(self):
        result = []
        for i, slot in enumerate(self.table):
            if slot is None:
                result.append(f"slot{i}: None")
            elif slot is self._TOMBSTONE:
                result.append(f"slot{i}: TOMBSTONE")
            else:
                result.append(f"slot{i}: {slot}")
        return "\n".join(result)


# ================================================================
# 方法五：双重哈希（Double Hashing）
# 用第二个哈希函数决定步长: index = (hash1 + i * hash2) % size
# hash2 永不为 0（用 (hash % (size-1)) + 1 保证）
# ================================================================
class HashTableWithDoubleHashing:
    _TOMBSTONE = object()

    def __init__(self, size=10):
        self.size = size
        self.table = [None] * self.size
        self.count = 0

    def _hash1(self, key):
        return hash(key) % self.size

    def _hash2(self, key):
        h = hash(key)
        return (h % (self.size - 1)) + 1

    def insert(self, key, value):
        if self.count >= self.size:
            raise Exception("hash table full")
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        first_tombstone = -1
        for i in range(self.size):
            probe_idx = (h1 + i * h2) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                target = probe_idx if first_tombstone == -1 else first_tombstone
                self.table[target] = (key, value)
                self.count += 1
                return
            if slot is self._TOMBSTONE:
                if first_tombstone == -1:
                    first_tombstone = probe_idx
            elif slot[0] == key:
                self.table[probe_idx] = (key, value)
                return
        if first_tombstone != -1:
            self.table[first_tombstone] = (key, value)
            self.count += 1

    def get(self, key):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        for i in range(self.size):
            probe_idx = (h1 + i * h2) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return None
            if slot is not self._TOMBSTONE and slot[0] == key:
                return slot[1]
        return None

    def delete(self, key):
        h1 = self._hash1(key)
        h2 = self._hash2(key)
        for i in range(self.size):
            probe_idx = (h1 + i * h2) % self.size
            slot = self.table[probe_idx]
            if slot is None:
                return False
            if slot is not self._TOMBSTONE and slot[0] == key:
                self.table[probe_idx] = self._TOMBSTONE
                self.count -= 1
                return True
        return False

    def __str__(self):
        result = []
        for i, slot in enumerate(self.table):
            if slot is None:
                result.append(f"slot{i}: None")
            elif slot is self._TOMBSTONE:
                result.append(f"slot{i}: TOMBSTONE")
            else:
                result.append(f"slot{i}: {slot}")
        return "\n".join(result)


# ================================================================
# 时间复杂度总结（n = 元素数量, m = 表大小, load factor a = n/m）
# 适用于 insert / get / delete 三个操作
# ================================================================
#  方法                   | 最好   | 平均        | 最坏
# -----------------------|--------|-------------|------
#  链地址法               | O(1)  | O(1 + a)   | O(n)
#  链表拉链法             | O(1)  | O(1 + a)   | O(n)
#  线性探测               | O(1)  | O(1/(1-a)) | O(m)
#  二次探测               | O(1)  | O(1/(1-a)) | O(m)
#  双重哈希               | O(1)  | O(1/(1-a)) | O(m)

# insert/get/delete 三者复杂度相同,因为它们都遵循同一流程:
#   step 1: hash(key) → 确定起始槽位 index  (O(1))
#   step 2: 在槽位/bucket 中查找目标 key    (差异在此)
#   step 3: 执行具体操作(写/读/删)           (O(1))
# 主要开销都在 step 2——沿着 probing 链或链表查找目标 key
#
#  最好: 起始槽位直接命中(无冲突), 一步到位
#  平均: 链地址法→遍历约α长度的链表; 开放寻址→取决于负载因子α
#  最坏: 链地址法→所有键哈希到同一槽位(退化为O(n)链表)
#        开放寻址→探测整个表(退化为O(m)全表扫描)

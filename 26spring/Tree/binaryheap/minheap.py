class MinHeapPriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, val):
        """将元素加入堆中，并向上调整 (Sift Up)"""
        self.heap.append(val)
        self._sift_up(len(self.heap) - 1)
        # T(n) = O(log n)

    def pop(self):
        """弹出堆顶（最小值），并将末尾元素移至堆顶进行向下调整 (Sift Down)"""
        if not self.heap:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        
        root = self.heap[0]
        # 将最后一个元素换到堆顶，然后进行调整
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root
        # T(n) = O(log n)

    def _sift_up(self, index):
        parent = (index - 1) // 2
        # 如果子节点比父节点小，则交换
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._sift_up(parent)

    def _sift_down(self, index):
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index

        # 找出父、左、右三个节点中最小的一个
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        # 如果最小值不是父节点，则交换并继续向下调整
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._sift_down(smallest)

    def peek(self):
        return self.heap[0] if self.heap else None


# ================================================================
# 时间复杂度总结（n = 堆中元素数量）
# ================================================================
#  操作     | 最好        | 平均        | 最坏
# ----------|-------------|-------------|--------
#  push     | O(1)        | O(log n)    | O(log n)
#  pop      | O(1)        | O(log n)    | O(log n)
#  peek     | O(1)        | O(1)        | O(1)
#
#  push 最好: 新元素不小于父节点,sift_up 只比较一次就不走了
#  push 最坏: sift_up 一路走到根,走完整棵树的深度 log n
#  pop 最好: 堆只有一个元素,不需要 sift_down
#  pop 最坏: sift_down 一路走到叶子,走完整棵树的深度 log n
#  peek: 直接读 self.heap[0],恒常 O(1)
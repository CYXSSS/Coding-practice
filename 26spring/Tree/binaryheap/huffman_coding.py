class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

def build_huffman_tree_manual(text):
    # --- 1. 手动统计频率 ---
    freq_dict = {}
    for char in text:
        if char in freq_dict:
            freq_dict[char] += 1
        else:
            freq_dict[char] = 1
    
    # --- 2. 将字典转化为节点列表 ---
    nodes = []
    for char, freq in freq_dict.items():
        nodes.append(Node(char, freq))
    
    # --- 3. 手动模拟优先级队列 ---
    # 只要列表里还有超过 1 个节点，就继续合并
    while len(nodes) > 1:
        # 按照频率从小到大排序
        # 这样列表的前两个元素永远是频率最小的
        nodes.sort(key=lambda x: x.freq)
        
        # 取出最小的两个
        left_node = nodes.pop(0)
        right_node = nodes.pop(0)
        
        # 合并并放回列表
        parent = Node(None, left_node.freq + right_node.freq)
        parent.left = left_node
        parent.right = right_node
        nodes.append(parent)
    
    return nodes[0]  # 最后剩下的就是根节点

def get_codes(node, current_code="", codes={}):
    if not node:
        return
    if node.char is not None:
        codes[node.char] = current_code
    get_codes(node.left, current_code + "0", codes)
    get_codes(node.right, current_code + "1", codes)
    return codes

# 测试          
text = "BANANA"
root = build_huffman_tree_manual(text)
codes = get_codes(root, "", {})

print(f"字符编码结果: {codes}")

# 时间复杂度（n = 文本长度，k = 不同字符数）
# 频率统计：O(n)
# 构建哈夫曼树（手动排序版本）：O(k² log k)，每轮都对 nodes 排序
#   若使用最小堆构建：O(k log k)，每轮 extract_min/insert 均为 O(log k)
# 生成编码（遍历树）：O(k)
# 总体：O(n + k² log k)，若用堆则为 O(n + k log k)

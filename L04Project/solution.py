"""
UFUG2602 Project Test C: Intelligent Document Compression and Full-Text Retrieval System

Student Name: 陈彦旭_______________
Student ID:   50032493_______________

Instructions:
  1. Implement all sections marked with TODO.
  2. Do NOT modify the parse_test_file() or main() functions.
  3. Do NOT use banned built-ins (see project spec for details).
  4. Run:  python3 solution.py <test_file> [output_file]
"""

"""
IMPORTANT:
If you use any AI tools (e.g., ChatGPT, Copilot, Cursor, Claude Code, etc.), you must include all prompts used as comments HERE.
"""

import sys
import re  # allowed for tokenization ONLY, NOT for pattern matching


# ================================================================
# Tokenization (provided — do NOT modify)
# ================================================================

def tokenize(text):
    """Split text into lowercase words (maximal sequences of English letters)."""
    return re.findall(r'[a-zA-Z]+', text.lower())


# ================================================================
# Data Structures — TODO: implement
# ================================================================

class MinHeap:
    """
    A min-heap (priority queue) based on a list.
    Elements must support < comparison.
    """
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def _sift_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self._data[idx] < self._data[parent]:
                self._data[idx], self._data[parent] = self._data[parent], self._data[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        n = len(self._data)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and self._data[left] < self._data[smallest]:
                smallest = left
            if right < n and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest != idx:
                self._data[idx], self._data[smallest] = self._data[smallest], self._data[idx]
                idx = smallest
            else:
                break

    def insert(self, item):
        # TODO: append item and sift up
        self._data.append(item)
        self._sift_up(len(self._data) - 1)

    def extract_min(self):
        # TODO: remove and return the minimum element
        if self.is_empty():
            return None
        min_item = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return min_item

    def peek(self):
        # TODO: return the minimum element without removing
        if self.is_empty():
            return None
        return self._data[0]

    def replace_min(self, item):
        # TODO: replace root with item and sift down
        if self.is_empty():
            self._data.append(item)
            return
        self._data[0] = item
        self._sift_down(0)


class HuffmanNode:
    """
    A node in the Huffman tree.
    - char: the character (None for internal nodes)
    - freq: the frequency
    - left, right: child nodes
    """
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        """
        Comparison for heap ordering.
        Tie-breaking rule (R4):
          - lower frequency first
          - leaf before internal node
          - among leaves, smaller char (ASCII) first
        """
        if self.freq != other.freq:
            return self.freq < other.freq
        if self.is_leaf() != other.is_leaf():
            return self.is_leaf()  # leaf nodes should appear first
        if self.is_leaf():
            return self.char < other.char  # smaller char ASCII value first
        return False  # no tie-breaking needed for internal nodes

    def is_leaf(self):
        return self.left is None and self.right is None


class HashTable:
    """
    A hash table with chaining for collision handling.
    Must support: put(key, value), get(key, default), items(), load_factor().
    """
    def __init__(self, size=997):
        self._size = size
        self._buckets = [[] for _ in range(size)]
        self._num_entries = 0

    def _hash(self, key):
        # TODO: implement a hash function for string keys
        # Hint: polynomial rolling hash  h = sum(ord(c) * 31^i) mod size
        h = 0
        for c in key:
            h = (h * 31 + ord(c)) % self._size
        return h

    def put(self, key, value):
        # TODO: insert or update key-value pair
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._num_entries += 1

    def get(self, key, default=None):
        # TODO: return value for key, or default if not found
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def items(self):
        # TODO: return a list of all (key, value) pairs
        result = []
        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair)
        return result

    def load_factor(self):
        return self._num_entries / self._size


# ================================================================
# Algorithms — TODO: implement
# ================================================================

def merge_sort(arr, key_func=None):
    """
    Stable merge sort.
    key_func: optional function that maps each element to a comparison key.
    Returns a new sorted list.
    """
    if key_func is None:
        key_func = lambda x: x

    # TODO: implement merge sort
    if len(arr) <= 1:
        return list(arr)

    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)

    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key_func(left[i]) <= key_func(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def build_lps(pattern):
    """
    Build the LPS (Longest Proper Prefix which is also Suffix) array for KMP.
    Returns a list of integers of length len(pattern).
    """
    # TODO: implement LPS construction
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps


def kmp_search(text, pattern):
    """
    Find all occurrences of pattern in text using KMP algorithm.
    Returns a list of starting positions (0-indexed).
    """
    # TODO: implement KMP matching
    m = len(pattern)
    if m == 0:
        return []
    lps = build_lps(pattern)
    n = len(text)
    i = j = 0
    positions = []
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            positions.append(i - j)
            j = lps[j - 1]
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return positions


# ================================================================
# Operation A: Huffman Compression & Decompression (30 pts)
# ================================================================

def run_operation_a(doc_content):
    """
    Given the content string of a document, perform Huffman encoding and decoding.

    Output format (return list of strings):
      === Operation A: Huffman Compression & Decompression ===
      Code Table:
        <char>: <binary_code>       (sorted by character)
      Original Length: <n> characters (<n*8> bits)
      Encoded Length: <m> bits
      Compression Ratio: <ratio>%
      Decompression Verified: True/False
    """
    output = []
    output.append("=== Operation A: Huffman Compression & Decompression ===")

    # TODO: 1. Count character frequencies
    freq = {}
    for ch in doc_content:
        freq[ch] = freq.get(ch, 0) + 1

    # TODO: 2. Build Huffman tree using MinHeap
    heap = MinHeap()
    for ch, f in freq.items():
        heap.insert(HuffmanNode(char=ch, freq=f))

    while len(heap) > 1:
        left = heap.extract_min()
        right = heap.extract_min()
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heap.insert(merged)

    root = heap.extract_min() if not heap.is_empty() else None

    # TODO: 3. Generate code table (traverse tree)
    code_table = {}

    def traverse(node, code):
        if node is None:
            return
        if node.is_leaf():
            code_table[node.char] = code
            return
        traverse(node.left, code + '0')
        traverse(node.right, code + '1')

    if root is not None:
        traverse(root, '')

    # TODO: 4. Encode content to binary string
    encoded = ''.join(code_table[ch] for ch in doc_content)

    # TODO: 5. Decode binary string back to original
    decoded = ''
    if root is not None:
        if root.is_leaf():
            decoded = root.char * len(encoded)
        else:
            node = root
            for bit in encoded:
                node = node.left if bit == '0' else node.right
                if node.is_leaf():
                    decoded += node.char
                    node = root

    # TODO: 6. Format output
    output.append("Code Table:")
    for ch in sorted(code_table.keys()):
        if ch == ' ':
            display = "' '"
        else:
            display = ch
        output.append(f"  {display}: {code_table[ch]}")

    orig_len = len(doc_content)
    enc_len = len(encoded)
    ratio = enc_len / (orig_len * 8) * 100
    output.append(f"Original Length: {orig_len} characters ({orig_len * 8} bits)")
    output.append(f"Encoded Length: {enc_len} bits")
    output.append(f"Compression Ratio: {ratio:.2f}%")
    output.append(f"Decompression Verified: {decoded == doc_content}")

    return output


# ================================================================
# Operation B: Top-K Frequent Words (30 pts)
# ================================================================

class _WordEntry:
    """Wrapper for Top-K selection where 'smaller' means 'worse'."""
    __slots__ = ("word", "freq")

    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __lt__(self, other):
        if self.freq != other.freq:
            return self.freq < other.freq
        if len(self.word) != len(other.word):
            return len(self.word) < len(other.word)
        return self.word > other.word


def run_operation_b(documents, k):
    """
    Find the K most frequent words across all documents.
    Ranking rule: descending frequency; ties broken by longer word first, then alphabetically ascending.
    Use HashTable for counting and MinHeap for Top-K selection.

    Output format (return list of strings):
      === Operation B: Top-<K> Frequent Words (Longer-Word Tie) ===
        1. <word>: <freq>
        2. <word>: <freq>
        ...
      Load Factor: <float>
    """
    output = []
    output.append(f"=== Operation B: Top-{k} Frequent Words (Longer-Word Tie) ===")

    # TODO: 1. Tokenize all documents, count word frequencies with HashTable
    table = HashTable()
    for _, _, content in documents:
        for word in tokenize(content):
            table.put(word, table.get(word, 0) + 1)

    # TODO: 2. Use MinHeap to select Top-K according to the ranking rule
    heap = MinHeap()
    for word, freq in table.items():
        heap.insert(_WordEntry(word, freq))
        if len(heap) > k:
            heap.extract_min()

    top_entries = []
    while not heap.is_empty():
        top_entries.append(heap.extract_min())

    # TODO: 3. Output results in this order: descending frequency; ties broken by longer word first, then alphabetically ascending
    top_entries = merge_sort(
        top_entries,
        key_func=lambda e: (-e.freq, -len(e.word), e.word),
    )

    # TODO: 4. Format output
    rank = 1
    for e in top_entries:
        output.append(f"  {rank}. {e.word}: {e.freq}")
        rank += 1

    output.append(f"Load Factor: {table.load_factor():.4f}")

    return output


# ================================================================
# Operation C: KMP Pattern Search + Merge Sort (40 pts)
# ================================================================

def run_operation_c(documents, patterns):
    """
    For each pattern, find all matching documents via KMP, sort results via merge sort.

    Output format (return list of strings):
      === Operation C: KMP Pattern Search ===
      Pattern: "<pattern>"
      LPS Array: [...]
        Doc <id>: <count> occurrence(s) at positions [<pos1>, <pos2>, ...]
        ...
      (blank line between patterns)
    """
    output = []
    output.append("=== Operation C: KMP Pattern Search ===")

    # TODO: For each pattern:
    for pi, pattern in enumerate(patterns):
        if pi > 0:
            output.append("")

        output.append(f'Pattern: "{pattern}"')
        lps = build_lps(pattern.lower())
        output.append(f"LPS Array: {lps}")

        # For each pattern, collect matching documents
        results = []
        for did, _, content in documents:
            positions = kmp_search(content.lower(), pattern.lower())
            if positions:
                results.append((did, positions))

        # Sort: descending count, then ascending first position, then ascending doc id
        results = merge_sort(
            results,
            key_func=lambda r: (-len(r[1]), r[1][0], r[0]),
        )

        for did, positions in results:
            pos_str = ", ".join(str(p) for p in positions)
            output.append(f"  Doc {did}: {len(positions)} occurrence(s) at positions [{pos_str}]")

    return output


# ================================================================
# I/O Handling (provided — do NOT modify)
# ================================================================

def parse_test_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f]

    idx = 0
    num_docs = int(lines[idx]); idx += 1
    documents = []
    for _ in range(num_docs):
        parts = lines[idx].split('|', 2)
        documents.append((int(parts[0]), parts[1], parts[2]))
        idx += 1

    huffman_doc_id = None
    topk_value = None
    kmp_patterns = []

    while idx < len(lines):
        line = lines[idx].strip(); idx += 1
        if not line:
            continue
        if line.startswith("HUFFMAN "):
            huffman_doc_id = int(line.split()[1])
        elif line.startswith("TOPK "):
            topk_value = int(line.split()[1])
        elif line.startswith("KMP_PATTERN "):
            kmp_patterns.append(line[len("KMP_PATTERN "):])

    return documents, huffman_doc_id, topk_value, kmp_patterns


def main():
    if len(sys.argv) < 2:
        print("Usage: python solution.py <test_file> [output_file]")
        sys.exit(1)

    documents, huffman_id, topk_k, kmp_patterns = parse_test_file(sys.argv[1])
    out = []

    for did, _, content in documents:
        if did == huffman_id:
            out.append(f"Document ID: {huffman_id}")
            out.extend(run_operation_a(content))
            break
    out.append("")

    out.extend(run_operation_b(documents, topk_k))
    out.append("")

    out.extend(run_operation_c(documents, kmp_patterns))

    text = "\n".join(out)
    if len(sys.argv) > 2:
        with open(sys.argv[2], 'w', encoding='utf-8') as f:
            f.write(text + "\n")
        print(f"Output written to {sys.argv[2]}")
    else:
        print(text)


if __name__ == "__main__":
    main()

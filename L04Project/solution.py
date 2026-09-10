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

    def insert(self, item):
        # TODO: append item and sift up
        
    def extract_min(self):
        # TODO: remove and return the minimum element
        
    def peek(self):
        # TODO: return the minimum element without removing

    def replace_min(self, item):
        # TODO: replace root with item and sift down      

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
    

    def put(self, key, value):
        # TODO: insert or update key-value pair
        

    def get(self, key, default=None):
        # TODO: return value for key, or default if not found

    def items(self):
        # TODO: return a list of all (key, value) pairs
        
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
    # TODO: implement merge sort
    


def build_lps(pattern):
    """
    Build the LPS (Longest Proper Prefix which is also Suffix) array for KMP.
    Returns a list of integers of length len(pattern).
    """
    # TODO: implement LPS construction
    


def kmp_search(text, pattern):
    """
    Find all occurrences of pattern in text using KMP algorithm.
    Returns a list of starting positions (0-indexed).
    """
    # TODO: implement KMP matching
    


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
    
    # TODO: 2. Build Huffman tree using MinHeap

    # TODO: 3. Generate code table (traverse tree)

    # TODO: 4. Encode content to binary string
    
    # TODO: 5. Decode binary string back to original
    
    # TODO: 6. Format output

    


# ================================================================
# Operation B: Top-K Frequent Words (30 pts)
# ================================================================

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
    
    # TODO: 2. Use MinHeap to select Top-K according to the ranking rule
    
    # TODO: 3. Output results in this order: descending frequency; ties broken by longer word first, then alphabetically ascending
    
    # TODO: 4. Format output
    




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

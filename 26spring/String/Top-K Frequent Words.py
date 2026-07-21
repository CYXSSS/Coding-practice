def top_k_frequent_no_libs(words, k):
    counts = {}
    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
            
    unique_words = list(counts.keys())
    unique_words.sort(key=lambda w: (-counts[w], w))
    return unique_words[:k]

# 测试
word_list = ["apple", "banana", "apple", "orange", "banana", "apple", "cherry", "cherry"]
# apple: 3, banana: 2, cherry: 2, orange: 1
print(f"Top 3: {top_k_frequent_no_libs(word_list, 3)}") 
# 输出: ['apple', 'banana', 'cherry'] (banana 和 cherry 频率相同，b 排在 c 前面)


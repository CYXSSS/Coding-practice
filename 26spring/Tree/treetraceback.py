import sys

def solve():
    # 读取输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    post_order = list(map(int, input_data[1:n+1]))
    in_order = list(map(int, input_data[n+1:2*n+1]))
    
    pre_order = []

    def build(post_sub, in_sub):
        if not post_sub or not in_sub:
            return
        
        # 1. 后序遍历的最后一个是根
        root_val = post_sub[-1]
        pre_order.append(root_val) # 前序：先记下根
        
        # 2. 在中序遍历中找到根的位置，以此划分左右子树
        root_idx_in = in_sub.index(root_val)
        
        # 左子树的节点数量
        left_size = root_idx_in
        
        # 3. 切分出左、右子树的中序和后序序列
        # 中序：[左子树, 根, 右子树]
        left_in = in_sub[:root_idx_in]
        right_in = in_sub[root_idx_in+1:]
        
        # 后序：[左子树, 右子树, 根]
        left_post = post_sub[:left_size]
        right_post = post_sub[left_size:-1]
        
        # 4. 递归处理（前序：先左后右）
        build(left_post, left_in)
        build(right_post, right_in)

    build(post_order, in_order)
    
    # 按照格式输出
    print("Preorder:", " ".join(map(str, pre_order)))

if __name__ == "__main__":
    solve()
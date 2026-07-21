import sys

def solve_maze():
    # 1. 读取所有输入数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    ptr = 0
    # 迷宫大小
    n = int(input_data[ptr])
    ptr += 1
    
    # 迷宫地图 (1为墙, 0为路)
    maze = []
    for i in range(n):
        maze.append([int(x) for x in input_data[ptr : ptr + n]])
        ptr += n
    
    # 入口和出口坐标
    start_x, start_y = int(input_data[ptr]), int(input_data[ptr+1])
    end_x, end_y = int(input_data[ptr+2]), int(input_data[ptr+3])
    
    # 2. 定义 8 个方向（正东开始，顺时针）
    # (dx, dy): 东, 东南, 南, 西南, 西, 西北, 北, 东北
    dx = [0, 1, 1, 1, 0, -1, -1, -1]
    dy = [1, 1, 0, -1, -1, -1, 0, 1]
    
    # 3. 初始化栈和访问标记
    # 栈元素格式: [x, y, direction_index]
    stack = [[start_x, start_y, 0]]
    visited = [[False for _ in range(n)] for _ in range(n)]
    visited[start_x][start_y] = True
    
    found = False
    
    # 4. 回溯算法主循环
    while stack:
        curr = stack[-1] # 查看栈顶
        x, y, di = curr[0], curr[1], curr[2]
        
        # 检查是否到达出口
        if x == end_x and y == end_y:
            found = True
            break
        
        moved = False
        # 尝试从当前的 di 开始探索 8 个方向
        for d in range(di, 8):
            nx, ny = x + dx[d], y + dy[d]
            
            # 更新当前格子下一次尝试的方向索引
            stack[-1][2] = d + 1 
            
            # 判断合法性：边界内、是通路、未访问过
            if 0 <= nx < n and 0 <= ny < n and maze[nx][ny] == 0 and not visited[nx][ny]:
                visited[nx][ny] = True
                stack.append([nx, ny, 0])
                moved = True
                break
        
        # 如果 8 个方向都走不通，回溯
        if not moved:
            stack.pop()
            
    # 5. 格式化输出路径（反向输出）
    if found:
        path_str = []
        while stack:
            node = stack.pop()
            path_str.append(f"{node[0]} {node[1]}")
        print(";".join(path_str) + ";")

if __name__ == "__main__":
    solve_maze()
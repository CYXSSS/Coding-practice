def maze_path(x, y, m, n):
    if x == m or y == n:    ### Out of bounds, no path
        return []
    elif x == m - 1 and y == n - 1: ### Base case: reached destination
        return [[(x, y)]]
    else:   ### Recursive case: explore paths by moving right and down
        paths = []
        for path in maze_path(x + 1, y, m, n):  ### Move down
            paths.append([(x, y)] + path)
        for path in maze_path(x, y + 1, m, n):  ### Move right
            paths.append([(x, y)] + path)
        return paths

m, n = 3, 3
paths = maze_path(0, 0, m, n)
for path in paths:
    print(path)

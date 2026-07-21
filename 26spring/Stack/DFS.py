n, e = map(int, input().split())
graph = [[] for _ in range(n)]
for _ in range(e):
    u, v = map(int, input().split())
    graph[u].append(v)
for i in range(n):
    graph[i].sort()
visited = [False] * n
result = []
def dfs(node):
    visited[node] = True
    result.append(node)
    for neighbor in graph[node]:
        if not visited[neighbor]:
            dfs(neighbor)
for i in range(n):
    if not visited[i]:
        dfs(i)
for node in result:
    print(node, end = ' ')

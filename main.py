vis = [False] * 100000
gr = [] * 100000
def dfs(j):
    vis[j] = True
    for i in gr[j]:
        if not vis[i]:
            dfs(i)

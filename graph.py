from collections import deque
import sys
import heapq
import pygame
class Graph(object):
    def __init__(self, graph, n):
        if isinstance(graph, Graph):
            "Проверка, является ли данный полученные данные классом Graph"
            self.graph = graph
            self.n = n
        elif isinstance(graph, dict):
            "Проверка, является ли данный полученные данные списком смежности"
            self.graph = graph
            self.n = n
        elif isinstance(graph[0], tuple):
            "Проверка, является ли данный полученные данные списком ребер"
            self.n = n
            b = {}
            for i in range(self.n):
                a = []
                for j in graph:
                    if j[0] == i:
                        a.append(j[0])
                b[i] = set(a)
            self.graph = b
        else:
            "Проверка, является ли данный полученные данные матрицей смежности"
            self.n = n
            b = {}
            for i in range(self.n):
                a = []
                for j in range(self.n):
                    if graph[i][j] != 0:
                        a.append(j)
                b[i] = set(a)
            self.graph = b


    def value(self, a, b):
        "Возвращает значение ребра между двумя вершинами."
        return self.graph[a][b]

    def dfs(self, j):
        "Реализует обход графа в глубину"
        vis[j] = True
        for i in self.graph[j]:
            if not vis[i]:
                dfs(i)

    def bfs(self, start):
        "Реализует обхода графа в ширину"
        vis = set()
        q = deque([start])

        while q:
            v = q.popleft()
            if v not in vis:
                vis.add(v)
                q.extend(self.graph[v] - vis)

    def dij(self, start):
        "Реализует алгоритм Дейкстры"
        dist[s] = 0
        q = [(0, start)]
        while q:
            b, a = heapq.heappop(q)
            if b > dist[a]:
                continue
            for u, w in self.graph[a].items():
                distance = b + w
                if distance < dist[u]:
                    dist[u] = distance
                    heapq.heappush(q, (distance, u))

        return dist

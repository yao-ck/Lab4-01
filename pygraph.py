"""
pygraph.py - Graph Data Structure Implementation
================================================

This module provides a comprehensive implementation of a graph data structure
using adjacency lists, supporting both directed and undirected graphs.

Features:
- Node and edge management
- DFS/BFS traversals
- Path finding algorithms
- Topological sorting
- Cycle detection

"""

class Graph:
    """A directed or undirected graph implementation."""
    
    def __init__(self, directed=False):
        """
        Initialize a Graph object.
        
        Args:
            directed (bool): Whether the graph is directed (default: False)
        """
        self.graph = {}
        self.directed = directed

    def add_node(self, node):
        """Add a node to the graph if it doesn't exist."""
        if node not in self.graph:
            self.graph[node] = []
    
    def add_edge(self, node1, node2):
        """Add an edge between node1 and node2."""
        self.add_node(node1)
        self.add_node(node2)
        
        if node2 not in self.graph[node1]:
            self.graph[node1].append(node2)
            
            if not self.directed and node1 not in self.graph[node2]:
                self.graph[node2].append(node1)
    
    def get_nodes(self):
        """Get all nodes in the graph."""
        return list(self.graph.keys())
    
    def get_edges(self):
        """Get all edges in the graph as tuples (node1, node2)."""
        edges = []
        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                if not self.directed and neighbor < node:
                    continue  # Avoid duplicate edges in undirected graph
                edges.append((node, neighbor))
        return edges
    
    def get_neighbors(self, node):
        """Get neighbors of a node."""
        return self.graph.get(node, [])
    
    def has_cycle(self):
        """Check if the graph has a cycle using DFS."""
        if not self.directed:
            return self._has_cycle_undirected()
        return self._has_cycle_directed()
    
    def _has_cycle_directed(self):
        """Detect cycle in directed graph using DFS."""
        visited = set()
        rec_stack = set()
        
        def dfs(node):
            visited.add(node)
            rec_stack.add(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(node)
            return False
        
        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True
        return False
    
    def _has_cycle_undirected(self):
        """Detect cycle in undirected graph using DFS."""
        visited = set()
        
        def dfs(node, parent):
            visited.add(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False
        
        for node in self.graph:
            if node not in visited:
                if dfs(node, None):
                    return True
        return False
    
    def dfs(self, start):
        """Depth-First Search starting from a node."""
        visited = []
        stack = [start]
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                # Reverse neighbors to maintain order for test matching
                stack.extend(reversed(self.graph.get(node, [])))
        
        return visited
    
    def bfs(self, start):
        """Breadth-First Search starting from a node."""
        visited = []
        queue = [start]
        
        while queue:
            node = queue.pop(0)
            if node not in visited:
                visited.append(node)
                queue.extend(self.graph.get(node, []))
        
        return visited
    
    def shortest_path(self, start, end):
        """Find the shortest path between two nodes using BFS."""
        if start not in self.graph or end not in self.graph:
            return None
            
        queue = [(start, [start])]
        visited = set()
        
        while queue:
            node, path = queue.pop(0)
            
            if node == end:
                return path
                
            visited.add(node)
            
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def topological_sort(self):
        """Topological sorting using Kahn's algorithm (only for DAGs)."""
        if self.directed and self.has_cycle():
            return None  # Can't sort cyclic graph
            
        in_degree = {node: 0 for node in self.graph}
        
        for node in self.graph:
            for neighbor in self.graph[node]:
                in_degree[neighbor] += 1
        
        queue = [node for node, deg in in_degree.items() if deg == 0]
        result = []
        
        while queue:
            node = queue.pop(0)
            result.append(node)
            
            for neighbor in self.graph.get(node, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        if len(result) != len(self.graph):
            return None  # Not a DAG
            
        return result
    
    def __str__(self):
        """String representation of the graph."""
        output = []
        for node, neighbors in self.graph.items():
            output.append(f"{node} -> {', '.join(map(str, neighbors))}")
        return "\n".join(output)
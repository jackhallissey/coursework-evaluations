#This file is not needed to run the evaluations but is included for completeness
#The statistics computed by this program are referenced in the report

from evaluation import grid_graph
from math import log

for size in (10, 50, 100, 250, 500, 750, 1000):
    graph, grid = grid_graph(size, size)

    num_vertices = graph.num_vertices()
    num_edges = graph.num_edges()

    degree_sum = 0

    for v in graph.vertices():
        degree_sum += graph.degree(v)

    avg_degree = degree_sum / num_vertices

    expression = num_vertices * log(num_vertices, 2)

    print("Size: %dx%d, Vertices: %d, Edges: %d, Average Degree: %0.3f, n*log(n): %0.3f" % (size, size, num_vertices, num_edges, avg_degree, expression))
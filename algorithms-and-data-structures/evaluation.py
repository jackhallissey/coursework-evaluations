#The following Python files are required to run the evaluations: apq.py, graph.py, evaluation.py

from graph import *
from random import randint
from time import perf_counter

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    vertices = {}
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertices[nodeid] = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    # print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length, None)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    # print('Read', num, 'edges and added into the graph')
    # print(graph)
    file.close()
    return graph, vertices

def grid_graph(n, m):
    g = Graph()  
    mat = [ [g.add_vertex("(%d, %d)" % (i, j)) for j in range(m)] for i in range(n) ]

    for i in range(n):
        for j in range(m):
            if i + 1 < n:
                g.add_edge(mat[i][j], mat[i+1][j], randint(1, max(n,m)//2), None)
            if j + 1 < m:
                g.add_edge(mat[i][j], mat[i][j+1], randint(1, max(n,m)//2), None)
    
    return g, mat

#Question 1
def q1():
    print("Question 1")
    graph, vertices = graphreader("simplegraph1-2.txt")

    src = vertices[1]
    dest = vertices[4]

    paths = graph.dijkstra_heap_v1(src, dest)

    v = dest
    while v:
        cost = paths[v][0]
        pred = paths[v][1]

        print("%s to %s: %d" % (src, v, cost))

        v = pred

#Question 2
def q2():
    print("\nQuestion 2")

    graph, grid = grid_graph(4, 4)

    print("Edge weights")
    for e in graph.edges():
        vertices = e.vertices()
        print("%s to %s: %d" % (vertices[0], vertices[1], e.weight()))

    print("\nShortest path")
    paths = graph.dijkstra_heap_v1(grid[0][0], grid[3][3])

    v = grid[3][3]
    while v:
        cost = paths[v][0]
        pred = paths[v][1]

        print("%s to %s: %d" % (grid[0][0], v, cost))

        v = pred

#Question 3
def q3():
    print("\nQuestion 3")

    for size in (10, 50, 100, 250, 500, 750, 1000):
        total_runtime = 0
        total_path_cost = 0

        for _ in range(10):
            graph, grid = grid_graph(size, size)

            src = grid[size//2][size//2]
            dest = grid[0][0]

            start = perf_counter()
            paths = graph.dijkstra_heap_v1(src, dest)
            end = perf_counter()

            total_runtime += (end - start)
            total_path_cost += paths[dest][0]

        avg_runtime = total_runtime / 10
        avg_path_cost = total_path_cost / 10
        
        print("Size: %d, Average Path Cost: %d, Average Runtime: %0.3f" % (size, avg_path_cost, avg_runtime))

#Question 4
def q4():
    #v1 is the all nodes version
    #v2 is the specific destination version

    print("\nQuestion 4")

    for dest in (275, 300, 350, 400, 450, 475, 499):
        v1_total_runtime = 0
        v1_total_path_cost = 0
        v2_total_runtime = 0
        v2_total_path_cost = 0

        for _ in range(10):
            graph, grid = grid_graph(500, 500)
            
            destv = grid[dest][dest]

            #All nodes
            start = perf_counter()
            v1_paths = graph.dijkstra_heap_v1(grid[250][250], destv)
            end = perf_counter()

            v1_total_runtime += (end - start)
            v1_total_path_cost += v1_paths[destv][0]

            #Specific destination
            start = perf_counter()
            v2_paths = graph.dijkstra_heap_v2(grid[250][250], destv)
            end = perf_counter()

            v2_total_runtime += (end - start)
            v2_total_path_cost += v2_paths[destv][0]

        v1_avg_runtime = v1_total_runtime / 10
        v1_avg_path_cost = v1_total_path_cost / 10
        v2_avg_runtime = v2_total_runtime / 10
        v2_avg_path_cost = v2_total_path_cost / 10

        print("All nodes: Destination: [%d][%d], Average Path Cost: %d, Average Runtime: %0.3f" % (dest, dest, v1_avg_path_cost, v1_avg_runtime))
        print("Specific destination: Destination: [%d][%d], Average Path Cost: %d, Average Runtime: %0.3f\n" % (dest, dest, v2_avg_path_cost, v2_avg_runtime))

def q5():
    print("\nQuestion 5")

    for size in (10, 50, 100, 250, 500):
        heap_total_runtime = 0
        heap_total_path_cost = 0
        list_total_runtime = 0
        list_total_path_cost = 0

        for _ in range(10):
            graph, grid = grid_graph(size, size)

            src = grid[size//2][size//2]
            dest = grid[0][0]
            
            #Heap
            start = perf_counter()
            heap_paths = graph.dijkstra_heap_v1(src, dest)
            end = perf_counter()

            heap_total_runtime += (end - start)
            heap_total_path_cost += heap_paths[dest][0]

            #List
            start = perf_counter()
            list_paths = graph.dijkstra_list(src, dest)
            end = perf_counter()

            list_total_runtime += (end - start)
            list_total_path_cost += list_paths[dest][0]

        heap_avg_runtime = heap_total_runtime / 10
        heap_avg_path_cost = heap_total_path_cost / 10
        list_avg_runtime = list_total_runtime / 10
        list_avg_path_cost = list_total_path_cost / 10
        
        print("Heap: Size: %d, Average Path Cost: %d, Average Runtime: %0.3f" % (size, heap_avg_path_cost, heap_avg_runtime))
        print("List: Size: %d, Average Path Cost: %d, Average Runtime: %0.3f\n" % (size, list_avg_path_cost, list_avg_runtime))

def q6():
    #Original version vs simpler priority queue
    #Both versions use HeapAPQ and find the shortest paths from the source to all other nodes

    print("\nQuestion 6")

    for size in (10, 50, 100, 250, 500, 750, 1000):
        original_total_runtime = 0
        original_total_path_cost = 0
        simpler_total_runtime = 0
        simpler_total_path_cost = 0

        for _ in range(10):
            graph, grid = grid_graph(size, size)

            src = grid[size//2][size//2]
            dest = grid[0][0]
            
            #Original
            start = perf_counter()
            original_paths = graph.dijkstra_heap_v1(src, dest)
            end = perf_counter()

            original_total_runtime += (end - start)
            original_total_path_cost += original_paths[dest][0]

            #Simpler PQ
            start = perf_counter()
            simpler_paths = graph.dijkstra_heap_q6(src, dest)
            end = perf_counter()

            simpler_total_runtime += (end - start)
            simpler_total_path_cost += simpler_paths[dest][0]

        original_avg_runtime = original_total_runtime / 10
        original_avg_path_cost = original_total_path_cost / 10
        simpler_avg_runtime = simpler_total_runtime / 10
        simpler_avg_path_cost = simpler_total_path_cost / 10
        
        print("Original: Size: %d, Average Path Cost: %d, Average Runtime: %0.3f" % (size, original_avg_path_cost, original_avg_runtime))
        print("Simpler PQ: Size: %d, Average Path Cost: %d, Average Runtime: %0.3f\n" % (size, simpler_avg_path_cost, simpler_avg_runtime))


if __name__ == "__main__":
    q1()
    # q2()
    # q3()
    # q4()
    # q5()
    # q6()
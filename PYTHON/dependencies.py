import numpy as np
import networkx as nx
import matplotlib.pyplot as plt  # Optional for visualization
from collections import defaultdict, deque
def compilation_order(dependencies):
    # Create a graph, in_degree and ranks dictionary
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    nodes = set()

    # Populate the graph and in-degree
    for dependent, dependency in dependencies:
        graph[dependency].add(dependent)
        in_degree[dependent] += 1
        nodes.add(dependency)
        nodes.add(dependent)

    # Queue for nodes with in-degree 0 (no dependencies), sorted alphabetically
    queue = deque(sorted(node for node in nodes if in_degree[node] == 0))
    ranks = {node: 0 for node in queue}  # Initialize ranks for these nodes

    # Perform the topological sort and calculate ranks
    topological_order = []
    while queue:
        node = queue.popleft()
        topological_order.append(node)
        neighbors = sorted(list(graph[node]))  # Sort neighbors alphabetically
        for neighbour in neighbors:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)
                ranks[neighbour] = ranks[node] + 1

    # Group nodes by their ranks
    ranked_groups = defaultdict(list)
    for node in topological_order:
        ranked_groups[ranks[node]].append(node)

    # Combine the groups based on ranks and sort alphabetically within each group
    combined_order = []
    for rank in sorted(ranked_groups):
        combined_order.extend(sorted(ranked_groups[rank]))

    return combined_order

# Create a directed graph
G = nx.DiGraph()

LAPACK = False
OPENMPI = False

lapack = [ "lapack", "fspblas", "scalapack" ]
openmpi = [ "hwloc", "libevent", "openmpi" ]

# Add nodes (vertices) to the graph
packages = [
		 "gmp",
		 "mpfr",
         "fftw",
         "cmake",
		 "hdf5",
		 "testsweeper",
		 "blas++",
		 "lapack++",
		 "metis",
		 "scotch",
		 "superlu",
		 "arpack",
		 "mumps",
		 "suitesparse",
         "armadillo",
         "blaze",
         "tinyxml2",
         "netcdf",
         "exodus",
         "slate"]

if( LAPACK ):
    for p in lapack :
        packages.append( p )
if( OPENMPI ):
    for p in openmpi :
        packages.append( p )


G.add_nodes_from(packages)


# Add edges (dependencies) to the graph
dependencies = [
    ("blas++", "testsweeper"),
    ("lapack++", "blas++"),
    ("superlu", "metis"),
    ("mumps", "metis"),
    ("mumps", "scotch"),
    ("arpack", "cmake"),
    ("superlu", "cmake"),
    ("scotch", "cmake"),
    ("metis", "cmake"),
    ("suitesparse","cmake"),
    ("suitesparse","gmp"),
    ("mpfr","gmp"),
    ("suitesparse","mpfr"),
    ("suitesparse","metis"),
    ("armadillo", "hdf5"),
    ("armadillo", "superlu"),
    ("armadillo", "arpack"),
    ("armadillo", "metis"),
    ("testsweeper", "cmake"),
    ("timyxml2", "cmake"),
    ("netcdf", "cmake"),
    ("netcdf", "hdf5"),
    ("exodus", "cmake"),
    ("exodus", "hdf5"),
    ("exodus", "metis"),
    ("exodus", "netcdf"),
    ("slate", "cmake"),
    ("slate", "blaspp"),
    ("slate", "lapackpp")]

lapack_dependencies = [
	("lapack", "cmake"),
    ("fspblas", "blas"),
	("blas++", "blas"),
	("lapack++", "lapack"), 
	("scotch", "scalapack"),
	("superlu", "blas"),
	("mumps", "scalapack"),
    ("lapack","cmake"),
    ("suitesparse","blas"),
    ("suitesparse","lapack"),
	("scalapack", "cmake"),
    ("blaze", "blas"),
    ("blaze", "lapack"),
    ("slate", "scalapack")]


openmpi_dependencies = [
    ("hwloc", "libevent"),
    ("openmpi", "hwloc"),
	("openmpi", "libevent"),
	("hdf5", "openmpi"),
    ("metis", "openmpi"),
    ("scotch", "openmpi"),
    ("arpack", "openmpi"),
    ("mumps", "openmpi"),
    ("netcdf", "openmpi"),
    ("exodus", "openmpi"),
]
if( LAPACK ):
    for d in lapack_dependencies :
        dependencies.append( d )

if( OPENMPI ):
    for d in openmpi_dependencies :
        dependencies.append( d )

G.add_edges_from(dependencies)
# Optional: Visualize the graph (requires matplotlib)
pos = nx.spring_layout(G, scale=30, k=2/np.sqrt(G.order()))
nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue")


compilation_order = compilation_order(dependencies)
count = 1
for package in compilation_order :
    print( count, package )
    count+=1
plt.show()
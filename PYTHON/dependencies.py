import numpy as np
import networkx as nx
import matplotlib.pyplot as plt  # Optional for visualization
from collections import defaultdict, deque






def compilation_order(dependencies, packages):
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    nodes = set(packages)

    # Initialize ranks for all nodes with a default value
    ranks = {node: -1 for node in nodes}

    # Populate the graph and in-degree
    for dependent, dependency in dependencies:
        graph[dependency].add(dependent)
        in_degree[dependent] += 1
        nodes.add(dependency)

    # Queue for nodes with in-degree 0 (no dependencies), sorted alphabetically
    queue = deque(sorted(node for node in nodes if in_degree[node] == 0))

    # Update the ranks for nodes with in-degree 0
    for node in queue:
        ranks[node] = 0

    # Perform the topological sort and calculate ranks
    while queue:
        node = queue.popleft()
        for neighbour in sorted(graph[node]):  # Sort neighbors alphabetically
            in_degree[neighbour] -= 1
            # Assign rank as max of current rank and one more than the rank of the node
            ranks[neighbour] = max(ranks[neighbour], ranks[node] + 1)
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    # Calculate the max rank from the graph
    max_rank = max(ranks.values())

    # Assign ranks to independent nodes (not in ranks yet)
    for node in nodes:
        if ranks[node] == -1:
            max_rank += 1
            ranks[node] = max_rank

    # Combine the nodes based on ranks and sort alphabetically within each group
    combined_order_with_ranks = []
    for rank in range(max_rank + 1):
        nodes_at_rank = [node for node, node_rank in ranks.items() if node_rank == rank]
        combined_order_with_ranks.extend((rank, node) for node in sorted(nodes_at_rank))

    # Check and adjust ranks if dependency conditions are violated
    dependency_violation = True
    while dependency_violation:
        dependency_violation = False
        for dependent, dependency in dependencies:
            if ranks[dependent] <= ranks[dependency]:
                ranks[dependent] = ranks[dependency] + 1
                dependency_violation = True

    # Reconstruct combined order with adjusted ranks
    combined_order_with_ranks = []
    for rank in range(max(ranks.values()) + 1):
        nodes_at_rank = [node for node, node_rank in ranks.items() if node_rank == rank]
        combined_order_with_ranks.extend((rank, node) for node in sorted(nodes_at_rank))

    return combined_order_with_ranks

# Create a directed graph
G = nx.DiGraph()

LAPACK = True
OPENMPI = False
MPICH = True
SLATE = False

lapack = [ "lapack", "fspblas", "scalapack" ]
slate = [ "testsweeper", "lapackpp", "blaspp", "slate"]

# Add nodes (vertices) to the graph
packages = [
         "gperftools",
		 "gmp",
		 "mpfr",
         "fftw",
         "cmake",
		 "hdf5",
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
         "zfp",
         "googletest",
         "blaze",
         "vtk",
         "butterflypack",
         "strumpack",
         "petsc"]


if( LAPACK ):
    for p in lapack :
        packages.append( p )

if( SLATE ):
    for p in slate :
        packages.append( p )



# Add edges (dependencies) to the graph

dependencies = [
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
    ("tinyxml2", "cmake"),
    ("netcdf", "cmake"),
    ("netcdf", "hdf5"),
    ("exodus", "cmake"),
    ("exodus", "hdf5"),
    ("exodus", "metis"),
    ("exodus", "netcdf"),
    ("zfp", "cmake"),
    ("googletest", "cmake"),
    ("vtk", "cmake"),
    ("butterflypack", "cmake"),
    ("strumpack", "cmake"),
    ("strumpack", "butterflypack"),
    ("strumpack", "metis"),
    ("strumpack", "scotch"),
    ("strumpack", "zfp"),
    ("petsc", "cmake"),
    ("petsc", "gmp"),
    ("petsc", "mpfr"),
    ("petsc", "fftw"),
    ("petsc", "metis"),
    ("petsc", "scotch"),
    ("petsc", "strumpack"),
    ("petsc", "googletest"),
    ("petsc", "hdf5")]

if SLATE :
    slate_dependencies = [
        ("blaspp", "testsweeper"),
        ("lapackpp", "blaspp"),
        ("slate", "cmake"),
        ("slate", "blaspp"),
        ("slate", "lapackpp"),
        ("testsweeper", "cmake"),
        ("strumpack", "slate")
    ]

    if LAPACK :
        slate_lapack_dependencies = [
            ("blaspp", "lapack"),
            ("lapackpp", "lapack"),
            ("slate", "scalapack"),
            ("mumps", "scalapack"),
            ("arpack", "scalapack"),
            ("butterflypack", "scalapack"),
            ("strumpack", "scalapack") ]

        for p in slate_lapack_dependencies:
            packages.append(p)



if (OPENMPI or MPICH):

    if( OPENMPI ) :
        mpiimpl = "openmpi"
    else :
        mpiimpl = "mpich"

    mpi = ["hwloc", "libevent", mpiimpl]

    mpi_dependencies = [
        ("hwloc", "libevent"),
        (mpiimpl, "hwloc"),
        ("hdf5", mpiimpl ),
        ("metis", mpiimpl ),
        ("scotch", mpiimpl ),
        ("arpack", mpiimpl ),
        ("mumps", mpiimpl),
        ("netcdf", mpiimpl ),
        ("exodus", mpiimpl ),
        ("petsc", mpiimpl)
    ]

    for p in mpi:
        packages.append(p)

    for d in mpi_dependencies :
        dependencies.append( d )

if LAPACK :
    lapack_dependencies = [
        ("lapack", "cmake"),
        ("fspblas", "lapack"),
        ("scotch", "scalapack"),
        ("superlu", "lapack"),
        ("mumps", "scalapack"),
        ("lapack", "cmake"),
        ("suitesparse", "lapack"),
        ("scalapack", "cmake"),
        ("scalapack", "lapack"),
        ("scalapack", mpiimpl),
        ("blaze", "lapack"),
        ("petsc", "lapack"),
        ("petsc", "scalapack")]

    for d in lapack_dependencies :
        dependencies.append( d )

G.add_nodes_from(packages)
G.add_edges_from(dependencies)
# Optional: Visualize the graph (requires matplotlib)
pos = nx.spring_layout(G, scale=30, k=2/np.sqrt(G.order()))
nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue")

count = 1

compilation_order_with_ranks = compilation_order(dependencies, packages)
current_rank = -1
for rank, package in compilation_order_with_ranks:
    if rank != current_rank:
        current_rank = rank
        print("--- Group ", rank+1, "---")
    print(count, package)
    count += 1

#plt.show()
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt  # Optional for visualization
from collections import defaultdict, deque, OrderedDict

def compilation_order(dependencies, packages):
    graph = defaultdict(set)
    in_degree = defaultdict(int)
    nodes = set(packages)
    ranks = {node: -1 for node in nodes}

    # Remove duplicate dependencies and packages
    dependencies = set(dependencies)
    packages = set(packages)

    # Populate the graph and in-degree
    for dependent, dependency in dependencies:
        if dependent not in packages or dependency not in packages:
            raise ValueError(f"Dependency '{dependent}' or '{dependency}' not in package list")
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
            ranks[neighbour] = max(ranks[neighbour], ranks[node] + 1)
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    # Assign ranks to independent nodes (not in ranks yet)
    max_rank = max(ranks.values())
    for node in nodes:
        if ranks[node] == -1:
            max_rank += 1
            ranks[node] = max_rank

    # Combine the nodes based on ranks and sort alphabetically within each group
    combined_order_with_ranks = []
    for rank in range(max_rank + 1):
        nodes_at_rank = [node for node, node_rank in ranks.items() if node_rank == rank]
        combined_order_with_ranks.extend((rank, node) for node in sorted(nodes_at_rank))

    # Verification Step: Ensure all dependencies are correctly ordered
    for dependent, dependency in dependencies:
        if ranks[dependent] <= ranks[dependency]:
            raise ValueError(f"Dependency order issue: '{dependent}' depends on '{dependency}'")

    return combined_order_with_ranks


# Create a directed graph
G = nx.DiGraph()

LAPACK = False
OPENMPI = False
MPICH = False
SLATE = True

lapack = [ "lapack", "fspblas", "scalapack" ]
slate = [ "testsweeper", "lapackpp", "blaspp", "slate"]

# Add nodes (vertices) to the graph
packages = [
        "hwloc",
        "libevent",
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

packages =list(OrderedDict.fromkeys(packages))

# Add edges (dependencies) to the graph

dependencies = [
    ("hwloc", "libevent"),
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
    ("petsc", "butterflypack"),
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

    for d in slate_dependencies:
        dependencies.append(d)

    if LAPACK :
        slate_lapack_dependencies = [
            ("blaspp", "lapack"),
            ("lapackpp", "lapack"),
            ("slate", "scalapack"),
            ("mumps", "scalapack"),
            ("arpack", "scalapack"),
            ("butterflypack", "scalapack"),
            ("strumpack", "scalapack") ]

        for d in slate_lapack_dependencies:
            dependencies.append(d)



if (OPENMPI or MPICH):

    if( OPENMPI ) :
        mpiimpl = "openmpi"
    else :
        mpiimpl = "mpich"

    mpi = [ mpiimpl]

    mpi_dependencies = [
        (mpiimpl, "hwloc"),
        ("hdf5", mpiimpl ),
        ("metis", mpiimpl ),
        ("scotch", mpiimpl ),
        ("arpack", mpiimpl ),
        ("mumps", mpiimpl),
        ("netcdf", mpiimpl ),
        ("exodus", mpiimpl ),
        ("petsc", mpiimpl),
        ("fftw", mpiimpl)
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
    print("#", package)
    count += 1

print( len( packages ))

#plt.show()
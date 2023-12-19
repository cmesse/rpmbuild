import networkx as nx
import matplotlib.pyplot as plt  # Optional for visualization

# Create a directed graph
G = nx.DiGraph()

LAPACK = False

lapack = [ "lapack", "fspblas", "scalapack" ]




# Add nodes (vertices) to the graph
packages = ["libevent",
		 "openmpi",
		 "hdf5",
		 "testsweeper",
		 "blas++",
		 "lapack++",
		 "metis",
		 "scotch",
		 "superlu" ]
		 
G.add_nodes_from(packages)

if( LAPACK ):
	G.add_nodes_from(packages)
	
# Add edges (dependencies) to the graph
dependencies = [
	("openmpi", "libevent"),
	("hdf5", "openmpi"), 
	("blas++", "testsweeper"), 
	("lapack++", "blas++"),
	("metis", "openmpi"),
	("scotch","openmpi"),
	("superlu", "metis") ]
	
G.add_edges_from(dependencies)

lapack_dependencies = [
	("blas++", "blas"),
	("lapack++", "lapack"), 
	("scotch", "scalapack"),
	("superlu", "blas")]
	
# Optional: Visualize the graph (requires matplotlib)
pos = nx.spring_layout(G, seed=42)  # Adjust layout as needed
nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue")
plt.show()

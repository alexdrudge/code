import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
// not allowed
import java.util.Collection;
import java.util.Collections;
import java.util.HashMap;

public class ShortestPath {

	private HashMap<String,Node> nodes;
	
	public ShortestPath() {
		nodes = new HashMap<>();
	}
	
	public String nodesInShortestPath(String start, String end) {
		// question 5
		
		Node startNode = nodes.get(start);
		Node endNode = nodes.get(end);

		Node currentNode = endNode;
		ArrayList<Node> path = new ArrayList<Node>();
		path.add(endNode);
		while (currentNode != null) {
			System.out.println(currentNode);
			EdgeList edges = currentNode.getEdges();
			int num_edges = edges.length();
			Node shortest = edges.get(0).getEndNode();
			for (int i=0;i<num_edges;i++) {
				Edge e = edges.get(i);
				Node n = e.getEndNode();
				if (n.getShortestDistance() <= shortest.getShortestDistance()) {
					shortest = n;
				}
			}
			path.add(shortest);
			if (shortest == startNode) {
				currentNode = null;
			} else {
				currentNode = shortest;
			}
		}
		Collections.reverse(path);
		String path_label = "[";
		for (Node node : path) {
			path_label += node.getLabel();
		}
		path_label += "]";
		
		return (path_label);
	}
	
	public int shortestPath(String start, String end) {
		// question 4
		
		Node startNode = nodes.get(start);
		Node endNode = nodes.get(end);
		
		PriorityQueue queue = new PriorityQueue();
		startNode.setAsStartNode();
		queue.add(0, startNode);

		while (queue.hasNext()) {
			Node currentNode = queue.getNextHighestPriorityNode();
			if (currentNode == endNode) {
				return endNode.getShortestDistance();
			} else {
				EdgeList edges = currentNode.getEdges();
				int num_edges = edges.length();
				for (int i=0;i<num_edges;i++) {
					Edge e = edges.get(i);
					Node n = e.getEndNode();
					if (currentNode.hasBeenVisited() == false) {
						n.updateShortestDistance(e);
						queue.add(n.getShortestDistance(), n);
					}
				}
				currentNode.setVisited();
			}
		}
		
		return 0;
	}
	
	public void readInNodes(String file) {
		try {
			File f = new File(file);
			BufferedReader br = new BufferedReader(new FileReader(f));
			String s = "";
			while((s=br.readLine()) !=null) {
				String[] info = s.split(" ");
				if(!nodes.containsKey(info[0])) {
					nodes.put(info[0], new Node(info[0]));
				}
				if(!nodes.containsKey(info[1])) {
					nodes.put(info[1], new Node(info[1]));
				}
				Node n1 = nodes.get(info[0]);
				Node n2 = nodes.get(info[1]);
				int i = Integer.valueOf(info[2]);
				Edge e = new Edge(i,n1,n2);
				nodes.get(info[0]).addEdge(e);
				Edge e2 = new Edge(i,n2,n1);
				nodes.get(info[1]).addEdge(e2);
			}
			br.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void printGraph() {
		System.out.println("Graph");
		for(String k : nodes.keySet()) {
			System.out.println(nodes.get(k));
		}
	}
}

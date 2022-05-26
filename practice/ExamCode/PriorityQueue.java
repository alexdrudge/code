
public class PriorityQueue {
	private QNode root;
	
	public PriorityQueue() {
		root = null;
	}
	
	public void add(int priority, Node n) {
		QNode node = new QNode(priority, n);
		if (root == null) {
			root = node;
		} else {
			root.addQNode(node);
			if (root.getPrevious() != null) {
				root = root.getPrevious();
			}
		}
	}
	
	public Node getNextHighestPriorityNode() {
		if (root == null) {
			return null;
		} else {
			QNode node = root;
			QNode next = root.getNext();
			if (next == null) {
				root = null;
			} else {
				root = next;
				next.setPrevious(null);
			}
			return node.getNode();
		}
	}
	
	public boolean hasNext() {
		return (root!=null);
	}
	
	public String toString() {
		if(root == null) {
			return "(empty)";
		}
		return root.toString();
	}
}
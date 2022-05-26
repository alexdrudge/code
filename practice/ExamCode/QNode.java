
public class QNode{
	private int priority;
	private QNode next;
	private QNode previous;
	private Node node;
	
	public QNode(int priority, Node n) {
		this.priority = priority;
		this.node = n;
		next = null;
		previous = null;
	}
	
	public Node getNode() {
		return node;
	}
	
	public void addQNode(QNode n) {
		int num = n.getPriority();
		if (num < priority) {
			if (previous == null) {
				n.setNext(this);
				n.setPrevious(null);
				previous = n;
			} else {
				n.setPrevious(previous);
				n.setNext(this);
				previous.setNext(n);
				previous = n;
			}
		} else if (next == null) {
			n.setPrevious(this);
			n.setNext(null);
			next = n;
		} else {
			next.addQNode(n);
		}
	}
	
	public int getPriority() {
		return priority;
	}
	
	public void setPrevious(QNode p) {
		previous = p;
	}
	
	public QNode getPrevious() {
		return previous;
	}
	
	public void setNext(QNode n) {
		next = n;
	}
	
	public QNode getNext() {
		return next;
	}
	
	public String toString() {
		String s = node.getLabel() + " (" + priority + ") : ";
		if (next!=null) {
			s += next.toString();
		}
		return s;
	}
	
}


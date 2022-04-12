public class SortedLinkedList implements SortedList{
    private Node head = null;
    private Node tail = null;
    private int length = 0;
    private boolean ascending = true;

    @Override
    public int size() {
        return this.length;
    }

    @Override
    public void add(String string) {
        Node node = new Node(string);
        this.add(node);
    }

    @Override
    public void add(Node node) {
        // verify that the strings are all [a-z][A-Z]
        if(this.length == 0) { // case 1.0 list is empty
            this.head = node;
            this.tail = node;
            node.setPrev(null);
            node.setNext(null);
            this.length++;
        } else if(this.length == 1) { // case 2.0 list has one node
            int diff = node.getString().compareToIgnoreCase(this.head.getString());
            if(diff > 0) { // case 2.1 the node is larger than the head
                this.tail = node;
                this.head.setNext(node);
                node.setPrev(this.head);
                node.setNext(null);
                this.length++;
            } else if(diff < 0) { // case 2.2 the node is smaller than the head
                this.head = node;
                this.tail.setPrev(node);
                node.setPrev(null);
                node.setNext(this.tail);
                this.length++;
            } else { // case 2.3 the node is the same as the head
                System.out.println("string already used");
            }
        } else { // case 3.0 the list has multiple nodes
            Node current = this.head;
            while(current != null) {
                int diff = node.getString().compareToIgnoreCase(current.getString());
                if(diff < 0) {
                    if(current == this.head) { // case 3.1 the node is smaller than the head
                        this.head = node;
                        node.setPrev(null);
                        node.setNext(current);
                        current.setPrev(node);
                        this.length++;
                        break;
                    } else { // case 3.2 the node is smaller than the current
                        current.getPrev().setNext(node);
                        node.setPrev(current.getPrev());
                        current.setPrev(node);
                        node.setNext(current);
                        this.length++;
                        break;
                    }
                } else if(diff == 0) { // case 3.3 the node is already in the list
                    System.out.println("string already used");
                    break;
                }
                current = current.getNext();
            }
            if(current == null) { // case 3.4 the node is larger than the tail
                current = this.tail;
                this.tail = node;
                current.setNext(node);
                node.setPrev(current);
                node.setNext(null);
                this.length++;
            }
        }
    }

    @Override
    public Node getFirst() {
        return this.get(0);
    }

    @Override
    public Node getLast() {
        return this.get(this.length-1);
    }

    @Override
    public Node get(int index) {
        int i = 0;
        Node current = null;
        if(this.ascending) {
            current = this.head;
        } else {
            current = this.tail;
        }
        while(current != null) {
            if(index == i) {
                return current;
            }
            if(this.ascending) {
                current = current.getNext();
            } else {
                current = current.getPrev();
            }
            i++;
        }
        return null;
    }

    @Override
    public boolean isPresent(String string) {
        Node current = this.head;
        while(current != null) {
            // should it be case insensitive?
            if(current.getString() == string) {
                return true;
            }
            current = current.getNext();
        }
        return false;
    }

    @Override
    public boolean removeFirst() {
        return this.remove(0);
    }

    @Override
    public boolean removeLast() {
        return this.remove(this.length-1);
    }

    @Override
    public boolean remove(int index) {
        if(this.length == 0) {
            return false;
        } else if(this.length == 1) {
            if(index == 0) {
                this.head = null;
                this.tail = null;
                this.length--;
                return true;
            } else {
                return false;
            }
        } else {
            int i = 0;
            Node current = null;
            if(this.ascending) {
                current = this.head;
            } else {
                current = this.tail;
            }
            while(current != null) {
                if(i == index) {
                    if(current == this.head) {
                        this.head = current.getNext();
                        this.head.setPrev(null);
                    } else if(current == this.tail) {
                        this.tail = current.getPrev();
                        this.tail.setNext(null);
                    } else {
                        current.getPrev().setNext(current.getNext());
                        current.getNext().setPrev(current.getPrev());
                    }
                    this.length--;
                    return true;
                }
                if(this.ascending) {
                    current = current.getNext();
                } else {
                    current = current.getPrev();
                }
                i++;
            }
            return false;
        }
    }

    @Override
    public boolean remove(String string) {
        Node current = this.head;
        int i = 0;
        while(current != null) {
            // should it be case insensitive?
            if(current.getString() == string) {
                if(this.ascending) {
                    return this.remove(i);
                } else {
                    return this.remove(this.length - i - 1);
                }
            }
            current = current.getNext();
            i++;
        }
        return false;
    }

    @Override
    public void orderAscending() {
        this.ascending = true;
    }

    @Override
    public void orderDescending() {
        this.ascending = false;
    }

    @Override
    public void print() {
        if(this.length == 0) {
            System.out.println("list empty");
        } else {
            Node current = null;
            if(this.ascending) {
                current = this.head;
            } else {
                current = this.tail;
            }
            while(current != null) {
                System.out.println(current.getString());
                if(this.ascending) {
                    current = current.getNext();
                } else {
                    current = current.getPrev();
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Start");

        SortedLinkedList list = new SortedLinkedList();
        list.add(new Node("Charlie"));
        list.add(new Node("Alpha"));
        list.add(new Node("Bravo"));
        list.orderDescending();
        list.add(new Node("bravo"));
        System.out.println(list.getLast().getString());
        list.remove("Bravo");
        list.print();

        System.out.println("Done");
    }
    
}

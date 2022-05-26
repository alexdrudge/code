/*
 * YOU ARE NOT ALLOWED TO MODIFY THIS FILE 
 */
public abstract class HashTable {

	protected String[] storageArray = new String[10];
	protected int numItems = 0;
	protected double loadFactor = 0.0;
	
	/**
	* Returns a string with the status of the hash table and its
	* contents.
	*
	* @return       a string with the status of the hash table
	*/
	public final String print() {
		String status = "~~~~~~~~~~~~~~\n";
		status += String.format("Hash table has %d entries, with a load factor of %f\n", numItems, loadFactor);
		for(int i = 0; i < storageArray.length; i++) {
			status += String.format("%d: %s\n", i, storageArray[i]);
		}
		return status;
	}
	
	/**
	* To be used as a placeholder in  the hash table.
	*
	* @return       the placeholder string
	*/
	protected final static String getPlaceholder() {
		return "---PLACEHOLDER---";
	}

	protected abstract int hashFunction(String key);
	protected abstract void resizeMap(int newSize);
	public abstract boolean add(String name);
	public abstract boolean remove(String name);
	public abstract boolean search(String name);

}

// This is a blank file, please complete your solution here.

/**
 * MyHashTable
 */
public class MyHashTable extends HashTable{

    // prevents infinite loop of upsizing then downsizing
    private boolean resizing;

    public MyHashTable() {
        this.resizing = false;
    }

    /**
     * Returns the hash value for a string
     * 
     * @param key The string to be hashed
     * @return An integer with the hash value
     */
    @Override
    protected int hashFunction(String key) {
        if (key == null) return 0;
        
        int total = 0;
        for (int i=0;i<key.length();i++) {
            char c = key.charAt(i);
            total += (int) c;
        }
        return total % storageArray.length;
    }

    /**
     * Resize the hash table
     * 
     * @param newSize The new length of the hash table
     */
    @Override
    protected void resizeMap(int newSize) {
        String[] temp_storageArray = new String[storageArray.length];
        System.arraycopy(storageArray, 0, temp_storageArray, 0, storageArray.length);
        storageArray = new String[newSize];
        
        numItems = 0;
        loadFactor = 0.0;
        resizing = true;

        for (String name : temp_storageArray) {
            if (name != getPlaceholder() && name != null) {
                add(name);
            }
        }

        resizing = false;
        checkResize();
    }

    /**
     * Checks if the table needs to be resized
     */
    private void checkResize() {
        if (resizing) return;

        if (loadFactor >= 0.7) {
            resizeMap(storageArray.length*2);
        } else if ((loadFactor <= 0.2) && (storageArray.length/2 >= 10)) {
            resizeMap(storageArray.length/2);
        }
    }

    /**
     * Adds a string into the hash table
     * 
     * @param name The string to be added to the hash table
     * @return true if the string is added, false if the string is not added
     */
    @Override
    public boolean add(String name) {
        if (name == getPlaceholder() || name == null) return false;
        if (search(name)) return false;

        int index = hashFunction(name);
        int count = 0;

        while (true) {
            if (storageArray[index] == null) {
                storageArray[index] = name;
                numItems++;
                loadFactor = (double) numItems / (double) storageArray.length;
                checkResize();
                return true;
            } else if (storageArray[index] == getPlaceholder()) {
                storageArray[index] = name;
                return true;
            } else {
                if (storageArray[index] == name) {
                    return false;
                }
                index = (index + 1) % storageArray.length;
            }
            count++;
            if (count > storageArray.length) return false;
        }
    }

    /**
     * Remove a string from the hash table
     * Strings are replaced with a place holder
     * 
     * @param name The string to be removed from the list
     * @return true if the string is removed, false if the string is not removed
     */
    @Override
    public boolean remove(String name) {
        if (name == getPlaceholder() || name == null) return false;
        
        int index = hashFunction(name);
        int count = 0;

        while (true) {
            if (storageArray[index] == name) {
                storageArray[index] = getPlaceholder();
                return true;
            } else if (storageArray[index] == null) {
                return false;
            } else {
                index = (index + 1) * storageArray.length;
            }
            count++;
            if (count > storageArray.length) return false;
        }
    }

    /**
     * Find if a string is stored within the hash table
     * 
     * @param name The string being searched for
     * @return true if the string is found, false if the string is not found
     */
    @Override
    public boolean search(String name) {
        int index = hashFunction(name);
        int count = 0;

        while (true) {
            if (storageArray[index] == name) {
                return true;
            } else if (storageArray[index] == null) {
                return false;
            } else {
                index = (index + 1) % storageArray.length;
            }
            count++;
            if (count > storageArray.length) return false;
        }
    }
    
}
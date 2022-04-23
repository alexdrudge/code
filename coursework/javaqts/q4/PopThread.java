import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class PopThread implements Runnable{
    private ArrayList<String> files = null;
    static {
        // ensures the file exists and is empty
        File temp = new File("result.txt");
        temp.delete();
        try {
            File file = new File("result.txt");
            file.createNewFile();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public PopThread(ArrayList<String> files) {
        this.files = files;
    }

    private ArrayList<String> file_read(String filename) {
        ArrayList<String> input = new ArrayList<String>();
        try(BufferedReader br = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                input.add(line);
            }
            return input;
        } catch(IOException e) {
            e.printStackTrace();
            return input;
        }
    }

    private static synchronized void file_write(int num, ArrayList<String> input) {
        // read in existsing data
        ArrayList<String> content = new ArrayList<String>();
        try(BufferedReader br = new BufferedReader(new FileReader("result.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                content.add(line);
            }
        } catch(IOException e) {
            e.printStackTrace();
        }
        // place in the new data
        ArrayList<String> temp = new ArrayList<String>();
        ArrayList<String> result = new ArrayList<String>();
        boolean written = false;
        for(String line : content) {
            temp.add(line);
            // assumes label in the form #000/000 exists
            // assumes totals are equal
            // assumes that no other lines has # and /
            if (line.length() == 8) {
                if(line.charAt(0) == '#' && line.charAt(4) == '/') {
                    char[] arr = new char[3];
                    line.getChars(1, 4, arr, 0);
                    int id = Integer.parseInt(String.valueOf(arr));
                    if(id == num) {
                        written = true;
                    } else if(id > num && written == false) {
                        for(String data : input) {
                            result.add(data);
                        }
                        written = true;
                    }
                    for(String data : temp) {
                        result.add(data);
                    }
                    temp = new ArrayList<String>();
                }
            }
        }
        if(written == false) {
            for(String data : input) {
                result.add(data);
            }
        }
        try(FileWriter fw = new FileWriter("result.txt")) {
            StringBuilder sb = new StringBuilder();
            for(String line : result) {
                sb.append(line);
                sb.append(System.lineSeparator());
            }
            String output = sb.toString();
            fw.write(output);
        } catch(IOException e) {
            e.printStackTrace();
        }
    }

    @Override
    public void run() {
        if (this.files != null) {
            for(String filename : this.files) {
                ArrayList<String> input = file_read(filename);
                if (input.size() > 0) {
                    // assumes label in the form #000/000 exists
                    // assumes totals are equal
                    char[] arr = new char[3];
                    input.get(input.size()-1).getChars(1,4,arr,0);
                    int num = Integer.parseInt(String.valueOf(arr));
                    file_write(num, input);
                }
            }
        }
    }

    public static void main(String[] args) {
        System.out.println("Start");

        ArrayList<String> filesOne = new ArrayList<String>();
        filesOne.add("1831-06-01.txt");
        filesOne.add("2003-08-27.txt");

        ArrayList<String> filesTwo = new ArrayList<String>();
        filesTwo.add("1961-04-12.txt");
        filesTwo.add("1972-12-11.txt");

        PopThread pop1 = new PopThread(filesOne);
        PopThread pop2 = new PopThread(filesTwo);
        Thread t1 = new Thread(pop1);
        Thread t2 = new Thread(pop2);
        System.out.println("threads created");

        t1.start();
        t2.start();
        try {
            t1.join();
            t2.join();
            System.out.println("threads completed");
        } catch(InterruptedException e) {
            System.out.println("threads interrupted");
        }

        System.out.println("Done");
    }
    
}

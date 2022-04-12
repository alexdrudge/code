import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class VigenereCipher implements Cipher{
    private static String import_file(String filename) {
        try (BufferedReader br = new BufferedReader(new FileReader(filename))) {
            StringBuilder sb = new StringBuilder();
            int c;
            while ((c = br.read()) != -1) {
                sb.append((char) c);
            }
            String input = sb.toString();
            return input;
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

    @Override
    public String encrypt(String message_filename, String key_filename) {
        String input = VigenereCipher.import_file(message_filename);
        String key = VigenereCipher.import_file(key_filename);
        if (key.matches("[a-zA-Z]+")) {
            key = key.toUpperCase();
        } else {
            return input;
        }
        if (input == "" || key == "") {
            return input;
        }
        StringBuilder sb = new StringBuilder();
        for (int i=0;i<input.length();i++) {
            char plain = input.charAt(i);
            if (Character.isAlphabetic(plain)) {
                plain = Character.toUpperCase(plain);
                int plain_num = ((int) plain) - 65;
                int key_num = ((int) key.charAt(i % key.length())) - 65;
                char cipher = (char) (((plain_num + key_num) % 26) + 65);
                sb.append(cipher);
            } else {
                sb.append(plain);
            }
        }
        String output = sb.toString();
        return output;
    }

    @Override
    public String decrypt(String message_filename, String key_filename) {
        String input = VigenereCipher.import_file(message_filename);
        String key = VigenereCipher.import_file(key_filename);
        if (key.matches("[a-zA-Z]+")) {
            key = key.toUpperCase();
        } else {
            return input;
        }
        if (input == "" || key == "") {
            return input;
        }
        StringBuilder sb = new StringBuilder();
        for (int i=0;i<input.length();i++) {
            char plain = input.charAt(i);
            if (Character.isAlphabetic(plain)) {
                plain = Character.toUpperCase(plain);
                int plain_num = ((int) plain) - 65;
                int key_num = ((int) key.charAt(i % key.length())) - 65;
                char cipher = (char) (((plain_num - key_num + 260) % 26) + 65);
                sb.append(cipher);
            } else {
                sb.append(plain);
            }
        }
        String output = sb.toString();
        return output;
    }

    public static void main(String[] args) {
        System.out.println("Start");

        VigenereCipher cipher = new VigenereCipher();
        System.out.println(VigenereCipher.import_file("encrypt.txt"));
        System.out.println(cipher.encrypt("encrypt.txt", "key.txt"));
        System.out.println(VigenereCipher.import_file("decrypt.txt"));
        System.out.println(cipher.decrypt("decrypt.txt", "key.txt"));

        System.out.println("Done");
    }
}

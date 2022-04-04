import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class EchoServer {

	private int port = 14002;
	
	public void go() {
	
		try(ServerSocket mySocket = new ServerSocket(port)) {
			
			System.out.println("Server listening...");
			// Accept a connection from a client
			Socket clientSocket = mySocket.accept();
			System.out.println("Server accepted connection on: " + mySocket.getLocalPort() + " ; " + clientSocket.getPort());
			
			// Setup the ability to read the data from the client
			InputStreamReader clientCharStream = new InputStreamReader(clientSocket.getInputStream());
			BufferedReader clientIn = new BufferedReader(clientCharStream);
								
			// Set up the ability to send the data to the client
			PrintWriter clientOut = new PrintWriter(clientSocket.getOutputStream(), true);
			
			// Read from the client, and send the message back
			while(true) {
				String userInput = clientIn.readLine();
				clientOut.println(userInput);
			}
			
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args) {
		EchoServer myEchoServer = new EchoServer();
		myEchoServer.go();
	}

}

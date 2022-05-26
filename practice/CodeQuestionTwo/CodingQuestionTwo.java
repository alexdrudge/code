import java.text.DecimalFormat;
import java.util.ArrayList;

/** 
 *  Coding Question Two:
 *  
 *  Your task is to develop the code which will enable the use of MarsAir International's 
 *  calculateFlightDistance method using the new CCSA interface. This is achieved in two steps:
 *  1.  Develop your solution by completing the class provided in CodingQuestionTwoClass.java. 
 *      Do not change the name of this class.
 *  2.  Modify the one line of code indicated in the CodingQuestionTwo.java which will instantiate 
 *      your developed class. Do not modify any other part of this file.
 *  
 *  You are not allowed to modify the FlightCalculator.java, FlightInterface.java, or 
 *  PolarCoordinate.java classes, however you should read them carefully.
*/
public class CodingQuestionTwo {

	/** 
	 *  Coding Question Two:
	 *  
	 *  This is the main method which will use your solution to calculate the flight distance given a set of 
	 *  Polar coordinate control points. 
	 *  
	 *  In this file, you should only change the one line of code that has been highlighted.
	 *  Please develop your solution in the CodingQuestionTwoClass.java file.
	 *  
	*/
	public static void main(String[] args) {
		
		ArrayList<PolarCoordinate> points = new ArrayList<PolarCoordinate>();
		points.add(new PolarCoordinate(1, Math.PI/2));
		points.add(new PolarCoordinate(3, 1.5));
		points.add(new PolarCoordinate(3, 3));
		
		/************************************************************************************/
		/*****  ONLY CHANGE THIS ONE LINE OF CODE *******************************************/
		FlightInterface yourClass = new CodingQuestionTwoClass(); // Replace null with your solution!
		/************************************************************************************/
		
		double flightDistance = yourClass.calculateFlightDistance(points);
		System.out.println(flightDistance);
		
		// This is included for you to check your answer - but be careful we will run other tests.
		DecimalFormat df = new DecimalFormat("#.########");
		String ans = df.format(flightDistance);
		
		if(ans.equals("4.07136904"))
			System.out.println("Test passed!");
		else
			System.out.println("Test failed... ");
	}
	
}

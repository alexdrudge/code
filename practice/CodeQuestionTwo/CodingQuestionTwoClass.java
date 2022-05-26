import java.util.ArrayList;

/** 
 *  Coding Question Two class:
 *  
 *  Develop your solution by completing this class.
 *  Do not change the name of this class.
 *  
*/
public class CodingQuestionTwoClass implements FlightInterface{

    @Override
    public double calculateFlightDistance(ArrayList<PolarCoordinate> controlPoints) {
        
        double[] xs = new double[controlPoints.size()];
        double[] ys = new double[controlPoints.size()];
        int count = 0;

        for (PolarCoordinate coord : controlPoints) {
            double r = coord.getR();
            double theta = coord.getTheta();
            double x = r * Math.cos(theta);
            double y = r * Math.sin(theta);
            xs[count] = x;
            ys[count] = y;
            count++;
        }

        FlightCalculator flightCalculator = new FlightCalculator();
        double distance = flightCalculator.calculateFlightDistance(xs, ys);

        return distance;
    }
	
}

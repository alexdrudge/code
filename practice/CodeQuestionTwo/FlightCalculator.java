/*
 * Copyright (c) 2021, MarsAir International and/or their affiliates. 
 * All rights reserved.
 *
 * Redistribution and use in source, with or without modification, are 
 * not permitted.
 * 
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
 * IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
 * THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
 * LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
 * NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. IT IS NOT
 * MY FAULT IF YOU DO NOT KNOW HOW TO BUILD A ROCKET TO GO TO MARS.
 */
 

/** The flight calculator to allow us to explore the solar system. Used for
 *  calculating the flight distance of our space shuttles and their payloads.
 *  @author REDACTED
 *  @version 1.8
 *  @since 1.0
*/
public class FlightCalculator {
	
	/**
     * The name of the target planet that we will go and explore
     */
	private String targetPlanet;
	
	/**
	 * The Rover's which we can use to travel the solar system
	 */
	enum Rover{
		SOJOURNER,
		OPPORTUNITY,
		SPIRIT,
		CURIOSITY,
		PERSERVERANCE
	}
	
	/**
	* Sole constructor, which sets the planet to Mars (don't want to waste memory
	* so only instantiate targetPlanet when object is created).
	*/
	public FlightCalculator() {
		targetPlanet = "Mars";
	}
	
	
	/**
	 * @return current target planet which we will be exploring
	 */
	public String getTargetPlanet() {
		return targetPlanet;
	}

	/**
	* A method for setting which planet we will journey to. It defaults to Mars because it is the
	* boss' favourite chocolate bar.
	*
	* @param  targetPlanet   sets the target planet for the expedition, must be in our Solar System
	*/
	public void setTargetPlanet(String targetPlanet) {
		this.targetPlanet = targetPlanet;
	}
	
	/**
	* A method to retrieve the weight of the Rover which we will be sending
	* to Mars. Useful in case it affects our trajectory at a later date, however
	* at the moment we do not need to know this information. My manager shouted at
	* me for wasting time on features we might not need, and accused me of using it 
	* as an excuse to browse Wikipedia searching for the weight of all these Rovers.
	*
	* @param  robot   the type of Rover that we will be sending to Mars
	* @return         the weight of the Rover in kg (these are accurate)
	*/
	public float calculateWeight(Rover robot) {
		switch(robot) {
			case SOJOURNER:
				return 12;
			case OPPORTUNITY:
				return 185;
			case SPIRIT:
				return 185;
			case CURIOSITY:
				return 899;
			case PERSERVERANCE:
				return 1025;
			default:
				return -1;
		}
	}

	/**
	* Calculates the Euclidean distance between two points in Euclidean space,
	* i.e. the length of the line segment between the two points. More specifically,
	* this method calculates the distance using the Cartesian coordinates of two 
	* two-dimensional points using Pythagorean theorem.
	*
	* @param  x1   the x coordinate of the first point
	* @param  y1   the y coordinate of the first point
	* @param  x2   the x coordinate of the second point
	* @param  y2   the y coordinate of the second point
	* @return      the Euclidean distance between the two points
	*/
	private double euclideanDistance(double x1, double y1, double x2, double y2) {
		return Math.sqrt(Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2));
	}
	
	/**
	* Calculates the flight distance of the launch shuttle given the control points.
	* This uses between two to four control points and Bezier curves to calculate the
	* aircraft's trajectory, and hence flight distance. The flight path can either be
	* a linear, quadratic, or cubic Bezier curve. This is based on Bernstein polynomials
	* and is super secret stuff - please don't tell NASA.
	*
	* @param  xs   the x values of the control points
	* @param  ys   the y values of the control points
	* @return      the distance of the flight path for the specified control points
	*/
	public double calculateFlightDistance(double[] xs, double[] ys) {
		
		if(xs.length != ys.length)
			return -1;
		
		if(xs.length < 2)
			return -1;
		
		double distance = 0.0;
		double prev_x = 0.0, prev_y = 0.0;
		
		if(xs.length == 2) {
			
			for(int i = 0; i <= 100; i++) {
				double t = (double)i/100;
				
				double x = (1 - t) * xs[0] + t * xs[1];
				double y = (1 - t) * ys[0] + t * ys[1];
				
				if(t > 0)
					distance += euclideanDistance(x, y, prev_x, prev_y);
				
				prev_x = x;
				prev_y = y;
			}
		}
		else if(xs.length == 3) {
			for(int i = 0; i <= 100; i++) {
				double t = (double)i/100;
				
				double x = Math.pow((1 - t),2) * xs[0] + 2 * (1 - t) * t * xs[1] + 
						Math.pow(t,2) * xs[2];
				double y = Math.pow((1 - t),2) * ys[0] + 2 * (1 - t) * t * ys[1] + 
						Math.pow(t,2) * ys[2];
				
				if(t > 0)
					distance += euclideanDistance(x, y, prev_x, prev_y);
				
				prev_x = x;
				prev_y = y;
			}
		}
		else if(xs.length == 4) {
			for(int i = 0; i <= 100; i++) {
				double t = (double)i/100;
				
				double x = Math.pow((1 - t),3) * xs[0] + 3 * Math.pow((1 - t),2) * t * xs[1] + 
						3 * (1 - t) * Math.pow(t,2) * xs[2] + Math.pow(t, 3) * xs[3];
				double y = Math.pow((1 - t),3) * ys[0] + 3 * Math.pow((1 - t),2) * t * ys[1] + 
						3 * (1 - t) * Math.pow(t,2) * ys[2] + Math.pow(t, 3) * ys[3];
				
				if(t > 0)
					distance += euclideanDistance(x, y, prev_x, prev_y);
				
				prev_x = x;
				prev_y = y;
			}
		}
		return distance;
	}

}

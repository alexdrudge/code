/*
 * Copyright (c) 2021, Chris Clarke Space Agency and/or their affiliates. 
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
 * SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. I WAS REALLY
 * EXCITED THAT I MIGHT GET TO GO AND MEET SANTA BUT THEN I GOOGLED WHAT
 * POLAR COORDINATES ACTUALLY ARE.
 */


/** Polar coordinates class.
 *  @author Chris Clarke
 *  @version 1.1
 *  @since 1.0
*/
public class PolarCoordinate {
	
	/**
     * The distance from a reference point
     */
	private double r;
	
	/**
     * The angle from a reference direction
     */
	private double theta;
	
	/**
	* Constructor for creating a polar coordinate.
	*
	* @param  r         the value of the distance from a reference point
	* @param  theta     the value of the angle from a reference direction
	*/
	public PolarCoordinate(double r, double theta) {
		this.r = r;
		this.theta = theta;
	}
	
	/**
	 * @return the distance from a reference point
	 */	
	double getR() {
		return r;
	}
	
	/**
	 * @return the angle from a reference direction
	 */
	double getTheta() {
		return theta;
	}
	
}
	
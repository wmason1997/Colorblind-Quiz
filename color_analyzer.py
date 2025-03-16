import numpy as np
import cv2

class ColorAnalyzer:
    def __init__(self):
        # Define the ideal ROYGBIV boundaries (normalized to 0-1 range)
        self.ideal_boundaries = np.array([
            0.143,  # Red-Orange
            0.286,  # Orange-Yellow
            0.429,  # Yellow-Green
            0.571,  # Green-Blue
            0.714,  # Blue-Indigo
            0.857   # Indigo-Violet
        ])
    
    def analyze_spectrum(self, user_lines):
        """
        Analyze user-drawn lines against ideal color boundaries.
        
        Args:
            user_lines (list): List of dictionaries containing x-coordinates of user-drawn lines
            
        Returns:
            dict: Analysis results including score and potential color blindness type
        """
        # Convert user lines to normalized positions (0-1 range)
        if not user_lines:
            return {
                "score": 0,
                "message": "No lines detected. Please draw lines where you see color changes.",
                "type": "unknown"
            }

        # Extract x coordinates and normalize them
        user_positions = np.array([line['x'] for line in user_lines]) / 600.0  # Canvas width is 600px
        
        if len(user_positions) != len(self.ideal_boundaries):
            return {
                "score": 0,
                "message": f"Expected {len(self.ideal_boundaries)} lines, but got {len(user_positions)}. Please mark all color transitions.",
                "type": "incomplete"
            }

        # Sort positions to match with ideal boundaries
        user_positions.sort()
        
        # Calculate mean squared error between user positions and ideal boundaries
        mse = np.mean((user_positions - self.ideal_boundaries) ** 2)
        
        # Convert MSE to a 0-100 score (0 = worst, 100 = perfect)
        score = max(0, 100 * (1 - mse * 10))
        
        # Analyze potential color blindness type based on specific deviations
        color_blindness_type = self._determine_color_blindness_type(user_positions)
        
        return {
            "score": round(score, 2),
            "message": self._get_score_message(score),
            "type": color_blindness_type
        }
    
    def _determine_color_blindness_type(self, user_positions):
        """
        Determine potential color blindness type based on line positions.
        """
        # Calculate deviations for each boundary
        deviations = user_positions - self.ideal_boundaries
        
        # Define thresholds for different types of color blindness
        red_green_threshold = 0.1
        blue_yellow_threshold = 0.1
        
        # Check for specific patterns in deviations
        if np.abs(deviations[0:2]).mean() > red_green_threshold:
            return "possible_protanopia"  # Red-blindness
        elif np.abs(deviations[2:4]).mean() > red_green_threshold:
            return "possible_deuteranopia"  # Green-blindness
        elif np.abs(deviations[4:]).mean() > blue_yellow_threshold:
            return "possible_tritanopia"  # Blue-blindness
        else:
            return "normal"
    
    def _get_score_message(self, score):
        """
        Get a descriptive message based on the score.
        """
        if score >= 90:
            return "Excellent color discrimination!"
        elif score >= 70:
            return "Good color discrimination, minor variations detected."
        elif score >= 50:
            return "Moderate color discrimination, possible mild color vision deficiency."
        else:
            return "Significant variations detected, consider consulting an eye care professional." 
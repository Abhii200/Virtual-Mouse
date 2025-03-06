import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import sys
import signal

# Initialize MediaPipe Hand tracking
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Get webcam
cap = cv2.VideoCapture(0)

# Get screen size
screen_width, screen_height = pyautogui.size()
# Set smoothing factor
smoothing = 0.2  # Reduced smoothing factor for better responsiveness

# Threshold for click detection
click_threshold = 0.04

# Handle system signals
def signal_handler(sig, frame):
    print('Exiting application...')
    cleanup()
    sys.exit(0)

def cleanup():
    print("Cleaning up resources...")
    cap.release()
    cv2.destroyAllWindows()
    hands.close()  # Close MediaPipe resources

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def on_window_close():
    # This function will be called when window close is detected
    cleanup()
    sys.exit(0)

def main():
    prev_x, prev_y = 0, 0
    
    # Create window and set up close callback
    cv2.namedWindow("Hand Tracking")
    
    while True:
        success, img = cap.read()
        if not success:
            break

        # Convert to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process hand detection
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Get index finger tip and thumb tip coordinates
                index_finger = hand_landmarks.landmark[8]
                thumb = hand_landmarks.landmark[4]

                # Convert coordinates to screen position
                x = int((1 - index_finger.x) * screen_width)  # Invert x-coordinate
                y = int(index_finger.y * screen_height)

                # Apply smoothing
                curr_x = int(prev_x + (x - prev_x) * smoothing)
                curr_y = int(prev_y + (y - prev_y) * smoothing)

                # Move cursor
                pyautogui.moveTo(curr_x, curr_y)

                prev_x, prev_y = curr_x, curr_y

                # Calculate distance between thumb and index finger
                distance = np.sqrt((index_finger.x - thumb.x)**2 + (index_finger.y - thumb.y)**2)

                # Trigger click if distance is below threshold
                if distance < click_threshold:
                    pyautogui.click()
                
                # Draw hand landmarks
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Show preview window
        cv2.imshow("Hand Tracking", img)
        
        # Check for key press to exit - note the waitKey timeout is critical
        key = cv2.waitKey(10) & 0xFF
        if key == ord('q') or key == 27:  # 'q' or ESC key
            break
            
        # Also check if window was closed by user
        if cv2.getWindowProperty("Hand Tracking", cv2.WND_PROP_VISIBLE) < 1:
            break

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        cleanup()
        sys.exit(0)  # Force exit
import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import math

# Install mediapipe
# py -3.11 -m pip install mediapi
# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Virtual keyboard keys layout
keys = [
    ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
    
    ["Z", "X", "C", "V", "B", "N", "M", "<", "Space"]
]

def draw_keyboard(frame, highlight_key=None):
    """
    Draws the virtual keyboard on the frame.
    Optionally highlights a key.
    Returns a list of button positions.
    """
    button_list = []
    for i, row in enumerate(keys):
        for j, key in enumerate(row):
            x = j * 70 + 50
            y = i * 80 + 100
            w, h = 65, 65
            color = (0, 255, 0) if highlight_key == (key, x, y, w, h) else (255, 0, 255)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, -1)
            cv2.putText(frame, key, (x + 20, y + 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            button_list.append([key, x, y, w, h])
    return button_list

def get_hovered_key(x8, y8, button_list):
    """
    Returns the key under the index finger tip, if any.
    """
    for key, x, y, w, h in button_list:
        if x < x8 < x + w and y < y8 < y + h:
            return (key, x, y, w, h)
    return None

def is_tap_gesture(x8, y8, x12, y12, threshold=40):
    """
    Returns True if index and middle finger tips are close (tap gesture).
    """
    dist = math.hypot(x8 - x12, y8 - y12)
    return dist < threshold

def main():
    cap = cv2.VideoCapture(0)
    last_press_time = 0
    typed_text = ""
    pressed_key = None
    pressed_time = 0

    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame = cv2.flip(frame, 1)
            # Show pressed key in green for 0.3s
            highlight = pressed_key if pressed_key and (time.time() - pressed_time < 0.3) else None
            button_list = draw_keyboard(frame, highlight_key=highlight)
            hovered_key = None

            # Draw typed text at the top
            cv2.rectangle(frame, (40, 20), (700, 80), (50, 50, 50), -1)
            cv2.putText(frame, typed_text, (60, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (255,255,255), 3)

            # Process image for hand detection
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb_frame)

            if result.multi_hand_landmarks:
                for handLms in result.multi_hand_landmarks:
                    lm_list = []
                    h, w, c = frame.shape
                    for lm in handLms.landmark:
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        lm_list.append((cx, cy))

                    if lm_list:
                        x8, y8 = lm_list[8]   # Index finger tip
                        x12, y12 = lm_list[12]  # Middle finger tip

                        # Show index finger tip
                        cv2.circle(frame, (x8, y8), 8, (0, 255, 255), cv2.FILLED)

                        hovered_key = get_hovered_key(x8, y8, button_list)
                        if hovered_key:
                            # Redraw keyboard with highlighted key
                            button_list = draw_keyboard(frame, highlight_key=hovered_key)
                            key = hovered_key[0]
                            # Tap gesture = index & middle fingers close together
                            if is_tap_gesture(x8, y8, x12, y12) and time.time() - last_press_time > 0.7:
                                last_press_time = time.time()
                                pressed_key = hovered_key
                                pressed_time = time.time()
                                if key == "Space":
                                    typed_text += " "
                                    pyautogui.write(' ')
                                elif key == "<":
                                    typed_text = typed_text[:-1]
                                    pyautogui.press('backspace')
                                else:
                                    typed_text += key
                                    pyautogui.write(key.lower())

                    mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            # Display exit instructions
            cv2.putText(frame, "Press 'q' to exit", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.imshow("Virtual Keyboard", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()




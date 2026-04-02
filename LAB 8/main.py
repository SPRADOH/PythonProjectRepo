import cv2 # type: ignore
import math
import time

def image_processing():
    img = cv2.imread('C:/Users/SPRADOH/Desktop/SPRADOH/PythonProjectRepo/LAB 8/variant-7.jpg')
    

    flipped = cv2.flip(img, -1)
    
    cv2.imshow('Original', img)
    cv2.imshow('Flipped Horizontally and Vertically', flipped)
    
    cv2.imwrite('variant-7_transformed.jpg', flipped)
    
    cv2.waitKey(0)

def video_processing():
    cap = cv2.VideoCapture(0)
    
    
    fly = cv2.imread('C:/Users/SPRADOH/Desktop/SPRADOH/PythonProjectRepo/LAB 8/fly64.png', cv2.IMREAD_UNCHANGED)
    
    # Get fly dimensions
    fly_height, fly_width = fly.shape[:2]
    fly_center_x = fly_width // 2
    fly_center_y = fly_height // 2
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        height, width = frame.shape[:2]
        center_x = width // 2
        center_y = height // 2
        
        cv2.circle(frame, (center_x, center_y), 5, (255, 0, 0), -1)
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(c) > 500:
                x, y, w, h = cv2.boundingRect(c)
                
                marker_x = x + w // 2
                marker_y = y + h // 2
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (marker_x, marker_y), 5, (0, 0, 255), -1)
                
                distance = int(math.sqrt((marker_x - center_x)**2 + (marker_y - center_y)**2))
                
                cv2.putText(frame, f"Distance: {distance} px", (20, 40), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # OVERLAY FLY ON MARKER (Additional Task)
                top_left_x = marker_x - fly_center_x
                top_left_y = marker_y - fly_center_y
                
                # Check if fly fits within frame boundaries
                if (top_left_x >= 0 and top_left_y >= 0 and 
                    top_left_x + fly_width <= width and 
                    top_left_y + fly_height <= height):
                    
                    # Overlay fly with transparency
                    for i in range(fly_height):
                        for j in range(fly_width):
                            if fly[i, j][3] > 0:  # If pixel is not transparent
                                frame[top_left_y + i, top_left_x + j] = fly[i, j][:3]
                
                print(f"Marker: ({marker_x}, {marker_y}), Distance: {distance}")
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.05)
    
    cap.release()

# use comment to toggle which one to process between video and image
if __name__ == '__main__':
    image_processing() 
    #video_processing()
    
    cv2.destroyAllWindows()
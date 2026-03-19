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
                
                print(f"Marker: ({marker_x}, {marker_y}), Distance: {distance}")
        
        cv2.imshow('frame', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        time.sleep(0.05)
    
    cap.release()

if __name__ == '__main__':
    #image_processing()  
    video_processing()  
    
    cv2.destroyAllWindows()
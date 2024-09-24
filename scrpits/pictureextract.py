import cv2
import os

def video_to_frames(video_path, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Capture the video
    vidcap = cv2.VideoCapture(video_path)
    success, image = vidcap.read()
    count = 0
    
    # Loop through the video frames
    while success:
        # Save frame as JPEG file
        cv2.imwrite(os.path.join(output_folder, f"frame{count:04d}.jpg"), image)
        success, image = vidcap.read()
        count += 1
    
    # Release the video capture object
    vidcap.release()
    print(f"Extracted {count} frames to {output_folder}")

# Example usage
video_path = r'C:\Users\DELL\Desktop\IORT\MyProject2 - Unreal Editor 2024-09-24 11-18-31.mp4'
output_folder = r'C:\Users\DELL\Desktop\IORT\pictures'

video_to_frames(video_path, output_folder)

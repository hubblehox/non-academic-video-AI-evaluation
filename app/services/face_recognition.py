import cv2
import random
import os
import numpy as np
from keras_facenet import FaceNet
from mtcnn import MTCNN
from scipy.spatial.distance import euclidean
import shutil

# Initialize the face embedding and detection models
embedder = FaceNet()
detector = MTCNN()

TEMP_FRAMES = r"app/data/temp_frames"
os.makedirs(TEMP_FRAMES, exist_ok=True)

def verify_person_in_video(video_path, output_folder, reference_image_path, threshold=0.2):
    """
    Extracts random frames from a video, compares the detected face in each frame with a reference face,
    and returns True if more than 70% of the processed frames match the reference face.

    Parameters:
        video_path (str): Path to the video file.
        output_folder (str): Folder where frames (or any optional outputs) will be saved.
        reference_image_path (str): Path to the reference image containing the face to compare against.
        threshold (float): Threshold used for determining a match based on Euclidean distance.

    Returns:
        bool: True if at least 70% of the frames match the reference face, else False.
    """
    # Load and process the reference image
    
    reference_img = cv2.imread(reference_image_path)
    if reference_img is None:
        print("Error: Cannot load reference image.")
        return False

    ref_rgb = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)
    ref_faces = detector.detect_faces(ref_rgb)
    if not ref_faces:
        print("Error: No face detected in the reference image.")
        return False

    # Crop the first detected face and compute its embedding
    x, y, w, h = ref_faces[0]['box']
    ref_face = ref_rgb[y:y+h, x:x+w]
    ref_embedding = embedder.embeddings([ref_face])[0]

    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames == 0:
        print("Error: Video has no frames.")
        cap.release()
        return False

    # Determine number of random frames to extract (10% of total frames, at least 1)
    num_frames_to_extract = max(1, total_frames // 100)
    random_frame_indices = sorted(random.sample(range(total_frames), num_frames_to_extract))

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List to store boolean results for each processed frame
    match_results = []

    # Process each selected frame
    for frame_idx in random_frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()
        if not ret:
            print(f"Warning: Could not read frame {frame_idx}")
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb_frame)
        if not faces:
            print(f"Warning: No face detected in frame {frame_idx}")
            match_results.append(False)
            continue

        # For simplicity, use the first detected face in the frame
        x, y, w, h = faces[0]['box']
        face_crop = rgb_frame[y:y+h, x:x+w]
        face_embedding = embedder.embeddings([face_crop])[0]

        # Compute Euclidean distance and determine if it's a match
        distance = euclidean(ref_embedding, face_embedding)
        # Logic: match is True if (1 - distance) > threshold
        match = (1 - distance) > threshold
        match_results.append(match)

        # Optionally save the frame to the output folder
        if match:
            frame_filename = os.path.join(output_folder, f"frame_{frame_idx}_match.jpg")
            # Uncomment the next line to save matching frames:
            # cv2.imwrite(frame_filename, frame)
            print(f"Frame {frame_idx}: MATCH (distance: {distance:.3f})")
        else:
            frame_filename = os.path.join(output_folder, f"frame_{frame_idx}_nomatch.jpg")
            cv2.imwrite(frame_filename, frame)
            print(f"Frame {frame_idx}: NO MATCH (distance: {distance:.3f})")

    cap.release()
    print(f"Processed {len(match_results)} random frames from {video_path}")

    if not match_results:
        print("No valid frames processed.")
        return False

    # Calculate the percentage of frames that match
    match_ratio = sum(match_results) / len(match_results)
    print(f"Match ratio: {match_ratio*100:.2f}%")

    shutil.rmtree(TEMP_FRAMES)
    os.makedirs(TEMP_FRAMES, exist_ok=True)
    # Return True if at least 70% of the frames match, else False
    return {'isSamePerson' :match_ratio >= 0.7}

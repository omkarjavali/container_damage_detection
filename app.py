import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import os
import tempfile
import shutil

# Initialize session state
if "processed_file_path" not in st.session_state:
    st.session_state.processed_file_path = None
if "table_data" not in st.session_state:
    st.session_state.table_data = []
if "file_type" not in st.session_state:
    st.session_state.file_type = None
if "frame_files" not in st.session_state:
    st.session_state.frame_files = []

# Load the YOLOv8 model
model = YOLO("best_yolov8l_72percent.pt")  # Replace with path to your best.pt file or URL

# Create output directory
output_dir = "outputs"
os.makedirs(output_dir, exist_ok=True)

# Streamlit app
st.title("Container Damage Detection")
st.write("Upload an image or video to detect damage. Preview your file below, then process it to view results on a separate page.")

# Upload options
upload_type = st.radio("Select upload type:", ("Image", "Video"))

if upload_type == "Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Process button
        if st.button("Process Image"):
            # Convert to OpenCV format
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Perform inference
            results = model(image_cv)
            
            # Create annotated image
            annotated_image = image_cv.copy()
            detections = results[0].boxes
            table_data = []
            
            for i, box in enumerate(detections):
                xyxy = box.xyxy[0].cpu().numpy()
                class_id = int(box.cls)
                label = model.names[class_id]
                confidence = box.conf.item()
                
                # Draw bounding box and label
                x_min, y_min, x_max, y_max = map(int, xyxy)
                cv2.rectangle(annotated_image, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                cv2.rectangle(
                    annotated_image,
                    (x_min, y_min - label_size[1] - 10),
                    (x_min + label_size[0], y_min),
                    (0, 255, 0),
                    -1
                )
                cv2.putText(
                    annotated_image,
                    label,
                    (x_min, y_min - 5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA
                )
                
                # Store detection details
                table_data.append({
                    "Detection #": i + 1,
                    "Damage Type": label,
                    "Confidence": f"{confidence:.2f}",
                    "Bounding Box": f"[{int(xyxy[0])}, {int(xyxy[1])}, {int(xyxy[2])}, {int(xyxy[3])}]"
                })
            
            # Save annotated image temporarily for results page
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                cv2.imwrite(tmp.name, annotated_image)
                st.session_state.processed_file_path = tmp.name
            st.session_state.table_data = table_data
            st.session_state.file_type = "image"
            st.session_state.frame_files = []  # No frames for images
            
            st.success("Image processed! Go to the **Results** page to view the output.")

elif upload_type == "Video":
    uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "avi", "mov"])
    if uploaded_file is not None:
        # Save video temporarily to display
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
            tmp.write(uploaded_file.read())
            temp_video_path = tmp.name
        
        # Display uploaded video
        st.video(temp_video_path)
        st.caption("Uploaded Video")
        
        # Process button
        if st.button("Process Video"):
            # Open video
            cap = cv2.VideoCapture(temp_video_path)
            if not cap.isOpened():
                st.error("Error opening video file.")
            
            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Create output video path
            video_filename = f"annotated_video_{os.path.basename(uploaded_file.name)}"
            output_video_path = os.path.join(output_dir, video_filename)
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            
            # Progress bar
            progress_bar = st.progress(0)
            frame_count = 0
            frame_files = []
            
            # Process each frame
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Perform inference
                results = model(frame)
                annotated_frame = frame.copy()
                detections = results[0].boxes
                
                # Draw annotations if damage detected
                has_damage = len(detections) > 0
                for box in detections:
                    xyxy = box.xyxy[0].cpu().numpy()
                    class_id = int(box.cls)
                    label = model.names[class_id]
                    x_min, y_min, x_max, y_max = map(int, xyxy)
                    cv2.rectangle(annotated_frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
                    label_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]
                    cv2.rectangle(
                        annotated_frame,
                        (x_min, y_min - label_size[1] - 10),
                        (x_min + label_size[0], y_min),
                        (0, 255, 0),
                        -1
                    )
                    cv2.putText(
                        annotated_frame,
                        label,
                        (x_min, y_min - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        1,
                        cv2.LINE_AA
                    )
                
                # Save frame only if damage detected
                if has_damage:
                    frame_filename = f"frame_{frame_count:04d}.jpg"
                    frame_path = os.path.join(output_dir, frame_filename)
                    cv2.imwrite(frame_path, annotated_frame)
                    frame_files.append(frame_path)
                
                # Write to output video
                out.write(annotated_frame)
                
                # Update progress
                frame_count += 1
                progress_bar.progress(min(frame_count / total_frames, 1.0))
            
            cap.release()
            out.release()
            
            # Clean up temp video
            os.remove(temp_video_path)
            
            # Store video path and frame files for results page
            st.session_state.processed_file_path = output_video_path
            st.session_state.frame_files = frame_files
            st.session_state.file_type = "video"
            st.session_state.table_data = []  # No table for videos
            
            st.success(f"Video processed! Annotated video and damage frames saved in '{output_dir}/'. Go to the **Results** page to view the output.")

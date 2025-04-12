import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

# Load the YOLOv8 model
model = YOLO("best_yolov8l_72percent.pt")  # Replace with the path to your best.pt file

# Streamlit app
st.title("Damage Detection with YOLOv8")
st.write("Upload an image to detect damage. The app will display the annotated image and detailed damage information below.")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Perform inference
    results = model(image_cv)
    
    # Get annotated image
    annotated_image = results[0].plot()  # Draws bounding boxes and labels
    annotated_image_pil = Image.fromarray(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
    
    # Display annotated image
    st.image(annotated_image_pil, caption="Detected Damage", use_column_width=True)
    
    # Extract and display damage data
    detections = results[0].boxes
    if len(detections) > 0:
        st.subheader("Damage Detection Details")
        # Create a table-like output using markdown
        st.markdown("**Detected Damage Data:**")
        table_data = []
        for i, box in enumerate(detections):
            class_name = model.names[int(box.cls)]  # Damage type
            confidence = box.conf.item()  # Confidence score
            xyxy = box.xyxy[0].cpu().numpy()  # Bounding box coordinates [x_min, y_min, x_max, y_max]
            table_data.append({
                "Detection #": i + 1,
                "Damage Type": class_name,
                "Confidence": f"{confidence:.2f}",
                "Bounding Box": f"[{int(xyxy[0])}, {int(xyxy[1])}, {int(xyxy[2])}, {int(xyxy[3])}]"
            })
        
        # Display as a table
        st.table(table_data)
    else:
        st.markdown("**No damage detected.**")
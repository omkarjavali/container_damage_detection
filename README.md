# Damage Detection with YOLOv8

A Streamlit web application for detecting damage in images using a pre-trained YOLOv8 model. Users can upload an image, view the detected damage with labeled bounding boxes (showing only damage types), and see detailed detection data in a table.

## Features
- Upload images (JPG, JPEG, PNG) for damage detection.
- Display annotated images with bounding boxes labeled by damaged.
- Show a table with detection details: Detection #, Damaged, Confidence, and Bounding Box coordinates.
- Built with Streamlit for an interactive web interface.
- Uses a custom YOLOv8 model (`best.pt`) for damage detection.

## Prerequisites
- Python 3.8 or higher
- A trained YOLOv8 model file (`best.pt`) in the project directory
- Git (for cloning the repository)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/omkarjavali/container_damage_detection.git
   cd container_damage_detection
   ```

2. **Create a virtual environment** *(optional but recommended)*:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ensure the YOLOv8 model**:
   - Place your `best.pt` file in the project root or update the path in `app.py` if stored elsewhere.

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

Access the app:
- Open your browser and go to `http://localhost:8501`
- Upload an image to detect damage
- View the annotated image with damage labels and a table of detection details below

## Project Structure
```
your-repo-name/
│
├── home.py              # Main Streamlit application
├── pages
    ├── result.py
├── best.pt              # YOLOv8 model file (not tracked in Git)
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
```

## Notes
- The app assumes `best.pt` outputs bounding boxes with class labels. Adjust `app.py` if your model has a different format.
- For large images, consider adding resizing logic in `app.py` to improve performance.
- To customize the UI (e.g., bounding box colors, table format), modify `app.py`.

## Contributors
- https://github.com/iamsonuram
- https://github.com/D-6503

## Acknowledgments
- Built with Streamlit and Ultralytics YOLOv8.
- Thanks to the open-source community for robust tools!

```


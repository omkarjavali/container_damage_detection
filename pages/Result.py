import streamlit as st
import os
import zipfile

# Streamlit results page
st.title("Damage Detection Results")
st.write("View the processed image or video with detected damage below.")

# Check if there's a processed file
if "processed_file_path" not in st.session_state or st.session_state.processed_file_path is None:
    st.warning("No file processed yet. Go to the Home page to upload an image or video.")
else:
    file_type = st.session_state.file_type
    file_path = st.session_state.processed_file_path
    
    if file_type == "image":
        st.image(file_path, caption="Detected Damage", use_column_width=True)
        
        # Display detection details
        table_data = st.session_state.table_data
        if table_data:
            st.subheader("Damage Detection Details")
            st.markdown("**Detected Damage Data:**")
            st.table(table_data)
        else:
            st.markdown("**No damage detected.**")
        
        # Clean up temporary image
        if os.path.exists(file_path):
            os.remove(file_path)
            st.session_state.processed_file_path = None
    
    elif file_type == "video":
        # Display annotated video
        st.video(file_path)
        
        # Display up to 5 damage frames
        frame_files = st.session_state.get("frame_files", [])
        if frame_files:
            st.subheader("Detected Damage Frames")
            # Limit to first 5 frames
            display_frames = frame_files[:30]
            for frame_path in display_frames:
                st.image(frame_path, caption=f"Damage Frame {os.path.basename(frame_path)}", use_column_width=True)
            if len(frame_files) > 5:
                st.write(f"Showing first 5 of {len(frame_files)} damage frames.")
        else:
            st.markdown("**No damage detected in any frames.**")
        
        # Download button for video
        with open(file_path, "rb") as f:
            st.download_button(
                label="Download Annotated Video",
                data=f,
                file_name=os.path.basename(file_path),
                mime="video/mp4"
            )
        
        # Download button for damage frames (zipped)
        if frame_files:
            zip_path = "damage_frames.zip"
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for frame in frame_files:
                    zipf.write(frame, os.path.basename(frame))
            with open(zip_path, "rb") as f:
                st.download_button(
                    label="Download Damage Frames",
                    data=f,
                    file_name="damage_frames.zip",
                    mime="application/zip"
                )
            if os.path.exists(zip_path):
                os.remove(zip_path)

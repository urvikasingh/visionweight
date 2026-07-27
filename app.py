import streamlit as st
from PIL import Image
from pipeline.detect import detect_object
from pipeline.volume import estimate_volume, estimate_volume_from_pixels
from pipeline.weight import estimate_weight, MATERIAL_DENSITY
from pipeline.calibrate import get_pixels_per_mm

st.set_page_config(page_title="VisionWeight", page_icon="⚖️")

st.title("⚖️ VisionWeight")
st.caption("AI-based object weight estimation — Phase 1 Prototype")

uploaded_file = st.file_uploader("Upload a photo of the object", type=["jpg", "jpeg", "png"])

if uploaded_file:
    temp_path = "data/sample_images/_temp_upload.jpg"
    image = Image.open(uploaded_file).convert("RGB")
    image.save(temp_path)

    st.image(image, caption="Uploaded image", use_container_width=True)

    with st.spinner("Detecting object..."):
        calibration = get_pixels_per_mm(temp_path)
        marker_bbox = calibration["marker_bbox"] if calibration else None
        detection = detect_object(temp_path, exclude_bbox=marker_bbox)

    if detection is None:
        st.error(
            "Couldn't confidently detect a known object. Try a clearer photo, better lighting, or a plainer background.")
    else:
        st.write("DEBUG bbox:", detection["bbox"])
        st.write("DEBUG pixels_per_mm:", calibration["pixels_per_mm"] if calibration else "N/A")
        st.success(
            f"Detected: **{detection['class_name']}** (shape: {detection['shape_category']}, confidence: {detection['confidence']:.0%})")

        use_auto = calibration is not None

        if use_auto:
            st.info(f"✅ Reference marker detected automatically (pixels/mm: {calibration['pixels_per_mm']:.2f})")
        else:
            st.warning("⚠️ No reference marker detected in this photo — falling back to manual entry.")

        st.subheader("Enter measured dimensions" if not use_auto else "Dimensions (auto-calculated, override if needed)")
        col1, col2 = st.columns(2)
        with col1:
            width_mm = st.number_input("Width / diameter (mm)", min_value=1.0, value=70.0)
        with col2:
            height_mm = st.number_input("Height (mm)", min_value=1.0, value=200.0)

        depth_mm = None
        if detection["shape_category"] in ("box", "irregular"):
            depth_mm = st.number_input(
                "Depth / thickness (mm) — optional, leave as 0 to auto-estimate",
                min_value=0.0, value=0.0
            )
            if depth_mm == 0.0:
                depth_mm = None

        material = st.selectbox("Material", options=list(MATERIAL_DENSITY.keys()))
        fill_ratio = st.slider(
            "Fill ratio (1.0 = solid, lower = hollow/shell-like)",
            min_value=0.01, max_value=1.0, value=0.06, step=0.01
        )

        if st.button("Estimate Weight"):
            if use_auto:
                volume_result = estimate_volume_from_pixels(
                    detection["shape_category"], detection["bbox"], calibration["pixels_per_mm"], depth_mm
                )
            else:
                volume_result = estimate_volume(detection["shape_category"], width_mm, height_mm, depth_mm)
            weight_result = estimate_weight(volume_result["volume_mm3"], material, fill_ratio)

            st.subheader("Results")
            c1, c2, c3 = st.columns(3)
            c1.metric("Volume", f"{volume_result['volume_mm3']:,.0f} mm³")
            c2.metric("Estimated Weight", f"{weight_result['weight_g']} g")
            c3.metric("Depth method", volume_result["depth_method"])

            st.caption(
                f"Dimension source: {'automatic (reference marker)' if use_auto else 'manual entry'}. "
                "Fill ratio is operator-estimated in this Phase 1 prototype."
            )
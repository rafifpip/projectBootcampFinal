import streamlit as st
import tempfile
import pandas as pd
import cv2
import plotly.express as px

from pengkodean.detect import detect_image
from pengkodean.statistik import count_classes
from pengkodean.waste_info import WASTE_INFO
from pengkodean.eco_score import (
    calculate_eco_score,
    get_eco_status
)
# from pengkodean.webcam_component import run_webcam

# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="Smart Recycling Assistant",
    page_icon="♻",
    layout="wide"
)

# =====================================
# HEADER
# =====================================

st.markdown("""
# ♻ Smart Recycling Assistant

### AI-Powered Waste Detection and Management System
""")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("♻ Dashboard")

st.sidebar.info("""
Smart Recycling Assistant

YOLOv8 Waste Detection System
""")

# =====================================
# TABS
# =====================================

tab1, tab2 = st.tabs(
    [
        "📁 Upload Image",
        "📸 Take Photo"
    ]
)

# ====================================================
# TAB 1 - UPLOAD IMAGE
# ====================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload a waste image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:

            st.error(
                "File size exceeds 5 MB."
            )

            st.stop()

    if uploaded_file is not None:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as tmp_file:

            tmp_file.write(
                uploaded_file.read()
            )

            temp_path = tmp_file.name

        result_image, detections = detect_image(
            temp_path
        )

        stats = count_classes(
            detections
        )

        eco_score = calculate_eco_score(
            stats
        )

        eco_status = get_eco_status(
            eco_score
        )

        st.sidebar.success(
            f"{len(detections)} objects detected"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📥 Input Image"
            )

            st.image(
                uploaded_file,
                use_container_width=True
            )

        with col2:

            st.subheader(
                "📷 Detection Result"
            )

            st.image(
                result_image,
                channels="BGR",
                use_container_width=True
            )

        st.subheader(
            "♻ Waste Information"
        )

        if len(detections) == 0:

            st.warning(
                "No objects detected."
            )

        else:

            for item in detections:

                class_name = item["class"]

                confidence = item["confidence"]

                info = WASTE_INFO.get(
                    class_name
                )

                with st.container():

                    if "Organic" in class_name:

                        st.success(
                            class_name
                        )

                    elif "Inorganic" in class_name:

                        st.info(
                            class_name
                        )

                    elif "B3" in class_name:

                        st.error(
                            class_name
                        )

                    else:

                        st.write(
                            class_name
                        )

                    st.progress(
                        float(confidence)
                    )

                    st.caption(
                        f"Model Confidence: {confidence:.2%}"
                    )

                    if info:

                        st.write(
                            f"**Description:** {info['description']}"
                        )

                        st.write(
                            f"**Waste Bin:** {info['bin']}"
                        )

                        st.write(
                            f"**Recommendation:** {info['recommendation']}"
                        )

                    else:

                        st.warning(
                            f"Information for '{class_name}' is not available yet."
                        )

                    st.divider()

        st.subheader(
            "♻ Eco Score"
        )

        eco_col1, eco_col2 = st.columns(
            2
        )

        with eco_col1:

            st.metric(
                "Eco Score",
                eco_score
            )

        with eco_col2:

            st.metric(
                "Status",
                eco_status
            )

        st.subheader(
            "📊 Waste Statistics"
        )

        if len(stats) > 0:

            metric_col1, metric_col2 = st.columns(
                2
            )

            with metric_col1:

                st.metric(
                    "Total Detected Objects",
                    sum(stats.values())
                )

            with metric_col2:

                st.metric(
                    "Number of Categories",
                    len(stats)
                )

            df = pd.DataFrame(
                list(stats.items()),
                columns=[
                    "Category",
                    "Count"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            fig = px.pie(
                df,
                values="Count",
                names="Category",
                title="Waste Category Distribution"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            dominant = max(
                stats,
                key=stats.get
            )

            st.info(
                f"""
                The most dominant waste category is
                **{dominant}**
                with a total of
                **{stats[dominant]} objects**.
                """
            )

# ====================================================
# TAB 2 - CAMERA
# ====================================================

with tab2:

    st.subheader(
        "📸 Capture Waste Image"
    )

    camera_on = st.toggle(
        "Enable Camera"
    )

    if camera_on:

        photo = st.camera_input(
            "Take a photo of the waste"
        )

        if photo is not None:

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".jpg"
            ) as tmp_file:

                tmp_file.write(
                    photo.getvalue()
                )

                temp_path = tmp_file.name

            result_image, detections = detect_image(
                temp_path
            )

            st.image(
                result_image,
                channels="BGR",
                use_container_width=True
            )

            st.success(
                f"{len(detections)} objects detected"
            )

    else:

        st.info(
            "Camera is currently disabled."
        )
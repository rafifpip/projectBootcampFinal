import streamlit as st
import cv2
import tempfile
import pandas as pd
import plotly.express as px

from pengkodean.detect import detect_image
from pengkodean.statistik import count_classes
from pengkodean.waste_info import WASTE_INFO
from pengkodean.eco_score import (
    calculate_eco_score,
    get_eco_status
)
from pengkodean.webcam_component import run_webcam

# =====================================
# KONFIGURASI HALAMAN
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

### Sistem Deteksi dan Pengelolaan Sampah Berbasis Artificial Intelligence
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
        "📷 Webcam Realtime"
    ]
)

# ====================================================
# TAB 1 - UPLOAD IMAGE
# ====================================================

with tab1:

    uploaded_file = st.file_uploader(
        "Upload gambar sampah",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:

        max_size = 5 * 1024 * 1024

        if uploaded_file.size > max_size:

            st.error(
                "Ukuran file melebihi 5 MB."
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

        # YOLO Detection

        result_image, detections = detect_image(
            temp_path
        )

        # Statistik

        stats = count_classes(
            detections
        )

        # Eco Score

        eco_score = calculate_eco_score(
            stats
        )

        eco_status = get_eco_status(
            eco_score
        )

        # Sidebar

        st.sidebar.success(
            f"{len(detections)} objek terdeteksi"
        )

        # =====================================
        # INPUT VS OUTPUT
        # =====================================

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📥 Gambar Input"
            )

            st.image(
                uploaded_file,
                use_container_width=True
            )

        with col2:

            st.subheader(
                "📷 Hasil Deteksi"
            )

            st.image(
                cv2.cvtColor(
                    result_image,
                    cv2.COLOR_BGR2RGB
                ),
                use_container_width=True
            )

        # =====================================
        # INFORMASI SAMPAH
        # =====================================

        st.subheader(
            "♻ Informasi Sampah"
        )

        if len(detections) == 0:

            st.warning(
                "Tidak ada objek terdeteksi."
            )

        else:

            for item in detections:

                class_name = item["class"]

                confidence = item["confidence"]

                info = WASTE_INFO.get(
                    class_name
                )

                with st.container():

                    if "Organik" in class_name:

                        st.success(
                            class_name
                        )

                    elif "Anorganik" in class_name:

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
                        f"Tingkat Keyakinan Model: {confidence:.2%}"
                    )

                    if info:

                        st.write(
                            f"**Deskripsi:** {info['description']}"
                        )

                        st.write(
                            f"**Tempat Sampah:** {info['bin']}"
                        )

                        st.write(
                            f"**Rekomendasi:** {info['recommendation']}"
                        )

                    else:

                        st.warning(
                            f"Informasi untuk '{class_name}' belum tersedia."
                        )

                    st.divider()

        # =====================================
        # ECO SCORE
        # =====================================

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

        # =====================================
        # STATISTIK
        # =====================================

        st.subheader(
            "📊 Statistik Sampah"
        )

        if len(stats) > 0:

            metric_col1, metric_col2 = st.columns(
                2
            )

            with metric_col1:

                st.metric(
                    "Total Objek Terdeteksi",
                    sum(stats.values())
                )

            with metric_col2:

                st.metric(
                    "Jumlah Kategori",
                    len(stats)
                )

            df = pd.DataFrame(
                list(stats.items()),
                columns=[
                    "Kategori",
                    "Jumlah"
                ]
            )

            st.dataframe(
                df,
                use_container_width=True
            )

            fig = px.pie(
                df,
                values="Jumlah",
                names="Kategori",
                title="Distribusi Jenis Sampah"
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
                Kategori sampah yang paling dominan adalah
                **{dominant}**
                dengan jumlah
                **{stats[dominant]} objek**.
                """
            )

# ====================================================
# TAB 2 - WEBCAM
# ====================================================

with tab2:

    st.subheader(
        "📷 Webcam Realtime Detection"
    )

    st.write(
        "Klik START untuk mengaktifkan kamera."
    )

    run_webcam()
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer
import av

model = YOLO("model/best.pt")


class VideoProcessor:

    def recv(self, frame):

        img = frame.to_ndarray(
            format="bgr24"
        )

        results = model(img)

        annotated = results[0].plot()

        return av.VideoFrame.from_ndarray(
            annotated,
            format="bgr24"
        )


def run_webcam():

    webrtc_streamer(
        key="waste-camera",
        video_processor_factory=VideoProcessor
    )
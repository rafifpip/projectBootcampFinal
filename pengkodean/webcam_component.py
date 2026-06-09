from ultralytics import YOLO
from streamlit_webrtc import (
    webrtc_streamer,
    RTCConfiguration
)
import av

model = YOLO("model/best.pt")

rtc_configuration = RTCConfiguration(
    {
        "iceServers": [
            {
                "urls": [
                    "stun:stun.l.google.com:19302"
                ]
            }
        ]
    }
)


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
        rtc_configuration=rtc_configuration,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={
            "video": True,
            "audio": False
        }
    )
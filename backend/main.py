from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import mediapipe as mp
from utils import ojo_cerrado, detectar_direccion, draw_fancy_box
import time
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MediaPipe FaceMesh
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

# Initialize FaceMesh once
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6, min_tracking_confidence=0.6)

# Do NOT open the camera at import time. Use CAMERA_SOURCE env var to control source:
# - if CAMERA_SOURCE is an integer string (e.g. '0') it will use that camera index
# - if CAMERA_SOURCE starts with 'file:' it will open the given file path
# - if CAMERA_SOURCE is 'none' (default) the endpoint will return an error explaining the missing source
ultimo_cierre = 0

def gen_frames():
    global ultimo_cierre

    # determine source
    source = os.environ.get('CAMERA_SOURCE', 'none')
    if source == 'none':
        # yield a single error frame (as JPEG) and stop
        import numpy as _np
        err_img = _np.zeros((240, 320, 3), dtype=_np.uint8)
        cv2.putText(err_img, 'No camera source configured', (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        ret, buffer = cv2.imencode('.jpg', err_img)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        return

    # open capture
    if source.startswith('file:'):
        path = source.split(':', 1)[1]
        cap = cv2.VideoCapture(path)
    else:
        try:
            cam_index = int(source)
            cap = cv2.VideoCapture(cam_index)
        except Exception:
            cap = cv2.VideoCapture(source)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            height, width, _ = frame.shape
            results = face_mesh.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            direccion = "Centro"

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

                    if ojo_cerrado(face_landmarks, width, height):
                        if time.time() - ultimo_cierre > 1.2:
                            direccion = "Gracias"
                            ultimo_cierre = time.time()
                    else:
                        direccion = detectar_direccion(face_landmarks, width, height)

            # Dibujar botones
            colores = {"Si": (0,255,0), "No": (0,0,255), "Ayuda": (0,200,200), "Gracias": (255,200,0)}
            draw_fancy_box(frame, (110,20), (230,70), colores["Ayuda"])
            draw_fancy_box(frame, (20,90), (100,150), colores["No"])
            draw_fancy_box(frame, (240,90), (320,150), colores["Si"])
            draw_fancy_box(frame, (110,160), (230,210), colores["Gracias"])

            cv2.putText(frame, f"Mirando: {direccion}", (20,250), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0,255,255), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    finally:
        try:
            cap.release()
        except Exception:
            pass

@app.get("/video_feed")
def video_feed():
    return StreamingResponse(gen_frames(), media_type='multipart/x-mixed-replace; boundary=frame')

@app.get("/")
def root():
    return {"message": "Servidor corriendo. Ve a /video_feed para el streaming"}

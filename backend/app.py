from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import cv2
import mediapipe as mp
import io

app = FastAPI(title="Ocular - Vision API")

# Allow CORS for requests from the frontend web build (adjust origins for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MediaPipe utilities
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh


def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def ojo_cerrado(landmarks, width, height):
    # uses two landmark pairs (approximate) to estimate eyelid distance
    ojo_derecho = [159, 145]
    ojo_izquierdo = [386, 374]
    parpado_derecho = distancia(
        (landmarks.landmark[ojo_derecho[0]].x * width, landmarks.landmark[ojo_derecho[0]].y * height),
        (landmarks.landmark[ojo_derecho[1]].x * width, landmarks.landmark[ojo_derecho[1]].y * height),
    )
    parpado_izquierdo = distancia(
        (landmarks.landmark[ojo_izquierdo[0]].x * width, landmarks.landmark[ojo_izquierdo[0]].y * height),
        (landmarks.landmark[ojo_izquierdo[1]].x * width, landmarks.landmark[ojo_izquierdo[1]].y * height),
    )
    return (parpado_derecho < 4 and parpado_izquierdo < 4)


def detectar_direccion(landmarks, width, height):
    ojo_derecho = [33, 133]
    ojo_izquierdo = [362, 263]
    iris_derecho = 468
    iris_izquierdo = 473

    puntos = {}
    for i in ojo_derecho + ojo_izquierdo + [iris_derecho, iris_izquierdo]:
        x = int(landmarks.landmark[i].x * width)
        y = int(landmarks.landmark[i].y * height)
        puntos[i] = (x, y)

    dx = puntos[iris_izquierdo][0] - np.mean([puntos[362][0], puntos[263][0]])
    dy = puntos[iris_izquierdo][1] - np.mean([puntos[362][1], puntos[263][1]])

    if dx > 5:
        return "Si", float(dx), float(dy)
    elif dx < -5:
        return "no", float(dx), float(dy)
    elif dy < -3:
        return "Ayuda", float(dx), float(dy)
    else:
        return "Centro", float(dx), float(dy)


class DetectResponse(BaseModel):
    direction: str
    eye_closed: bool
    dx: float | None = None
    dy: float | None = None


@app.get("/")
def root():
    return {"status": "ok", "service": "Ocular Vision API"}


@app.post("/detect", response_model=DetectResponse)
async def detect(image: UploadFile = File(...)):
    """Receive an image file (jpeg/png) and return basic gaze detection result."""
    if image.content_type.split("/")[0] != "image":
        raise HTTPException(status_code=400, detail="Invalid content type, expected image/*")

    data = await image.read()
    # Decode image bytes to numpy array
    image_np = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    if frame is None:
        raise HTTPException(status_code=400, detail="Cannot decode image")

    height, width, _ = frame.shape
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.6, min_tracking_confidence=0.6) as face_mesh:
        results = face_mesh.process(frame_rgb)
        if not results.multi_face_landmarks:
            # No faces detected
            return DetectResponse(direction="NoFace", eye_closed=False)

        # For first face only
        face_landmarks = results.multi_face_landmarks[0]
        closed = ojo_cerrado(face_landmarks, width, height)
        direction, dx, dy = detectar_direccion(face_landmarks, width, height)
        return DetectResponse(direction=direction, eye_closed=closed, dx=dx, dy=dy)

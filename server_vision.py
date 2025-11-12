import cv2
import mediapipe as mp
import numpy as np
import os
import base64
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware   # 🧩 Importante para Flutter Web
from datetime import datetime
from io import BytesIO
from PIL import Image
import uvicorn

# ---------------------------------------------------
# ⚙️ Configuración general
app = FastAPI(title="VisionBio Server")

# 🧩 Permitir conexión desde Flutter (localhost o Chrome)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes restringir luego si lo deseas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

carpeta_fotos = os.path.expanduser("~/VisionBioApp/backend_python/capturas")
os.makedirs(carpeta_fotos, exist_ok=True)
print(f"📂 Las fotos se guardarán en: {carpeta_fotos}")

# ---------------------------------------------------
# 🧠 Inicializar MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# ---------------------------------------------------
# 🧮 Funciones
def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

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
        return "Si"
    elif dx < -5:
        return "No"
    elif dy < -3:
        return "Ayuda"
    else:
        return "Centro"

# ---------------------------------------------------
# 🧠 Endpoint principal
@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    direccion = "Centro"
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1)
            )
            direccion = detectar_direccion(face_landmarks, width, height)

    nombre = datetime.now().strftime("foto_%Y%m%d_%H%M%S.jpg")
    ruta = os.path.join(carpeta_fotos, nombre)
    cv2.imwrite(ruta, frame)

    _, buffer = cv2.imencode('.jpg', frame)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return JSONResponse({
        "direccion": direccion,
        "imagen_anotada": img_base64
    })

# ---------------------------------------------------
# 🌐 Endpoint de prueba
@app.get("/")
def home():
    return {"status": "ok", "message": "Servidor VisionBio activo 🚀"}

# ---------------------------------------------------
# 🚀 Iniciar servidor
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

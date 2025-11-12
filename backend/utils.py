import numpy as np
import cv2

def distancia(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

def ojo_cerrado(landmarks, width, height):
    ojo_derecho = [159, 145]
    ojo_izquierdo = [386, 374]
    parpado_derecho = distancia(
        (landmarks.landmark[ojo_derecho[0]].x * width, landmarks.landmark[ojo_derecho[0]].y * height),
        (landmarks.landmark[ojo_derecho[1]].x * width, landmarks.landmark[ojo_derecho[1]].y * height)
    )
    parpado_izquierdo = distancia(
        (landmarks.landmark[ojo_izquierdo[0]].x * width, landmarks.landmark[ojo_izquierdo[0]].y * height),
        (landmarks.landmark[ojo_izquierdo[1]].x * width, landmarks.landmark[ojo_izquierdo[1]].y * height)
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
        return "Si"
    elif dx < -5:
        return "No"
    elif dy < -3:
        return "Ayuda"
    else:
        return "Centro"

def draw_fancy_box(img, top_left, bottom_right, color, thickness=2, r=15):
    x1, y1 = top_left
    x2, y2 = bottom_right
    cv2.rectangle(img, (x1 + r, y1), (x2 - r, y2), color, thickness)
    cv2.rectangle(img, (x1, y1 + r), (x2, y2 - r), color, thickness)
    cv2.circle(img, (x1 + r, y1 + r), r, color, thickness)
    cv2.circle(img, (x2 - r, y1 + r), r, color, thickness)
    cv2.circle(img, (x1 + r, y2 - r), r, color, thickness)
    cv2.circle(img, (x2 - r, y2 - r), r, color, thickness)

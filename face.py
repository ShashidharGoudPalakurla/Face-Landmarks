import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh.
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    min_detection_confidence=0.5, min_tracking_confidence=0.5
)

# Initialize MediaPipe drawing utilities.
mp_drawing = mp.solutions.drawing_utils
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

# Initialize webcam.
cap = cv2.VideoCapture(0)  # 0 for default webcam

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = face_mesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=drawing_spec,
            )
            # You can also draw only specific connections or landmarks if needed.
            #mp_drawing.draw_landmarks(
            #    image=image,
            #    landmark_list=face_landmarks,
            #    connections=mp_face_mesh.FACEMESH_CONTOURS,
            #    landmark_drawing_spec=None,
            #    connection_drawing_spec=drawing_spec
            #)
            #mp_drawing.draw_landmarks(
            #    image=image,
            #    landmark_list=face_landmarks,
            #    connections=mp_face_mesh.FACEMESH_IRISES,
            #    landmark_drawing_spec=None,
            #    connection_drawing_spec=drawing_spec
            #)

    cv2.imshow("MediaPipe Face Mesh", image)
    if cv2.waitKey(5) & 0xFF == 27:  # Press Esc to exit.
        break

cap.release()
cv2.destroyAllWindows()
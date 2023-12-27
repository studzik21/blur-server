import cv2
import mediapipe as mp
import numpy as np


def blur(file, out_file_name):
    cap = cv2.VideoCapture(file)

    mp_face_detection = mp.solutions.face_detection
    face_detection = mp_face_detection.FaceDetection(0.75, 1)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    size = (frame_width, frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter(out_file_name, fourcc, fps, size)

    success, img = cap.read()
    while success:
        results = face_detection.process(img)

        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape

                # For blur box
                bbox_x = max(0, int(bboxC.xmin * iw))
                bbox_y = max(0, int(bboxC.ymin * ih))

                old_width = int(bboxC.width * iw)
                old_height = int(bboxC.height * ih)

                img[bbox_y:min(img.shape[0], bbox_y + old_height), bbox_x:min(img.shape[1], bbox_x + old_width)] = \
                    np.zeros((min(img.shape[0], bbox_y + old_height) - bbox_y,
                              min(img.shape[1], bbox_x + old_width) - bbox_x, 3))

        out.write(img)

        success, img = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()

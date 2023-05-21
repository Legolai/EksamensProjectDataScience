import cv2
from detect import detect
from PIL import Image
import numpy as np


def main() -> None:
    webcam = cv2.VideoCapture(1)
    width = 512
    height = 512

    while True:
        _, frame = webcam.read()

        # Resize to respect the input_shape
        flipped = cv2.flip(frame, 1)
        img = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
        im_pil = Image.fromarray(img)
        detected_image = detect(im_pil, min_score=0.2,
                                max_overlap=0.5, top_k=200)
        im_np = cv2.cvtColor(np.asarray(detected_image), cv2.COLOR_RGB2BGR)
        cv2.imshow('frame', im_np)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == '__main__':
    main()

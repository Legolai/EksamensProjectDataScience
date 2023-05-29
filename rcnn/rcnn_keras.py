# import the necessary packages
from pyimagesearch.iou import compute_iou
from pyimagesearch import config
from bs4 import BeautifulSoup
from imutils import paths
import cv2
import os


def main() -> None:
    """Main function of the program."""
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 420)

    cv2.CascadeClassifier()


if __name__ == "__main__":
    main()

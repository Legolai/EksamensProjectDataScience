import cv2


def main() -> None:
    """Main function of the program."""
    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 420)

    cv2.CascadeClassifier()


if __name__ == "__main__":
    main()

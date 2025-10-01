import cv2
from skimage.metrics import structural_similarity as ssim
import argparse

def get_similarity(frame1_path: str, frame2_path: str):
    img1 = cv2.imread(frame1_path)
    img2 = cv2.imread(frame2_path)

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    result = ssim(gray1, gray2, full=True)

    return result[0]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find frame similarity")

    parser.add_argument(
        "frame1",
        type=str,
        help="The path to the first frame"
    )

    parser.add_argument(
        "frame2",
        type=str,
        help="The path to the second frame"
    )

    args = parser.parse_args()

    score = get_similarity(args.frame1, args.frame2)
    print(f"SSIM: {score:.4f}")  # 1.0 = identical
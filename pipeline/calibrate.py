import cv2
import numpy as np

CARD_WIDTH_MM=85.6
CARD_HEIGHT_MM=53.98
CARD_ASPECT_RATIO=CARD_WIDTH_MM/CARD_HEIGHT_MM


def find_reference_card(image_path,ratio_tolerance=0.15):
    """
    Detects the reference card in the image by finding the rectangular
    contour whose aspect ratio most closely matches a standard card.

    Returns dict: {bbox (x, y, w, h), pixels_per_mm}
    or None if no matching rectangle was found.
    """
    image=cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f'Could not read image: {image_path}')

    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    blurred=cv2.GaussianBlur(gray,(5,5),0)
    edges=cv2.Canny(blurred,50,150)


    kernel=np.ones((5,5),np.uint8)
    closed=cv2.morphologyEx(edges,cv2.MORPH_CLOSE,kernel)

    contours,_=cv2.findContours(closed,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)


    best_match=None
    best_ratio_diff=ratio_tolerance

    for contour in contours:
        x,y,w,h=cv2.boundingRect(contour)

        if w==0 or h==0:
            continue

        ratio=max(w,h)/min(w,h)
        ratio_diff=abs(ratio-CARD_ASPECT_RATIO)


        area=w*h
        if area<1000:
            continue

        if ratio_diff<best_ratio_diff:
            best_ratio_diff=ratio_diff
            best_match=(x,y,w,h)


    if best_match is None:
        return None

    x,y,w,h=best_match

    card_pixel_width=max(w,h)
    pixels_per_mm=card_pixel_width/CARD_WIDTH_MM

    return{
        "bbox":(x,y,w,h),
        "pixels_per_mm":pixels_per_mm
    }





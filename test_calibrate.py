from pipeline.calibrate import get_pixels_per_mm

result = get_pixels_per_mm("data/sample_images/card_bottle.jpeg")
print(result)
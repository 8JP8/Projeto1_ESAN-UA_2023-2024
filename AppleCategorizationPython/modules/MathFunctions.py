import math

def pixels_to_cm(pixels, camera_height_cm, field_of_view_degrees, camera_distance_cm):
    field_of_view_radians = math.radians(field_of_view_degrees)
    cm_per_pixel = (2 * camera_distance_cm * math.tan(field_of_view_radians / 2)) / camera_height_cm
    centimeters = pixels * cm_per_pixel
    return centimeters
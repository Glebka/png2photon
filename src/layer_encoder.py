from color_record import ColorRecord


'''
TODO: optimize the code, it is slow
'''


def encode_layer(src_pixels, src_width, src_height, dest_width, dest_height):
    if src_width > dest_width or src_height > dest_height:
        raise RuntimeError(
            'Source image is out of printer''s LCD screen bounds')
    packed_image = b''
    color_rec = ColorRecord(src_pixels[0, 0])
    for i in range(src_width):
        for j in range(src_height):
            new_color_rec = ColorRecord(src_pixels[i, j])
            if color_rec == new_color_rec:
                if not color_rec.inc():
                    packed_image += color_rec.build()
                    color_rec = new_color_rec
            else:
                packed_image += color_rec.build()
                color_rec = new_color_rec

        for j in range(j + 1, dest_height):
            new_color_rec = ColorRecord((0, 0, 0, 255))
            if color_rec == new_color_rec:
                if not color_rec.inc():
                    packed_image += color_rec.build()
                    color_rec = new_color_rec
            else:
                packed_image += color_rec.build()
                color_rec = new_color_rec

    for i in range(i + 1, dest_width):
        for j in range(dest_height):
            new_color_rec = ColorRecord((0, 0, 0, 255))
            if color_rec == new_color_rec:
                if not color_rec.inc():
                    packed_image += color_rec.build()
                    color_rec = new_color_rec
            else:
                packed_image += color_rec.build()
                color_rec = new_color_rec
    return packed_image

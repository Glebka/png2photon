from construct import *
from construct.lib import *

from config import conf

'''
Photon Mono [SE] file structure: 

+-----------------------+
| PhotonFilePreamble    |
+-----------------------+
| PhotonFileHeader      |
+-----------------------+
| PhotonFilePreview     |
+-----------------------+
| <Preview Image Data>  |  RGB16 format
+-----------------------+
| PhotonLayersDefHeader |
+-----------------------+
| PhotonLayerDef        |
+-----------------------+
| <N-1 layer defs>      |
+-----------------------+
| Layer image data      | Packed format, see PhotonColorRecord struct
+-----------------------+
| <N-1 layer data>      |
+-----------------------+
'''

PhotonColorRecord = BitStruct(
    'color_code' / BitsInteger(4),
    'pixels_count' / IfThenElse(lambda ctx: (ctx.color_code >
                                             0 and ctx.color_code < 0xF), BitsInteger(4), BitsInteger(12))
)

PhotonLayerPixels = GreedyRange(PhotonColorRecord)


PhotonLayerDef = Struct(
    'addr' / Int32ul,                                           # offset to the layer image data (?)
    'size' / Int32ul,                                           # size of the image data (?)
    'z_lift_distance' / Default(Float32l, conf.ZLiftDistance),  # how far the platform moves up in mm
    'z_lift_speed' / Default(Float32l, conf.ZLiftUpSpeed),      # platfrom movement speed in mm/s
    'exp_time' / Default(Float32l, conf.ExposureTime),          # layer exposure time in seconds
    'thikness' / Default(Float32l, conf.LayerThikness),         # layer thikness, mm
    'unknown'  / Const(b'\x00' * 8)                             # Range Start and Range End fields
                                                                # 4 bytes length each
)

PhotonLayersDefHeader = Struct(
    'magic' / Const(b'LAYERDEF\x00\x00\x00\x00'),
    'size' / Int32ul,   # sizeof this struct plus size of all following PhotonLayerDef structs in bytes
    'layers_count' / Int32ul
)

PhotonFileHeader = Struct(
    'magic' / Const(b'HEADER\x00\x00\x00\x00\x00\x00'),
    'len' / Default(Int32ul, 80),                                               # length of this struct in bytes
    'pixel_size' / Default(Float32l, conf.PixelSize),                           # ?
    'layer_thikness' / Default(Float32l, conf.LayerThikness),                   # typical layer thikness, mm
    'normal_exp_time' / Default(Float32l, conf.ExposureTime),                   # exposure time for "normal" layers in seconds
    'uv_off_time' / Default(Float32l, conf.UvOffTime),                          # machine uv light off time in seconds
    'bottom_exp_time' / Default(Float32l, conf.ExposureTime),                   # exposure time for firts N (bottom) layers in seconds
    'bottom_layers' / Default(Float32l, conf.BottomLayers),                     # number of bottom layers
    'z_lift_distance' / Default(Float32l, conf.ZLiftDistance),                  # how far the platform moves up in mm
    'z_lift_up_speed' / Default(Float32l, conf.ZLiftUpSpeed),                   # platfrom up movement speed in mm/s
    'z_lift_down_speed' / Default(Float32l, conf.ZLiftDownSpeed),               # platfrom down movement speed in mm/s
    'volume' / Default(Float32l, 0.0),                                          # calculated 3D model volume
    'anti_aliasing_grade' / Default(Int32sl, conf.AntiAliasingGrade),           # typical values are 1, 2, 4, 8
    'res_x' / Default(Int32ul, conf.ScreenHeight),                              # screen height, px
    'res_y' / Default(Int32ul, conf.ScreenWidth),                               # screen width, px
    'weight' / Default(Float32l, 0),                                            # calculated weight of the model
    'price' / Default(Float32l, 0),                                             # calculated price of the model
    'resin_type' / Default(Int32ul, conf.ResinType),                            # resin type ?
    'use_individual_param' / Default(Int32ul, conf.UseIndividualLayerParams),   # 1 - use params from PhotonLayerDef; 0 - use params defined here
    'reserved' / Const(b'\x00' * 12),                                           # ?
)

PhotonFilePreview = Struct(
    'magic' / Const(b'PREVIEW\x00\x00\x00\x00\x00'),
    'size' / Default(Int32ul, conf.PreviewWidth * conf.PreviewHeight *      # struct + preview image data size
                     2 + 12 + 4 + 4 + 4 + 4),
    'width' / Default(Int32ul, conf.PreviewWidth),                          # preview image width, px
    'unknown' / Default(Array(4, Byte), [42, 0, 0, 0]),                     # ?
    'height' / Default(Int32ul, conf.PreviewHeight),                        # preview image height
    'data' / Const(b'\x00' * (conf.PreviewWidth * conf.PreviewHeight * 2))  # blank preview data
)

PhotonFilePreamble = Struct(
    'magic' / Const(b'ANYCUBIC\x00\x00\x00\x00'),
    'version' / Default(Int32ul, 1),                                    # file version
    'area_num' / Default(Int32ul, 0),                                   # ?
    'header_addr' / Default(Int32ul, 0x30),                             # offset to the PhotonFileHeader struct from the beginning of the file
    'reserved1' / Const(0, Int32ul),                                    # ?
    'preview_addr' / Const(0x30 + PhotonFileHeader.sizeof(), Int32ul),  # offset to the PhotonFilePreview struct from the beginning of the file
    'reserved2' / Const(0, Int32ul),                                    # ? 
    'layersdef_addr' / Default(Int32ul, 0),                             # offset to the PhotonLayersDefHeader struct from the beginning of the file
    'reserved3' / Const(0, Int32ul),                                    # ?
    'layers_image_addr' / Default(Int32ul, 0),                          # offset to the first layer image from the beginning of the file
)


__all__ = ['PhotonLayerDef', 'PhotonLayersDefHeader', 'PhotonFileHeader', 
    'PhotonFilePreview', 'PhotonFilePreamble', 'PhotonColorRecord', 'PhotonLayerPixels']
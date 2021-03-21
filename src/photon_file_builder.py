from PIL import Image
from structs import PhotonFilePreamble, PhotonFileHeader, PhotonFilePreview, PhotonLayersDefHeader, PhotonLayerDef
from layer_encoder import encode_layer


class PhotonFileBuilder(object):
    def __init__(self):
        super().__init__()

    def _build_header(self):
        return PhotonFileHeader.build({})

    def _build_preview(self):
        return PhotonFilePreview.build({})

    def _build_layers_def_header(self):
        return PhotonLayersDefHeader.build({
            'layers_count': 1,
            'size': PhotonLayersDefHeader.sizeof() + PhotonLayerDef.sizeof()
        })

    def _build_layer_def(self, packed_layer_size):
        return PhotonLayerDef.build({
            'addr': PhotonFilePreamble.sizeof() + PhotonFileHeader.sizeof() + PhotonFilePreview.sizeof()
            + PhotonLayersDefHeader.sizeof() + PhotonLayerDef.sizeof(),
            'size': packed_layer_size,
        })

    def _build_preamble(self):
        layersdef_addr = PhotonFilePreamble.sizeof() + PhotonFileHeader.sizeof() + \
            PhotonFilePreview.sizeof()
        return PhotonFilePreamble.build({
            'layersdef_addr': layersdef_addr,
            'layers_image_addr': layersdef_addr + PhotonLayersDefHeader.sizeof() + PhotonLayerDef.sizeof()
        })

    def build_photon_file(self, src_image_file, output_file):
        pil_image = Image.open(src_image_file)
        pixels_matrix = pil_image.load()
        layer_data = encode_layer(
            pixels_matrix, pil_image.size[0], pil_image.size[1], 2560, 1620)
        with open(output_file, 'wb') as out:
            out.write(self._build_preamble())
            out.write(self._build_header())
            out.write(self._build_preview())
            out.write(self._build_layers_def_header())
            out.write(self._build_layer_def(len(layer_data)))
            out.write(layer_data)

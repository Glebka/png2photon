from structs import PhotonColorRecord
from struct import pack


class ColorRecord(object):

    def __init__(self, rgba):
        super().__init__()
        if rgba[0] == 0 and rgba[1] == 0 and rgba[2] == 0:
            self.code = 0
        else:
            self.code = 0xF
        self.count = 1

    def __eq__(self, value):
        return self.code == value.code

    def inc(self):
        if self.count < 0xFFF:
            self.count += 1
            return True
        return False

    def build(self):
        return PhotonColorRecord.build({
            'color_code': self.code,
            'pixels_count': self.count
        })

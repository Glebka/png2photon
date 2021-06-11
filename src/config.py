import configparser
from os import path


class Config(object):

    def __init__(self):
        super().__init__()
        self._config = configparser.ConfigParser()
        self._config['DEFAULT'] = {
            'LayerThikness': 0.05, # mm
            'UvOffTime': 0.5,
            'ExposureTime': 40.0,
            'BottomLayers': 1.0,
            'ZLiftDistance': 0.0,
            'ZLiftUpSpeed': 4.0,
            'ZLiftDownSpeed': 6.0,
            'AntiAliasingGrade': 1,
            'PixelSize': 51.0,      # mm * 10^-3
            'ScreenWidth': 2560,    # px
            'ScreenHeight': 1620,   # px
            'OutFileExt': '.pwms',
            'ResinType': 42434,
            'UseIndividualLayerParams': 0,
            'PreviewWidth': 224,    # px
            'PreviewHeight': 168,   # px
            'OffsetX': 5.0,         # mm
            'OffsetY': 5.0          # mm
        }

        self._data_types = {
            'LayerThikness': float,
            'UvOffTime': float,
            'ExposureTime': float,
            'BottomLayers': float,
            'ZLiftDistance': float,
            'ZLiftUpSpeed': float,
            'ZLiftDownSpeed': float,
            'AntiAliasingGrade': int,
            'PixelSize': float,
            'ScreenWidth': int,
            'ScreenHeight': int,
            'OutFileExt': str,
            'ResinType': int,
            'UseIndividualLayerParams': int,
            'PreviewWidth': int,
            'PreviewHeight': int,
            'OffsetX': float,
            'OffsetY': float
        }

    def load_file(self, config_file):
        absolute_path = path.abspath(config_file)
        if path.exists(absolute_path):
            self._config.read(absolute_path)
            return True
        return False

    def __getattr__(self, name):
        section_name = 'DEFAULT'
        if 'PresetName' in self._config[section_name]:
            section_name = self._config[section_name]['PresetName']
        config_section = self._config[section_name]
        data_type = self._data_types.get(name, str)
        return data_type(config_section[name])


conf = Config()

__all__ = ['conf']

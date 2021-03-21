import argparse
from os import path
from config import conf

def main():
    parser = argparse.ArgumentParser(description='Converts given image into a file for DLP 3D printers of Anycubic Photon SE / Mono / Mono SE family')
    parser.add_argument('-c', '--conf', type=str, help='Config file to load')
    parser.add_argument('-o', '--output', type=str, help='Output photon file')
    parser.add_argument('input', type=str, help='Input image file to process')
    args = parser.parse_args()
    if not args.output:
        file_path, ext = path.splitext(args.input)
        args.output = path.basename(file_path) + '.pwms'
    
    if not args.conf:
        args.conf = 'config.ini'

    conf.load_file(args.conf)
    
    from photon_file_builder import PhotonFileBuilder
    builder = PhotonFileBuilder()
    builder.build_photon_file(args.input, args.output)


if __name__ == "__main__":
    main()


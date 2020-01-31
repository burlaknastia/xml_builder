import json
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser

from src.helpers import convert_data
from src.utils import xml_builder, create_tag_with_children

example = {
    "widget": {
        "debug": "on",
        "window": {
            "title": "Sample Konfabulator Widget",
            "name": "main_window",
            "width": 500,
            "height": 500
        },
        "image": {
            "src": "Images/Sun.png",
            "name": "sun1",
            "hOffset": 250,
            "vOffset": 250,
            "alignment": "center"
        },
        "text": {
            "data": "Click Here",
            "size": 36,
            "style": "bold",
            "name": "text1",
            "hOffset": 250,
            "vOffset": 100,
            "alignment": "center",
            "onMouseUp": "sun1.opacity = (sun1.opacity / 100) * 90;"
        }
    }}

# TODO: чтение из файла
parser = ArgumentParser(description="Convert JSON to xml string. "
                                    "Use only one option.")
parser.add_argument('-i', '--input', dest='input', type=json.loads,
                    help='Convert a JSON string in xml string')
parser.add_argument('--test', dest='test-sample', action='store_true',
                    help='Use built-in example for building xml string')

args = parser.parse_args()


def main():
    payload = vars(args)
    if payload.get('test-sample') and payload.get('input') is not None:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if payload.get('test-sample'):
        converted_payload = convert_data(example)
    else:
        converted_payload = create_tag_with_children(payload['input'],
                                                     'test_sample')
    xml_payload = xml_builder(converted_payload)
    xml_received = ET.tostring(xml_payload).decode()
    # вывод результата
    sys.stdout.write(xml_received)
    sys.stdout.write('\n')


if __name__ == "__main__":
    main()

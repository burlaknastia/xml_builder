import json
import sys
import typing as t
import xml.etree.ElementTree as ET
from argparse import ArgumentParser
from dataclasses import dataclass, field

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


@dataclass
class XMLTag:
    tag: str
    children: t.List['XMLTag'] = field(default_factory=list)
    attrs: t.List[t.Tuple[str, str]] = field(default_factory=list)
    value: t.Optional[str] = None


def create_tag_with_children(payload: dict,
                             label: str,
                             attributes: t.Optional[
                                 t.List[t.Tuple[str, str]]] = None) \
        -> XMLTag:
    payload_tag = XMLTag(tag=label)
    if attributes is not None:
        payload_tag.attrs = attributes
    for key, value in payload.items():
        if isinstance(value, dict):
            payload_tag.children.append(create_tag_with_children(value, key))
        else:
            child_tag = XMLTag(tag=key, value=str(value))
            payload_tag.children.append(child_tag)
    return payload_tag


def xml_builder(xml_tag: XMLTag) -> ET.Element:
    elem = ET.Element(xml_tag.tag)
    for attr in xml_tag.attrs:
        elem.set(*attr)
    for child in xml_tag.children:
        elem.append(xml_builder(child))
    elem.text = xml_tag.value
    return elem


def convert_data(data: dict) -> XMLTag:
    widget = data.get('widget')
    widget_tag = XMLTag(tag='widget')
    debug_tag = XMLTag(tag='debug', value=widget.get('debug'))
    widget_tag.children.append(debug_tag)

    window = widget.get('window')
    window_tag = create_tag_with_children(window, "window",
                                          [("title", window.pop('title', ''))])
    widget_tag.children.append(window_tag)

    image = widget.get('image')
    image_attrs = [
        ("src", image.pop('src')),
        ("name", image.pop('name')),
    ]
    image_tag = create_tag_with_children(image, "image", image_attrs)
    widget_tag.children.append(image_tag)

    text = widget.get('text')
    text_attrs = [
        ("data", text.pop('data')),
        ("size", str(text.pop('size'))),
        ("style", str(text.pop('style'))),
    ]
    text_tag = create_tag_with_children(text, "text", text_attrs)
    widget_tag.children.append(text_tag)

    return widget_tag


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

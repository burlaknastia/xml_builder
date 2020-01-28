import typing as t

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

xml_expected = """<widget><debug>on</debug><window title="Sample Konfabulator Widget"><name>main_window</name><width>500</width><height>500</height></window><image src="Images/Sun.png" name="sun1"><hOffset>250</hOffset><vOffset>250</vOffset><alignment>center</alignment></image><text data="Click Here" size="36" style="bold"><name>text1</name><hOffset>250</hOffset><vOffset>100</vOffset><alignment>center</alignment><onMouseUp>sun1.opacity = (sun1.opacity / 100) * 90;</onMouseUp></text></widget>"""

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
    window_tag = create_tag_with_children(window, "window", [("title", window.pop('title', ''))])
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


def main():
    converted_payload = convert_data(example)
    xml_payload = xml_builder(converted_payload)
    xml_recieved = ET.tostring(xml_payload).decode()
    print(xml_recieved)
    assert len(xml_expected) == len(xml_recieved)

if __name__ == "__main__":
    main()

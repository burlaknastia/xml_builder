import typing as t
import xml.etree.ElementTree as ET

from src.models import XMLTag

# TODO: создание атрибутов сразу


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

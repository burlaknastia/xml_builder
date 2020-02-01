import typing as t
import xml.etree.ElementTree as ET

from src.models import XMLTag


def create_tag(payload: t.Union[dict, list],
               label: t.Optional[str] = None,
               attributes_labels: t.Optional[t.List[str]] = None) -> XMLTag:

    tags = __create_tag_recursive(payload, attributes_labels)
    if label is not None or isinstance(payload, list):
        payload_tag = XMLTag(tag=label)
        payload_tag.children = tags
    else:
        payload_tag = tags[0]
    return payload_tag


def __create_tag_recursive(payload: t.Union[dict, list],
                           attributes_labels: t.Optional[t.List[str]] = None) \
        -> t.List[XMLTag]:
    tags = list()
    attr_values = list()
    if isinstance(payload, dict):
        if attributes_labels is not None:
            # поиск аттриубутов из указанного списка
            attr_values = __get_attributes(attributes_labels, payload)
        for key, value in payload.items():
            tag = XMLTag(tag=key, attrs=attr_values)
            children = __create_tag_recursive(value, attributes_labels)
            if len(children) == 0:
                # когда в качестве значений передается массив
                # строк/чисел, создается n тегов со значением ключа
                if isinstance(value, list):
                    tags += [XMLTag(tag=key, value=str(v)) for v in value]
                    continue
                tag.value = str(value)
            else:
                tag.children = children
            tags.append(tag)
    elif isinstance(payload, list):
        for item in payload:
            tags += __create_tag_recursive(item, attributes_labels)
    return tags


def __get_attributes(attributes_labels: t.List[str],
                     payload: dict) -> t.List[t.Tuple[str, str]]:
    attr_values = list()
    for attr in attributes_labels:
        if payload.get(attr) is not None:
            attr_values.append((attr, str(payload.pop(attr))))
    return attr_values


def xml_builder(xml_tag: XMLTag) -> ET.Element:
    elem = ET.Element(xml_tag.tag)
    for attr in xml_tag.attrs:
        elem.set(*attr)
    for child in xml_tag.children:
        elem.append(xml_builder(child))
    elem.text = xml_tag.value
    return elem

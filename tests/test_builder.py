import xml.etree.ElementTree as ET

import pytest

from src.models import XMLTag
from src.utils import xml_builder, create_tag

"""
Тесты основных функций `create_tag_with_children` 
и `xml_builder` (to be continued)
"""


def test_create_tag():
    """
    Проверка создания тега типа ``XMLTag``
    """
    payload = {
        'sample': {
            'test_tag': 'tag_value'
        }
    }
    xml_tag = create_tag(payload)
    expected_tag = XMLTag(tag='sample',
                          children=[
                              XMLTag(tag='test_tag', value='tag_value')
                          ])
    assert xml_tag == expected_tag


def test_create_tag_with_attr():
    """
    Проверка создания тега типа ``XMLTag`` с атрибутами
    """
    payload = {
        'sample': {
            'test_tag': 'tag_value',
            'test_attr': 'attr_value'
        }
    }

    xml_tag = create_tag(payload, attributes_labels=['test_attr'])
    expected_tag = XMLTag(tag='sample',
                          children=[
                              XMLTag(tag='test_tag', value='tag_value',
                                     attrs=[('test_attr', 'attr_value')], )
                          ])
    assert xml_tag == expected_tag


def test_xml_builder():
    """
    Проверка создания элемента `XML`
    """
    xml_tag = XMLTag(tag='sample',
                     children=[
                         XMLTag(tag='test_tag', value='tag_value')
                     ])
    xml_payload = xml_builder(xml_tag)
    xml_received = ET.tostring(xml_payload).decode()
    xml_expected = "<sample><test_tag>tag_value</test_tag></sample>"
    assert xml_received == xml_expected


def test_xml_builder_with_attrs():
    """
    Проверка создания элемента `XML` с атрибутами
    """
    xml_tag = XMLTag(tag='sample',
                     attrs=[('test_attr', 'attr_value')],
                     children=[
                         XMLTag(tag='test_tag', value='tag_value')
                     ])
    xml_payload = xml_builder(xml_tag)
    xml_received = ET.tostring(xml_payload).decode()
    xml_expected = '<sample test_attr="attr_value"><test_tag>tag_value' \
                   '</test_tag></sample>'
    assert xml_received == xml_expected


@pytest.fixture
def load_json_sample():
    import json
    with open('tests/test.json', 'r') as f:
        return json.load(f)


def test_xml_from_fixture(load_json_sample):
    """
    Проверка полной сборки примера с массивом значений

    :param load_json_sample: JSON пример
    :return:
    """
    payload = load_json_sample
    xml_tag = create_tag(payload)
    xml_payload = xml_builder(xml_tag)
    xml_received = ET.tostring(xml_payload).decode()
    xml_expected = '<test_sample><test><tag1>value1</tag1><tag2>value2</tag2>' \
                   '<tag3>value3</tag3><tag3>value4</tag3></test><attr1>attr1' \
                   '</attr1><attr2>attr2</attr2><attr3>attr3</attr3>' \
                   '</test_sample>'
    assert xml_received == xml_expected


def test_xml_with_attrs_from_fixture(load_json_sample):
    """
    Проверка полной сборки примера с массивом значений и
    с использоваением атрибутов

    :param load_json_sample: JSON пример
    :return:
    """
    payload = load_json_sample
    xml_tag = create_tag(payload, attributes_labels=['attr1', 'attr2', 'attr3'])
    xml_payload = xml_builder(xml_tag)
    xml_received = ET.tostring(xml_payload).decode()
    xml_expected = '<test_sample><test attr1="attr1" attr2="attr2" ' \
                   'attr3="attr3"><tag1>value1</tag1><tag2>value2</tag2>' \
                   '<tag3>value3</tag3><tag3>value4</tag3></test></test_sample>'
    assert xml_received == xml_expected


def test_xml_with_label_from_fixture(load_json_sample):
    """
    Проверка полной сборки примера с массивом значений,
    с использоваением атрибутов и указанием верхнеуровнего тэга

    :param load_json_sample: JSON пример
    :return:
    """
    payload = load_json_sample
    xml_tag = create_tag(payload, label='main_tag',
                         attributes_labels=['attr1', 'attr2', 'attr3'])
    xml_payload = xml_builder(xml_tag)
    xml_received = ET.tostring(xml_payload).decode()
    xml_expected = '<main_tag><test_sample><test attr1="attr1" attr2="attr2" ' \
                   'attr3="attr3"><tag1>value1</tag1><tag2>value2</tag2><tag3>' \
                   'value3</tag3><tag3>value4</tag3></test></test_sample>' \
                   '</main_tag>'
    assert xml_received == xml_expected

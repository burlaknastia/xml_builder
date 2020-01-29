import xml.etree.ElementTree as ET

from main import create_tag_with_children, XMLTag, xml_builder

"""
Модульные тесты основных функций `create_tag_with_children` 
и `xml_builder` (to be continued)
"""


def test_create_tag():
    """
    Проверка создания тега типа ``XMLTag``
    """
    payload = {
        'test_tag': 'tag_value'
    }
    xml_tag = create_tag_with_children(payload, "sample")
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
        'test_tag': 'tag_value'
    }
    attrs = [('test_attr', 'attr_value')]
    xml_tag = create_tag_with_children(payload, "sample", attrs)
    expected_tag = XMLTag(tag='sample',
                          attrs=attrs,
                          children=[
                              XMLTag(tag='test_tag',  value='tag_value')
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

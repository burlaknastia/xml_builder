from src.models import XMLTag
from src.utils import create_tag_with_children


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

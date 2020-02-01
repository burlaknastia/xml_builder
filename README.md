# xml_builder

#### Конвертация данных `JSON` в формат `xml`.

---

Скрипт предоставляет возможность задать атрибуты из конвертируемого объекта, а также задать значение верхнеуровневого тэга, если `JSON` представляет собой массив объектов. Чтение данных возможно как из файла, так и из консоли.

---

Запуск `xml_bulder` осуществляется через консоль с использованием различных параметров (подробнее в help message `--help`).

Пример запуска:
    
    python3 main.py -i '{"test_tag": "tag_value"}' > output.xml
    python3 main.py -r test.json -a attr1 attr2 attr3 -o output.xml
    python3 main.py < test.json -l main_tag > output.xml

Для тестирования функционала используется `pytest`.

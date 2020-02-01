import json
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, FileType

from src.utils import xml_builder, create_tag

parser = ArgumentParser(description="Convert JSON object to XML format. You "
                                    "can either read object from JSON file or "
                                    "type it to console input. Also, it is "
                                    "possible to define attributes in future "
                                    "XML. Use only one input option.")
parser.add_argument('-r', '--read', dest='read_file', type=FileType('r'),
                    help="Read JSON data from file.")
parser.add_argument('-o', '--output',
                    help="Directs the output to the user's path. Optional "
                         "argument, you can use '>' instead.")
parser.add_argument('-i', '--input', metavar="INPUT_CONSOLE", type=json.loads,
                    help='Read a JSON string from console.')
parser.add_argument('-a', '--attributes', nargs='*',
                    help="Array of JSON keys to use as attribute labels in XML.")
parser.add_argument('-l', '--label',
                    help="Define top level tag label. Required, if JSON top "
                         "level is a list, or filename would be used.")

args = parser.parse_args()


def main():
    if args.read_file is not None and args.input is not None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.read_file is not None:
        with args.read_file as file:
            try:
                payload = json.load(file)
            except ValueError as e:
                sys.stdout.write(e)
                sys.exit(1)
    else:
        payload = args.input

    label = args.label
    if args.label is None and isinstance(payload, list):
        label = args.read_file.name if args.read_file is not None else "input"
    converted_payload = create_tag(payload, label, args.attributes)
    xml_payload = xml_builder(converted_payload)
    # вывод результата
    output = args.output if args.output is not None else sys.stdout
    ET.ElementTree(xml_payload).write(output,
                                      encoding='unicode',
                                      xml_declaration=True)


if __name__ == "__main__":
    main()

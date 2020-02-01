import json
import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, FileType

from src.utils import xml_builder, create_tag

parser = ArgumentParser(description="Convert JSON to XML string. "
                                    "Use only one input option.")
parser.add_argument('-a', '--attributes', nargs='*',
                    help="Array of JSON keys to use as attribute labels in XML")
parser.add_argument('-i', '--input', type=json.loads,
                    help='Read a JSON string from console')
parser.add_argument('-r', '--read', dest='read_file', type=FileType('r'),
                    help="Read JSON data from file")
parser.add_argument('-o', '--output',
                    help="Directs the output to the user's path. Optional "
                         "argument, you can use '>' instead")

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
    converted_payload = create_tag(payload, attributes_labels=args.attributes)
    print(converted_payload)
    xml_payload = xml_builder(converted_payload)
    built_xml = ET.tostring(xml_payload).decode()

    # вывод результата
    if args.output is not None:
        sys.stdout = open(args.output, 'w')
    sys.stdout.write(built_xml)
    sys.stdout.write('\n')
    if args.output is not None:
        sys.stdout.close()


if __name__ == "__main__":
    main()

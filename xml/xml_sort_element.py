import xml.etree.ElementTree as ET


def sort_xml_elements(element):
    if element.text:
        element.text = element.text.strip() or None
    
    if element.tail:
        element.tail = element.tail.strip() or None

    for child in element:
        sort_xml_elements(child)

    children = [child for child in element if isinstance(child.tag, str)]

    if len(children) > 1:
        children.sort(key = lambda child: child.tag.lower())

        for child in children:
            element.remove(child)
        
        for child in children:
            element.append(child)

def sort_xml_file(input_path, output_path):
    ET.register_namespace('', 'specify-your-uri')

    tree = ET.parse(input_path)

    root = tree.getroot()
    sort_xml_elements(root)
    ET.indent(tree, space = "    ")

    tree.write(output_path, encoding = "utf-8", xml_declaration = False)

    print("File sorted successfully.")


if __name__ == "__main__":
    input_path = input("Enter the path of the input XML file: ")
    output_path = input_path[:-len(".xml")] + ".sorted.xml"
    sort_xml_file(input_path, output_path)

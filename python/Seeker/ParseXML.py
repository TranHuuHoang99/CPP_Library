from xml.etree import ElementTree
import os

class ParseXML:
    def __init__(self, xml_path) -> None:
        self.xml_path = xml_path

    def extract_data(self):
        root_path = os.path.abspath(os.path.dirname(__file__))
        xml_file = os.path.join(root_path, self.xml_path)
        xml_tree = ElementTree.parse(xml_file)
        xml_root = xml_tree.getroot()

        count = 0
        for data in xml_root.findall('.//'):
            for subdata in data.findall('.'):
                if subdata.tag == '{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE':
                    for sub in subdata.findall('.'):
                        print(sub.tag)

xml_obj = ParseXML('raw_data/CheryFR_Dem_Customer_EcucValues.arxml')
xml_obj.extract_data()
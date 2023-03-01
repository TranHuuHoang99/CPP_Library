from lxml import etree
import os


class ParseXML:
    def __init__(self, arxml_path) -> None:
        self.arxml_path = arxml_path

    def extract_data(self):
        root_path = os.path.abspath(os.path.dirname(__file__))
        arxml_file = os.path.join(root_path, self.arxml_path)
        arxml_tree = etree.parse(arxml_file)

        data = "//*[local-name() = 'ECUC-CONTAINER-VALUE']/*[local-name() = 'SHORT-NAME']/text()"
        data_parsed = arxml_tree.xpath(data)

        return data_parsed
    

arxml_obj = ParseXML('raw_data/CheryFR_Dem_Customer_EcucValues.arxml')
for DTCName in arxml_obj.extract_data():
    print(DTCName)


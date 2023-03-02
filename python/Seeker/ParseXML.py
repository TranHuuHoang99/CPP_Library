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

        Dtc_temp = []

        for data in xml_root.findall('.//'):
            if data.tag == "{http://autosar.org/schema/r4.0}ECUC-CONTAINER-VALUE" and \
                data.find('./').text == "DTC_ADC_SELF_TEST_FAILURE":
                Dtc_temp.append(data)

        for data in Dtc_temp[0].findall('.//'):
            if data.tag == "{http://autosar.org/schema/r4.0}ECUC-NUMERICAL-PARAM-VALUE":
                for subdata in data.findall('./'):
                    if subdata.tag == "{http://autosar.org/schema/r4.0}VALUE":
                        subdata.text = "D91832"

        ElementTree.register_namespace("", "http://autosar.org/schema/r4.0")

        xml_tree.write(xml_file, encoding='UTF-8', xml_declaration=True)
            


xml_obj = ParseXML('raw_data/CheryFR_Dem_Customer_EcucValues.arxml')
xml_obj.extract_data()
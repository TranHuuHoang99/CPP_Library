from BCTARXMLParser.etree import ElementTree
import os

class ParseXML:
    def __init__(self, xml_path) -> None:
        self.xml_path = xml_path

        self.root_path = os.path.abspath(os.path.dirname(__file__))
        self.xml_file = os.path.join(self.root_path, self.xml_path)
        self.xml_tree = ElementTree.parse(self.xml_file)
        self.xml_root = self.xml_tree.getroot()

        self.NAMESPACE = "http://autosar.org/schema/r4.0"
        self.SCHEMALOCATION = "http://autosar.org/schema/r4.0 autosar_4-2-2.xsd"
        self.ENDLINE_CMT = "<!-- Last modified by AEEE-Pro_2019.1.1 - BCT -->"

    def cfg_Namespace(self, namespace: str):
        self.NAMESPACE = namespace
    
    def cfg_Schemalocation(self, schemalocation: str):
        self.SCHEMALOCATION = schemalocation

    def cfg_EndlineCmt(self, Endline_cmt: str):
        self.ENDLINE_CMT = Endline_cmt

    def extract_DTC(self, DTC_name):
        self.Dtc_found = []

        for data in self.xml_root.findall('.//'):
            if data.tag == "{%s}ECUC-CONTAINER-VALUE"%(self.NAMESPACE) and \
                data.find('./').text == DTC_name:
                self.Dtc_found.append(data)

        print("Invalid DTC name !!!")

    def set_DTCId_value(self, DTC_value: str):
        if self.Dtc_found == []:
            return

        for data in self.Dtc_found[0].findall('.//'):
            if data.tag == "{%s}ECUC-NUMERICAL-PARAM-VALUE"%(self.NAMESPACE):
                for subdata in data.findall('./'):
                    if subdata.tag == "{%s}VALUE"%(self.NAMESPACE):
                        subdata.text = "%s"%(DTC_value)

    def start_gen_BCT(self):
        ElementTree.register_namespace("", self.NAMESPACE)
        self.xml_tree.register_schemalocation(self.SCHEMALOCATION)
        self.xml_tree.write(self.xml_file, encoding="UTF-8", xml_declaration=True)

        endline_iso = ['', '%s'%(self.ENDLINE_CMT), '']

        with open(self.xml_file, "a") as f:
            f.write('\n'.join(endline_iso))

    def __isDTCExisted(self, DTC_name):
        self.extract_DTC(DTC_name=DTC_name)
        return True if self.Dtc_found != [] else False

    def __extract_DTC_container(self):
        self.DTC_Fault_container = []
        for container in self.xml_root.findall('.//'):
            if container.tag == "{%s}ECUC-CONTAINER-VALUE"%(self.NAMESPACE)\
                and container.find('./').text == "DemConfigSet":
                for subcontainer in container.findall('./'):
                    if subcontainer.tag == "{%s}SUB-CONTAINERS"%(self.NAMESPACE):
                        self.DTC_Fault_container.append(subcontainer)

    def insert_DTC(self, name:str, severity, value: str, Priority: str):
        if self.__isDTCExisted(DTC_name=name):
            print("DTC name already existed please choose other methodto config DTC properties")
            return

        print("INSERTING NEW DTC TO BCT ...")

        self.Default_DTC = '\n\
              <ECUC-CONTAINER-VALUE>\n\
               <SHORT-NAME>%s</SHORT-NAME>\n\
               <DEFINITION-REF DEST="ECUC-PARAM-CONF-CONTAINER-DEF">/AUTOSAR_Dem/EcucModuleDefs/Dem/DemConfigSet/DemDTC</DEFINITION-REF>\n\
               <PARAMETER-VALUES>\n\
                <ECUC-TEXTUAL-PARAM-VALUE>\n\
                 <DEFINITION-REF DEST="ECUC-ENUMERATION-PARAM-DEF">/AUTOSAR_Dem/EcucModuleDefs/Dem/DemConfigSet/DemDTC/DemDTCSeverity</DEFINITION-REF>\n\
                 <VALUE>%s</VALUE>\n\
                </ECUC-TEXTUAL-PARAM-VALUE>\n\
                <ECUC-NUMERICAL-PARAM-VALUE>\n\
                 <DEFINITION-REF DEST="ECUC-INTEGER-PARAM-DEF">/AUTOSAR_Dem/EcucModuleDefs/Dem/DemConfigSet/DemDTC/DemDtcValue</DEFINITION-REF>\n\
                 <VALUE>%s</VALUE>\n\
                </ECUC-NUMERICAL-PARAM-VALUE>\n\
               </PARAMETER-VALUES>\n\
               <REFERENCE-VALUES>\n\
                <ECUC-REFERENCE-VALUE>\n\
                 <DEFINITION-REF DEST="ECUC-REFERENCE-DEF">/AUTOSAR_Dem/EcucModuleDefs/Dem/DemConfigSet/DemDTC/DemDTCAttributesRef</DEFINITION-REF>\n\
                 <VALUE-REF DEST="ECUC-CONTAINER-VALUE">/RB/UBK/Project/EcucModuleConfigurationValuess/Dem/DemConfigSet/DemDTCAttributes_Priority%s</VALUE-REF>\n\
                </ECUC-REFERENCE-VALUE>\n\
               </REFERENCE-VALUES>\n\
              </ECUC-CONTAINER-VALUE>\n\
        '%(name,severity,value, Priority)

        new_Dtc = ElementTree.fromstring(self.Default_DTC)
        self.__extract_DTC_container()
        self.DTC_Fault_container[0].append(new_Dtc)
        ElementTree.indent(self.DTC_Fault_container[0], space=' ', level=13)

        print("Done!!!")
        
            

xml_obj = ParseXML('C:/Users/TOH4HC/Documents/SAMPLE_TASK/fr5cp_fm_sampletask/apl/chery/cubas/cfg/common/Diagnosis/Dem/CheryFR_Dem_Customer_EcucValues.arxml')
xml_obj.insert_DTC(
    name="DTC_VBAT_HIGHH",
    severity="",
    value="0xFFFFF",
    Priority="2"
)
xml_obj.start_gen_BCT()
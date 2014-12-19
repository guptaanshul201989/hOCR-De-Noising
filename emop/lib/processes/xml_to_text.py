import collections
import os
import xml.etree.ElementTree as ET
from emop.lib.processes.processes_base import ProcessesBase


class XML_To_Text(ProcessesBase):

    def __init__(self, job):
        super(self.__class__, self).__init__(job)

    def run(self):
        Results = collections.namedtuple('Results', ['stdout', 'stderr', 'exitcode'])

        if not self.idhmc_xml_file or not os.path.isfile(self.idhmc_xml_file):
            stderr = "XML to Text: Could not find XML file"
            return Results(stdout=None, stderr=stderr, exitcode=1)

        xml = ET.parse(self.idhmc_xml_file)

        lines = xml.findall(".//*[@class='ocr_line']")
        lines_text = []
        for line in lines:
            words = line.findall(".//*[@class='ocrx_word']")
            words_list = []
            for word in words:
                text = word.text or ""
                for sub_ele in word:
                    text += ET.tostring(sub_ele, encoding="utf-8", method="text")
                words_list.append(text)
            line_text = " ".join(filter(None, words_list))
            lines_text.append(line_text)

        text = "\n".join(lines_text)
        print text

        with open(self.idhmc_txt_file, 'w') as txt_file:
            txt_file.write(text)

        return Results(stdout=None, stderr=None, exitcode=0)

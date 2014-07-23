#!/usr/bin/env python3

from lxml import etree

class TrafficFileParser:

    def get_traffic_settings(self, file_name, traffic_id):
        search_expression = "//config/[@id='" + str(traffic_id) + "']"
        document = etree.parse(file_name)
        result = document.findall(search_expression)

        if len(result) == 1:
            return result[0].attrib

        return {}

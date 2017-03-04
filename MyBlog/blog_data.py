# -*- coding: utf-8 -*-


class TagData:
    def __init__(self, tag_id, tag_name, tag_li_list):
        self.tag_id = tag_id
        self.tag_href = "#"+tag_id
        self.tag_name = tag_name
        self.tag_li_list = tag_li_list
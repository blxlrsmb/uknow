#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# $File: base.py
# $Date: Sat Dec 14 16:11:20 2013 +0800
# $Author: jiakai <jia.kai66@gmail.com>

"""
Serialization format:
descriptor_name + SERIALIZATION_SEP + descriptor.serialze()
"""

from abc import ABCMeta, abstractmethod

SERIALIZATION_SEP = '\x23'


class ItemDescBaseMeta(ABCMeta):
    def __new__(cls, name, base, attr):
        obj = super(ItemDescBaseMeta, cls).__new__(cls, name, base, attr)
        if name != 'ItemDescBase':
            desc_name = obj.get_desc_name()
            assert SERIALIZATION_SEP not in desc_name, \
                'bad desc name: ' + desc_name
            assert desc_name not in ItemDescBase._desc_mapper, \
                'multiple item descriptors have same name: ' + desc_name
            ItemDescBase._desc_mapper[desc_name] = obj

        return obj


class ItemDescBase(object):
    """Description of an item.
    Each item has a description, which could be used, for example, to render
    this item to HTML to be displayed as an entry on a webpage.
    Multiple description types are allowed, each having a unique name."""

    __metaclass__ = ItemDescBaseMeta

    _desc_mapper = dict()
    """desc name => desc class"""

    @abstractmethod
    def _do_serialize(self):
        """serialize to binary, to be stored in database; plain text should be
        preserved to help search. Text should be encoded as UTF-8"""

    @abstractmethod
    def _do_deserialize(cls, data):
        """classmethod to deserialize"""

    @abstractmethod
    def get_desc_name(self):
        """return a string, denoting the descriptor type;
        this should be a class method, and return value should be constant"""

    @abstractmethod
    def render_title(self):
        """render the title of this desc as human-readable text"""

    @abstractmethod
    def render_content(self):
        """render the contetn of this desc as human-readable text"""

    def serialize(self):
        return self.get_desc_name() + SERIALIZATION_SEP + self._do_serialize()

    @classmethod
    def deserialize(cls, data):
        name, data = data.split(SERIALIZATION_SEP, 1)
        itm_cls = cls._desc_mapper.get(name)
        if itm_cls:
            return itm_cls._do_deserialize(data)

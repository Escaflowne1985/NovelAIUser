# -*- coding: utf-8 -*-
# 文件大小类
from django.utils import six

if six.PY3:
    long = int


class FileSize():
    SIZE_UNIT = {
        "Byte": 1, "KB": 1024, "MB": 1048576,
        "GB": 1073741824, "TB": 1099511627776
    }

    def __init__(self, size):
        self.size = long(FileSize.Format(size))

    @staticmethod
    def Format(size):
        import re
        if isinstance(size, six.integer_types):
            return size
        else:
            if not isinstance(size, six.string_types):
                return 0
            else:
                oSize = size.lstrip().upper().replace(" ", "")
                pattern = re.compile(
                    r"(\d*\.?(?=\d)\d*)(byte|kb|mb|gb|tb)", re.I)
                match = pattern.match(oSize)
                if match:
                    m_size, m_unit = match.groups()
                    if m_size.find(".") == -1:
                        m_size = long(m_size)
                    else:
                        m_size = float(m_size)
                    if m_unit != "BYTE":
                        return m_size * FileSize.SIZE_UNIT[m_unit]
                    else:
                        return m_size
                else:
                    return 0

    # 返回字节为单位的值
    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, newsize):
        try:
            self._size = long(newsize)
        except:
            self._size = 0

    # 返回带单位的自动值
    @property
    def FriendValue(self):
        if self.size < FileSize.SIZE_UNIT["KB"]:
            unit = "Byte"
        elif self.size < FileSize.SIZE_UNIT["MB"]:
            unit = "KB"
        elif self.size < FileSize.SIZE_UNIT["GB"]:
            unit = "MB"
        elif self.size < FileSize.SIZE_UNIT["TB"]:
            unit = "GB"
        else:
            unit = "TB"

        if (self.size % FileSize.SIZE_UNIT[unit]) == 0:
            return "%s%s" % ((self.size / FileSize.SIZE_UNIT[unit]), unit)
        else:
            return "%0.2f%s" % (round(float(self.size) / float(
                FileSize.SIZE_UNIT[unit]), 2), unit)

    def __str__(self):
        return self.FriendValue

    # 相加
    def __add__(self, other):
        if isinstance(other, FileSize):
            return FileSize(other.size + self.size)
        else:
            return FileSize(FileSize(other).size + self.size)

    def __sub__(self, other):
        if isinstance(other, FileSize):
            return FileSize(self.size - other.size)
        else:
            return FileSize(self.size - FileSize(other).size)

    def __gt__(self, other):
        if isinstance(other, FileSize):
            if self.size > other.size:
                return True
            else:
                return False
        else:
            if self.size > FileSize(other).size:
                return True
            else:
                return False

    def __lt__(self, other):
        if isinstance(other, FileSize):
            if other.size > self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size > self.size:
                return True
            else:
                return False

    def __ge__(self, other):
        if isinstance(other, FileSize):
            if self.size >= other.size:
                return True
            else:
                return False
        else:
            if self.size >= FileSize(other).size:
                return True
            else:
                return False

    def __le__(self, other):
        if isinstance(other, FileSize):
            if other.size >= self.size:
                return True
            else:
                return False
        else:
            if FileSize(other).size >= self.size:
                return True
            else:
                return False

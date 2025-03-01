# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from collections import OrderedDict as odict  # noqa: F401
from itertools import chain
import os
from shlex import split
import sys
from tempfile import NamedTemporaryFile

from .._vendor.six import (  # noqa: F401
    integer_types,
    iteritems,
    iterkeys,
    itervalues,
    string_types,
    text_type,
    wraps,
)

NoneType = type(None)
primitive_types = tuple(chain(string_types, integer_types, (float, complex, bool, NoneType)))


def isiterable(obj):
    # and not a string
    try:
        from collections.abc import Iterable
    except ImportError:
        from collections import Iterable
    return not isinstance(obj, string_types) and isinstance(obj, Iterable)


# shlex.split() is a poor function to use for anything general purpose (like calling subprocess).
# It mishandles Unicode in Python 3 but all is not lost. We can escape it, then escape the escapes
# then call shlex.split() then un-escape that.
def shlex_split_unicode(to_split, posix=True):
    # shlex.split does its own un-escaping that we must counter.
    e_to_split = to_split.replace("\\", "\\\\")
    return split(e_to_split, posix=posix)


def utf8_writer(fp):
    return fp


def Utf8NamedTemporaryFile(
    mode="w+b", buffering=-1, newline=None, suffix=None, prefix=None, dir=None, delete=True
):
    if "CONDA_TEST_SAVE_TEMPS" in os.environ:
        delete = False
    if "CONDA_USE_PREFIX_TEMP" in os.environ:
        if dir is None:
            dir = os.path.join(sys.prefix, "tmp")
            os.makedirs(dir, exist_ok=True)
    encoding = None
    if "b" not in mode:
        encoding = "utf-8"
    return NamedTemporaryFile(
        mode=mode,
        buffering=buffering,
        encoding=encoding,
        newline=newline,
        suffix=suffix,
        prefix=prefix,
        dir=dir,
        delete=delete,
    )

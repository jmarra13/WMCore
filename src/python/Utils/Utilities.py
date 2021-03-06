#! /usr/bin/env python

from __future__ import division, print_function

import subprocess
import os
import re
import zlib
import base64

def makeList(stringList):
    """
    _makeList_

    Make a python list out of a comma separated list of strings,
    throws a ValueError if the input is not well formed.
    If the stringList is already of type list, then return it untouched.
    """
    if isinstance(stringList, list):
        return stringList
    if isinstance(stringList, basestring):
        toks = stringList.lstrip(' [').rstrip(' ]').split(',')
        if toks == ['']:
            return []
        return [str(tok.strip(' \'"')) for tok in toks]
    raise ValueError("Can't convert to list %s" % stringList)


def makeNonEmptyList(stringList):
    """
    _makeNonEmptyList_

    Given a string or a list of strings, return a non empty list of strings.
    Throws an exception in case the final list is empty or input data is not
    a string or a python list
    """
    finalList = makeList(stringList)
    if not finalList:
        raise ValueError("Input data cannot be an empty list %s" % stringList)
    return finalList


def strToBool(string):
    """
    _strToBool_

    Try to convert a string to boolean. i.e. "True" to python True
    """
    if string in [False, True]:
        return string
    elif string in ["True", "true", "TRUE"]:
        return True
    elif string in ["False", "false", "FALSE"]:
        return False
    raise ValueError("Can't convert to bool: %s" % string)


def safeStr(string):
    """
    _safeStr_

    Cast simple data (int, float, basestring) to string.
    """
    if not isinstance(string, (tuple, list, set, dict)):
        return str(string)
    raise ValueError("We're not supposed to convert %s to string." % string)


def diskUse():
    """
    This returns the % use of each disk partition
    """
    diskPercent = []
    df = subprocess.Popen(["df", "-klP"], stdout=subprocess.PIPE)
    output = df.communicate()[0].split("\n")
    for x in output:
        split = x.split()
        if split != [] and split[0] != 'Filesystem':
            diskPercent.append({'mounted': split[5], 'percent': split[4]})

    return diskPercent


def numberCouchProcess():
    """
    This returns the number of couch process
    """
    ps = subprocess.Popen(["ps", "-ef"], stdout=subprocess.PIPE)
    process = ps.communicate()[0].count('couchjs')

    return process


def rootUrlJoin(base, extend):
    """
    Adds a path element to the path within a ROOT url
    """
    if base:
        match = re.match("^root://([^/]+)/(.+)", base)
        if match:
            host = match.group(1)
            path = match.group(2)
            newpath = os.path.join(path, extend)
            newurl = "root://%s/%s" % (host, newpath)
            return newurl
    return None


def zipEncodeStr(message, maxLen=5120, compressLevel=9, steps=100, truncateIndicator=" (...)"):
    """
    _zipEncodeStr_
    Utility to zip a string and encode it.
    If zipped encoded length is greater than maxLen,
    truncate message until zip/encoded version
    is within the limits allowed.
    """
    encodedStr = zlib.compress(message, compressLevel)
    encodedStr = base64.b64encode(encodedStr)
    if len(encodedStr) < maxLen or maxLen == -1:
        return encodedStr

    compressRate = 1. * len(encodedStr) / len(base64.b64encode(message))

    # Estimate new length for message zip/encoded version
    # to be less than maxLen.
    # Also, append truncate indicator to message.
    strLen = int((maxLen - len(truncateIndicator)) / compressRate)
    message = message[:strLen] + truncateIndicator

    encodedStr = zipEncodeStr(message, maxLen=-1)

    # If new length is not short enough, truncate
    # recursively by steps
    while len(encodedStr) > maxLen:
        message = message[:-steps - len(truncateIndicator)] + truncateIndicator
        encodedStr = zipEncodeStr(message, maxLen=-1)

    return encodedStr

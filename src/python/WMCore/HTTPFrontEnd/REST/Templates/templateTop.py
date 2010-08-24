#!/usr/bin/env python




##################################################
## DEPENDENCIES
import sys
import os
import os.path
from os.path import getmtime, exists
import time
import types
import __builtin__
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import DummyTransaction
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
try:
    True, False
except NameError:
    True, False = (1==1), (1==0)
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.0.1'
__CHEETAH_versionTuple__ = (2, 0, 1, 'final', 0)
__CHEETAH_genTime__ = 1229648252.2574601
__CHEETAH_genTimestamp__ = 'Thu Dec 18 19:57:32 2008'
__CHEETAH_src__ = 'Templates/tmpl/templateTop.tmpl'
__CHEETAH_srcLastModified__ = 'Thu Dec 18 16:44:32 2008'
__CHEETAH_docstring__ = 'Autogenerated by CHEETAH: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class templateTop(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        Template.__init__(self, *args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write('''<!-- templateTop.tmpl -->
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head profile="http://www.w3.org/2005/11/profile">
<title>RESTofUs</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta http-equiv="Content-Language" content="en-us" />
<meta name="author" content="Valentin Kuznetsov (vkuznet at gmail dot com)" />
<meta name="MSSmartTagsPreventParsing" content="true" />
<meta name="ROBOTS" content="ALL" />
<meta name="Copyright" content="(CC) 2008, CMS collaboration." />
<meta http-equiv="imagetoolbar" content="no" />
<meta name="Rating" content="General" />
<link rel="icon" 
      type="image/png" 
      href="''')
        _v = VFFSL(SL,"host",True) # '${host}' on line 16, col 13
        if _v is not None: write(_filter(_v, rawExpr='${host}')) # from line 16, col 13.
        write('''/images/CMSLogo.png" />
<link rel="stylesheet" type="text/css" href="/css/rest.css" />
<style type="text/css">div.normalcontent { display:none }</style>
<script type="text/javascript">
function SetMain() {
  var id=document.getElementById("main");
  if (id) {
      id.className="main";
  }
}
</script>
</head>
<body onload="''')
        _v = VFFSL(SL,"onload",True) # '$onload' on line 28, col 15
        if _v is not None: write(_filter(_v, rawExpr='$onload')) # from line 28, col 15.
        write('''" id="content">

<noscript>
<h1 class="box_red">Warning:</h1>
<table width="50%" class="main">
<tr>
<td>
<div class="sectionhead_tight">REST page
is AJAX enabled and require that your browser have scripting 
enabled and JavaScript support. Your browser either does not support JavaScript, 
or it has JavaScript support disabled. Please enable JavaScript support or 
use a different browser with JavaScript support to use this page.
</div>
</td>
</tr>
</table>
</noscript>

<div id="main" class="hide">
<script type="text/javascript">SetMain()</script>

<!-- end of templateTop.tmpl -->
''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_templateTop= 'respond'

## END CLASS DEFINITION

if not hasattr(templateTop, '_initCheetahAttributes'):
    templateAPIClass = getattr(templateTop, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(templateTop)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=templateTop()).run()



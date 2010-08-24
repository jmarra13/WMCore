#!/usr/bin/env python
#pylint: disable-msg=E1101,E1103,C0103,R0902
"""
Defines default config values for errorhandler specific
parameters.
"""
__all__ = []
__revision__ = "$Id: DefaultConfig.py,v 1.3 2009/02/06 10:15:37 fvlingen Exp $"
__version__ = "$Revision: 1.3 $"


from WMCore.Agent.Configuration import Configuration

config = Configuration()
config.component_("ErrorHandler")
#The log level of the component. 
config.ErrorHandler.logLevel = 'DEBUG'
#The namespace of the component
config.ErrorHandler.namespace = 'WMComponent.ErrorHandler.ErrorHandler'
# maximum number of threads we want to deal
# with messages per pool.
config.ErrorHandler.maxThreads = 30
# maximum number of retries we want for job
config.ErrorHandler.maxRetries = 10
# depending on the application an operator can reconfigure what we use.
# but these are the default settings.
config.ErrorHandler.submitFailureHandler = \
    'WMComponent.ErrorHandler.Handler.DefaultSubmit'
config.ErrorHandler.createFailureHandler = \
    'WMComponent.ErrorHandler.Handler.DefaultCreate'
config.ErrorHandler.runFailureHandler = \
    'WMComponent.ErrorHandler.Handler.DefaultRun'


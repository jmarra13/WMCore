#!/usr/bin/env python
"""
Poll request manager for new work
"""
__all__ = []



import re
import os
import os.path
import time

from WMCore.WorkerThreads.BaseWorkerThread import BaseWorkerThread
from WMCore.WMSpec.WMWorkload import WMWorkloadHelper
from WMCore.WorkQueue.Policy.End import endPolicy
from WMCore.WorkQueue.WorkQueueExceptions import WorkQueueWMSpecError, WorkQueueNoWorkError

class WorkQueueManagerReqMgrPoller(BaseWorkerThread):
    """
    Polls for requests
    """
    def __init__(self, reqMgr, queue, config):
        """
        Initialise class members
        """
        BaseWorkerThread.__init__(self)
        self.reqMgr = reqMgr
        self.wq = queue
        self.config = config

    def algorithm(self, parameters):
        """
        retrive workload (workspec) from RequestManager
	    """
        self.wq.logger.info("Contacting Request manager for more work")
        work = 0
        workLoads = []
        try:
            workLoads = self.retrieveWorkLoadFromReqMgr()
        except Exception, ex:
            workLoads = {}
            msg = "Error contacting RequestManager: %s" % str(ex)
            self.wq.logger.warning(msg)
        if workLoads:
            self.wq.logger.debug(workLoads)
            #TODO: Same functionality as WorkQueue.pullWork() - combine
            for team, reqName, workLoadUrl in workLoads:
                try:
                    #TO: maybe better to do bulk status update outside the loop.
                    self.reqMgr.reportRequestStatus(reqName, "negotiating")
                except Exception, ex:
                    self.wq.logger.error("""
                        Unable to update ReqMgr state to negotiating: %s
                        Ignoring this request: %s""" % (str(ex), reqName))
                    continue

                try:
                    self.wq.logger.info("Processing request %s" % reqName)
                    wmspec = WMWorkloadHelper()
                    wmspec.load(workLoadUrl)

                    units = self.wq._splitWork(wmspec)

                    # Process each request in a transaction - isolate bad req's
                    with self.wq.transactionContext() as trans:
                        if self.wq._insertWMSpec(wmspec):
                        # check whether there is duplicate wmspec. 
                        # If there is, log the error message and continue 
                        # inside transaction so nothing is inserted on error
                            msg = "Error: Duplicate wmspec: %s, ignore request"
                            self.wq.logger.error(msg % wmspec.name())
                            self.wq.rollbackTransaction(trans)
                            continue

                        for unit in units:
                            self.wq._insertWorkQueueElement(unit, reqName,
                                                            team)
                        try:
                            self.reqMgr.putWorkQueue(reqName, 
                                            self.config.get('QueueURL', 'No Queue'))
                        except Exception, ex:
                            self.wq.logger.error("Unable to update ReqMgr state: %s" % str(ex))
                            self.wq.logger.error('Request "%s" not queued' % reqName)
                            self.wq.rollbackTransaction(trans)

                    work += len(units)
                except (WorkQueueWMSpecError, WorkQueueNoWorkError), ex:
                    # fatal error - report back to ReqMgr
                    self.wq.logger.error("Permanent failure processing request %s - %s" % (reqName, str(ex)))
                    self.wq.logger.error("Marking request %s as failed in ReqMgr" % reqName)
                    self.reportRequestStatusToReqMgr(reqName, 'failed', message = str(ex))
                except Exception, ex:
                    #TODO: Improve this to handle intermittent (dbs/phedex down etc.) failures
                    self.wq.logger.exception("Error processing request %s" % reqName)
                    self.reportRequestStatusToReqMgr(reqName, 'failed', message = str(ex))
                
            self.wq.logger.info("There is new work, update location info")     
            self.wq.updateLocationInfo(newDataOnly = True)

        self.logger.info("%s element(s) obtained from RequestManager" % work)

        try:
            self.reportToReqMgr()
        except:
            self.wq.logger.exception("Error caught during RequestManager update")
        return


    def retrieveCondition(self):
        """
        _retrieveCondition_
        set true or false for given retrieve condion
        i.e. thredshod on workqueue 
        """
        return True

    def retrieveWorkLoadFromReqMgr(self):
        """
        retrieveWorkLoad
        retrieve list of url for workloads.
        """
        results = []
        for team in self.wq.params['Teams']:
            temp = self.reqMgr.getAssignment(team)
            results.extend([(team, y, z) for y, z in temp.items()])
        return results

    # Reuse this when bulk updates supported
#    def sendConfirmationToReqMgr(self, requestNames):
#        """
#        """
#        #TODO: allow bulk post
#        for requestName in requestNames:
#            result = self.reqMgr.postAssignment(requestName)

    def reportToReqMgr(self):
        """Report request status to ReqMgr"""
        now = int(time.time())
        updated = []

        elements = self.wq.statusReqMgrUpdateNeeded(dictKey = "RequestName")
        elements = [endPolicy(group,
                             self.wq.params['EndPolicySettings']) for \
                             group in elements.values()]
        if not elements:
            return

        for ele in elements:
            status = self.reqMgrStatus(ele)

            try:
                reported_back = self.reportRequestStatusToReqMgr(ele['RequestName'], status)

                if ele['PercentComplete'] or ele['PercentSuccess']:
                    args = {'percent_complete' : ele['PercentComplete'],
                            'percent_success' : ele['PercentSuccess']}
                    self.reqMgr.reportRequestProgress(ele['RequestName'],
                                                      **args)

            except Exception, ex:
                msg = 'Error updating ReqMgr about request "%s": %s'
                self.wq.logger.warning(msg % (ele['RequestName'], str(ex)))
            else:
                if reported_back:
                    updated.append(ele)

        if updated:
            updated_elements = sum([], *[x['Elements'] for x in updated])
            self.wq.setReqMgrUpdate(now, *[y['Id'] for y in updated_elements])

            self.wq.deleteFinisedWork(updated)

    def reportRequestStatusToReqMgr(self, request, status, message = None):
        """Change state in RequestManager
           Optionally, take a message to append to the request"""
        try:
            if status:
                self.reqMgr.reportRequestStatus(request, status)
            if message:
                self.reqMgr.sendMessage(request, str(message))
        except Exception, ex:
            self.wq.logger.error("Unable to report to ReqMgr: %s" % str(ex))
            return False
        return True

    def reqMgrStatus(self, ele):
        """Map WorkQueue Status to that reported to ReqMgr"""
        statusMapping = {'Acquired' : 'running',
                         'Failed' : 'failed',
                         'Canceled' : 'aborted',
                         'Done' : 'completed'
                         }
        if statusMapping.has_key(ele.status()):
            return statusMapping[ele.status()]
        else:
            return None

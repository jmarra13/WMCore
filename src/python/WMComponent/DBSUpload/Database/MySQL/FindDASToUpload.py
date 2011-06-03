#!/usr/bin/env python

"""
This code should load the necessary information regarding
dataset-algo combinations from the DBSBuffer.

"""




from WMCore.Database.DBFormatter import DBFormatter


class FindDASToUpload(DBFormatter):
    """
    Find Uploadable DAS

    """


    sql = """SELECT DISTINCT das.dataset_id AS dataset, ds.Path as Path, das.algo_id as Algo, das.in_dbs as in_dbs,
               das.id AS das_id,
               da.app_name AS ApplicationName, 
               da.app_ver AS ApplicationVersion, 
               da.app_fam AS ApplicationFamily, 
               da.PSet_Hash as PSetHash,
               da.Config_Content as PSetContent,
               da.in_dbs AS algo_in_dbs,
               ds.valid_status AS valid_status,
               ds.global_tag AS global_tag
             FROM dbsbuffer_algo_dataset_assoc das
             INNER JOIN dbsbuffer_dataset ds ON ds.id = das.dataset_id
             INNER JOIN dbsbuffer_algo da ON da.id = das.algo_id
             WHERE EXISTS (SELECT id FROM dbsbuffer_file dbsfile
                            WHERE dbsfile.dataset_algo = das.id
                            AND dbsfile.status = 'NOTUPLOADED')
             AND UPPER(ds.Path) NOT LIKE 'BOGUS'
             """


    def makeDAS(self, results):
        ret=[]
        for r in results:
            entry={}
            entry['Path']=r['path']
            entry['DAS_ID'] = long(r['das_id'])
            if not r['algo'] == None:
                entry['Algo'] = int(r['algo'])
            else:
                entry['Algo'] = None
            if not r['algo_in_dbs'] == None:
                entry['AlgoInDBS'] = int(r['algo_in_dbs'])
            else:
                entry['AlgoInDBS'] = None
            if not r['in_dbs'] == None:
                entry['DASInDBS'] = int(r['in_dbs'])
            else:
                entry['DASInDBS'] = None
            path = r['path']
            entry['PrimaryDataset']     = path.split('/')[1]
            entry['ProcessedDataset']   = path.split('/')[2]
            entry['DataTier']           = path.split('/')[3]
            entry['ApplicationName']    = r['applicationname']
            entry['ApplicationVersion'] = r['applicationversion']
            entry['ApplicationFamily']  = r['applicationfamily']
            entry['PSetHash']           = r['psethash']
            entry['PSetContent']        = r['psetcontent']
            entry['Dataset']            = r['dataset']
            entry['ValidStatus']        = r['valid_status']
            entry['GlobalTag']          = r.get('global_tag', '')
            ret.append(entry)

        return ret


    def execute(self, conn=None, transaction = False):

        binds  = {}
        result = self.dbi.processData(self.sql, binds, 
                         conn = conn, transaction = transaction)
        
        return self.makeDAS(self.formatDict(result))

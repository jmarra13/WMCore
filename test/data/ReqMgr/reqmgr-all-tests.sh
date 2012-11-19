py test/data/ReqMgr/reqmgr.py -u https://localhost:2000 -c ~/tmp/caltech/grid_certificate/2012-usercert.pem -k ~/tmp/caltech/grid_certificate/2012-userkey-passphraseless.pem -f ./test/data/ReqMgr/requests/MonteCarlo.json  --json '{"createRequest": {"Requestor": "maxa"}, "assignRequest": {"Team": "dmwm"}}' --allTests && \
py test/data/ReqMgr/reqmgr.py -u https://localhost:2000 -c ~/tmp/caltech/grid_certificate/2012-usercert.pem -k ~/tmp/caltech/grid_certificate/2012-userkey-passphraseless.pem -f ./test/data/ReqMgr/requests/MonteCarloFromGEN.json  --json '{"createRequest": {"Requestor": "maxa", "InputDataset": "/QCD_HT-1000ToInf_TuneZ2star_8TeV-madgraph-pythia6/Summer12-START50_V13-v1/GEN"}, "assignRequest": {"Team": "dmwm"}}' --allTests && \
py test/data/ReqMgr/reqmgr.py -u https://localhost:2000 -c ~/tmp/caltech/grid_certificate/2012-usercert.pem -k ~/tmp/caltech/grid_certificate/2012-userkey-passphraseless.pem -f ./test/data/ReqMgr/requests/ReDigi.json  --json '{"createRequest": {"Requestor": "maxa", "InputDataset": "/WprimeToENu_M-3000_TuneZ2star_8TeV-pythia6/Summer12-START50_V13-v1/GEN-SIM"}, "assignRequest": {"Team": "dmwm"}}' --allTests && \
py test/data/ReqMgr/reqmgr.py -u https://localhost:2000 -c ~/tmp/caltech/grid_certificate/2012-usercert.pem -k ~/tmp/caltech/grid_certificate/2012-userkey-passphraseless.pem -f ./test/data/ReqMgr/requests/ReReco.json  --json '{"createRequest": {"Requestor": "maxa", "InputDataset": "/BTag/Run2011B-v1/RAW"}, "assignRequest": {"Team": "dmwm"}}' --allTests
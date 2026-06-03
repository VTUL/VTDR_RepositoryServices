#!/bin/bash

cd /projects/lib-data-share/curation_scripts/VTDR_RepositoryServices/Figshare-APTrust

echo "========== STEP 1: ingest =========="
python ingest_bagit_arc.py || exit 1

echo "========== STEP 2: pub folder =========="
python PubFolder_Download.py || exit 1

echo "========== STEP 3: pub bag =========="
python PubBagDART_TransferAPTrust.py || exit 1

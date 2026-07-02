# VTDR Repository Services – Figshare → BagIt → APTrust Workflow

## Overview

This document describes the setup and execution process for the VTDR Repository Services workflow that packages research data into BagIt bags and prepares them for APTrust preservation.

The workflow consists of the following major components:

1. Download publication metadata from Figshare.
2. Copy research data from the ARC storage location.
3. Generate a BagIt package using DART.
4. Transfer the package for APTrust preservation.

---

# Prerequisites

## 1. Verify System Architecture

Determine which version of DART Runner to download.
[DART Runner Download](https://aptrust.github.io/dart-docs/runner/)

bash command:
```
uname -m
```

Expected output:

| Output    | Platform            |
| --------- | ------------------- |
| `x86_64`  | Linux Intel (AMD64) |
| `aarch64` | Linux ARM           |

Download the correct DART Runner locally, then copy it into the project directory.

---

# DART Configuration

## 1. Configure APTrust Storage Class

To use APTrust **Basic Storage Service** instead of **High Assurance Storage**, modify the DART BagIt profile.

Locate the tag file:

```
aptrust_info.txt
```

Change:

```
Storage Option = Standard
```

to

```
Storage Option = Glacier-OH
```

---

## 2. Export Workflow Files

Export the workflow JSON files from DART and copy them into:

```
VTDR_RepositoryServices/ARC/
```

Save them using the following filenames:

```
package_only.json
Demo_workflow.json
Repo_workflow.json
```

> **Note**
>
> This step may be simplified in a future version of the workflow.

---

# Connect to ARC

## 1. Connect to the VPN

Connect to the Virginia Tech VPN before accessing ARC resources.

---

## 2. Connect Using VS Code

Install the extension:

```
Remote - SSH
```

Connect to:

```
datatransfer.arc.vt.edu
```

Authenticate using:

* ARC password
* Duo Push verification

---

# Configure the Workflow

Open:

```
VTDR_RepositoryServices/
    Figshare-APTrust/
        configurations.ini
```

Update all configuration values as needed.

The most important setting is:

```
[ARC_PathSettings]
ARCResourcePath=
```

This should point to the dataset directory.

Example:

```
ARCResourcePath=/projects/lib-data-share/31448899_Borgoltz_2026_Stability_V1
```

If you are only running the publication workflow, you can ignore the Scratch configuration for now.

---

# Scratch Directory

Check whether a scratch directory exists.

```bash
whoami
```

Example:

```
jiren
```

Check:

```bash
ls /scratch
ls /scratch/jiren
```

If it does not exist:

```bash
mkdir -p /scratch/$(whoami)/bags
```

> **Note**
>
> The Globus node does not currently contain the `/scratch` directory.

---

# DART Runner

Ensure the executable has permission:

```bash
chmod +x dart-runner
```

Verify installation:

```bash
./dart-runner --help
```

---

# Workflow Scripts

The workflow uses several scripts.

## AutomatedReadmertf.py

Utility script.

---

## ingest_bagit_arc.py

Ingests completed BagIt packages into the repository.

---

## PubFolder_Download.py

Responsibilities:

* Download `metadata.json` from Figshare using the article ID.
* Copy research files from the ARC resource directory.
* Prepare the publication folder.

The workflow uses:

```
arc_resource_path
```

and

```
arc_template
```

within the script.

Data source:

```
Disseminated/
    file/
        DisseminatedContent/
```

---

## PubBagDART_TransferAPTrust.py

Creates the BagIt package and transfers it to APTrust.

Before running this script, change:

```python
destination = choose_destination_terminal()
```

to

```python
destination = "JUST BAGIT"
```

where appropriate (currently required in steps (1) and (3)).

---

# Running the Workflow

Navigate to:

```bash
cd Figshare-APTrust
```

## Download publication metadata

```bash
nohup python PubFolder_Download.py > pubdownload.log 2>&1 &
```

## Run the complete workflow

```bash
nohup bash run_vtdr_workflow.sh > workflow.log 2>&1 &
```

---

# Monitoring Progress

View the workflow log:

```bash
tail -f workflow.log
```

Exit log monitoring:

```
Ctrl + C
```

---

# Verify Running Processes

Check whether the workflow is still running.

Workflow script:

```bash
ps -fu $USER | grep run_vtdr
```

Publication download:

```bash
ps -fu $USER | grep PubFolder_Download
```

All Python processes:

```bash
ps -fu $USER | grep python
```

Inspect a specific process:

```bash
ps -p <PID> -o pid,etime,pcpu,pmem,stat,cmd
```

Example:

```text
PID     ELAPSED %CPU %MEM STAT CMD
1981610 13:36   47.0  0.0 R    python PubFolder_Download.py
```

---

# Finding Log Files

Locate DART log files:

```bash
find ~ -iname "*.log" | grep -i dart
```

---

# Important Checklist Before Running

* Confirm VPN connection.
* Verify `ARCResourcePath` points to the correct dataset.
* Ensure the destination mode is set appropriately (e.g., `"JUST BAGIT"` when required).
* Confirm DART Runner is executable.
* Verify the workflow JSON files are in the `ARC` directory.
* Confirm `aptrust_info.txt` uses the desired storage option.

---

# Troubleshooting

## Figshare 404 Error

Example:

```text
404 Client Error:
Entity not found: ArticleVersion
```

Example output:

```text
https://api.figshare.com/v2/articles/31448899

Entity not found: ArticleVersion
```

Possible causes include:

* Incorrect Figshare article ID.
* Incorrect article version.
* The article has not been published.
* Insufficient permissions.
* The article no longer exists.

Example test:

```bash
python test.py
```

---

# Open Questions

* Confirm whether the publication source files are obtained directly from the ARC resource directory or downloaded using the Figshare article ID.
* Investigate why article `31448899` returned a 404 response during testing.
* Consider simplifying the workflow export process from DART in future revisions.
* Update the Scratch directory documentation once the implementation is finalized.

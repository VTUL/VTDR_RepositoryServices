#!/usr/bin/env python3
"""
VTDR Figshare Ingest -> BagIt (ARC) using dart-runner (package-only workflow)

Features (no terminal ID input):
- Use a TXT file to choose what to process.
- Supports:
  1) Single ID: put one Figshare ArticleID in the txt file.
  2) Batch IDs: put multiple ArticleIDs in the txt file.
  3) Whole dataset:
      - If content already downloaded into ingest_input, put:
            @ALL_FOLDERS
        to scan IngFolderPath for VTDR_* folders and bag them all (no Figshare download).
      - Or put a long list of all IDs (download+bag).

TXT file format:
- One entry per line
- Blank lines allowed
- Lines starting with # are comments
- Special directives:
    @ALL_FOLDERS              -> bag all VTDR_* folders under IngFolderPath
    FOLDER:/abs/path/to/folder -> bag a specific existing ingest folder (skip download)

Outputs:
- dart-runner writes .tar to RunnerOutputDir (scratch_out)
- script copies .tar to FinalOutputDir
"""

import os
import sys
import json
import shutil
import subprocess
import configparser
from datetime import date, datetime

from figshare import Figshare
import figshareDownload
from Read_VTDR_Spreadsheet import vtingsheet


# ----------------------------- Utilities -----------------------------

def die(msg: str, code: int = 2):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def load_config(path: str) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    if not os.path.exists(path):
        die(f"Config file not found: {path}")
    cfg.read(path)
    return cfg


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def now_stamp():
    today = date.today().strftime("%Y%m%d")
    t = datetime.now().strftime("%H_%M_%S")
    return today, t


def read_targets_txt(txt_path: str) -> list[str]:
    """
    Returns list of target lines (raw tokens) excluding comments/blanks.
    """
    if not os.path.exists(txt_path):
        die(f"IDs txt file not found: {txt_path}")
    targets = []
    with open(txt_path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            targets.append(s)
    return targets


def list_ingest_folders(ing_folder_path: str) -> list[str]:
    """
    Lists all VTDR_* directories under IngFolderPath.
    """
    if not os.path.isdir(ing_folder_path):
        die(f"IngFolderPath is not a directory: {ing_folder_path}")
    folders = []
    for name in sorted(os.listdir(ing_folder_path)):
        p = os.path.join(ing_folder_path, name)
        if os.path.isdir(p) and name.startswith("VTDR_"):
            folders.append(p)
    return folders


# ----------------------------- Figshare + Ingest folder -----------------------------

def build_ingest_folder_name(ingsheet: dict) -> str:
    ingest_no = ingsheet["ingestno"]
    req_lfi = ingsheet["ingreqlastfirsti"]
    cor_lfi = ingsheet["ingcorlastfirsti"]
    version = ingsheet["ingversion"]
    date_ingested = ingsheet["ingestdate"]
    return f"VTDR_{ingest_no}_{req_lfi}_{cor_lfi}_v{version}_{date_ingested}"


def download_and_prepare_ingest_folder(
    token: str,
    article_id_from_sheet: str,
    ingest_version: str,
    ing_folder_path: str,
    metadata_jsonpath: str,
) -> dict:
    """
    Uses vtingsheet(article_id, ingest_version) to find the ingest row,
    downloads the private Figshare article into an ingest folder,
    writes ingest metadata json, and returns info for bagging.

    Returns dict:
      - ing_folder_name
      - data_directory_path
      - ingest_no
    """
    ingsheet = vtingsheet(article_id_from_sheet, ingest_version)

    fig_article_id = ingsheet["ingarticleid"]
    ingest_no = ingsheet["ingestno"]

    ing_folder_name = build_ingest_folder_name(ingsheet)
    data_directory_path = os.path.join(ing_folder_path, ing_folder_name)

    metadata_filename = f"{ingest_no}_DownloadedFileMetadata"
    metadata_directory_path = os.path.join(metadata_jsonpath, metadata_filename)

    ensure_dir(data_directory_path)
    ensure_dir(metadata_directory_path)

    # Download
    fs = Figshare(token=token, private=True, version=None)
    figshareDownload.download_files(
        fig_article_id,
        None,
        fs,
        data_directory=data_directory_path,
        metadata_directory=metadata_directory_path
    )

    # Write ingest metadata json
    json_out_file = os.path.join(data_directory_path, f"{ingest_no}_IngestedMetadata.json")
    if not os.path.exists(json_out_file):
        json_response = fs.get_article_details(fig_article_id, version=None)
        with open(json_out_file, "w", encoding="utf-8") as f:
            json.dump(json_response, f, indent=4)

    return {
        "ing_folder_name": ing_folder_name,
        "data_directory_path": data_directory_path,
        "ingest_no": ingest_no,
    }


# ----------------------------- dart-runner -----------------------------

def build_job_params(ing_folder_name: str, data_directory_path: str, ingest_no: str) -> dict:
    bag_tar = f"{ing_folder_name}.tar"
    return {
        "packageName": bag_tar,
        "files": [data_directory_path],
        "tags": [
            {"tagFile": "bag-info.txt", "tagName": "Bag-Group-Identifier", "value": f"VTDR_{ingest_no}"},
            {"tagFile": "bag-info.txt", "tagName": "Source-Organization", "value": "Virginia Tech"},
            {"tagFile": "aptrust-info.txt", "tagName": "Access", "value": "Institution"},
            {"tagFile": "aptrust-info.txt", "tagName": "Storage-Option", "value": "Standard"},
            {"tagFile": "aptrust-info.txt", "tagName": "Title", "value": ing_folder_name},
            {"tagFile": "bagit.txt", "tagName": "BagIt-Version", "value": "0.97"},
            {"tagFile": "bagit.txt", "tagName": "Tag-File-Character-Encoding", "value": "UTF-8"},
        ]
    }


def run_dart_runner_and_copy(
    dart_runner: str,
    workflow_json: str,
    scratch_out: str,
    final_out: str,
    job_params: dict,
):
    """
    Runs dart-runner (single job via stdin job params),
    then copies the resulting .tar from scratch_out to final_out.
    """
    ensure_dir(scratch_out)
    ensure_dir(final_out)

    bag_tar = job_params["packageName"]
    today, t = now_stamp()

    cmd = [
        dart_runner,
        f"--workflow={workflow_json}",
        f"--output-dir={scratch_out}",
        "--delete=false",
        "--skip-artifacts",
    ]

    print(f"\nRunning dart-runner for {bag_tar} ...")
    p = subprocess.run(
        cmd,
        input=json.dumps(job_params),
        text=True,
        capture_output=True
    )

    # stdout is JSON Lines, usually 1 line for single job
    if p.stdout.strip():
        print("dart-runner stdout:\n", p.stdout)
    if p.stderr.strip():
        print("dart-runner stderr:\n", p.stderr, file=sys.stderr)

    if p.returncode != 0:
        die(f"dart-runner failed for {bag_tar}, exit={p.returncode}")

    scratch_tar_path = os.path.join(scratch_out, bag_tar)
    if not os.path.exists(scratch_tar_path):
        die(f"Expected tar not found: {scratch_tar_path}")

    final_tar_path = os.path.join(final_out, bag_tar)
    if os.path.exists(final_tar_path):
        # avoid overwrite
        base = bag_tar.replace(".tar", "")
        final_tar_path = os.path.join(final_out, f"{base}_{today}_{t}.tar")

    shutil.copy2(scratch_tar_path, final_tar_path)
    print(f"✅ Bag copied to: {final_tar_path}")


# ----------------------------- Main logic -----------------------------

def main():
    # 1) Config paths (edit here once)
    CONFIG_PATH = "configurations.ini"
    IDS_TXT_PATH = "ids_to_process.txt"  # user edits this file, no terminal input needed

    cfg = load_config(CONFIG_PATH)

    # Required settings
    token = cfg["FigshareSettings"]["token"]
    ingest_version = cfg["FigshareSettings"]["IngestVersionNumber"]

    ing_folder_path = cfg["IngestBag_PathSettings"]["IngFolderPath"]
    metadata_jsonpath = cfg["IngestBag_PathSettings"]["metadatajsonpath"]

    dart_runner = cfg["dart_PathSettings"]["dart_runner_path"]
    workflow_json = cfg["dart_PathSettings"]["workflow_package_only"]

    scratch_out = cfg["IngestBag_PathSettings"]["RunnerOutputDir"]
    final_out = cfg["IngestBag_PathSettings"]["FinalOutputDir"]

    # Quick sanity checks
    for key_path, label in [
        (dart_runner, "dart_runner_path"),
        (workflow_json, "workflow_package_only"),
    ]:
        if not os.path.exists(key_path):
            die(f"{label} not found: {key_path}")

    ensure_dir(ing_folder_path)
    ensure_dir(scratch_out)
    ensure_dir(final_out)

    # 2) Read targets from txt
    targets = read_targets_txt(IDS_TXT_PATH)
    if not targets:
        die(f"No targets found in {IDS_TXT_PATH}. Put an ArticleID, FOLDER:/path, or @ALL_FOLDERS.")

    # 3) Expand targets to actions
    # We will build a list of (mode, value) where mode is "ID" or "FOLDER"
    actions: list[tuple[str, str]] = []

    for token_line in targets:
        if token_line == "@ALL_FOLDERS":
            folders = list_ingest_folders(ing_folder_path)
            if not folders:
                die(f"No VTDR_* folders found under {ing_folder_path} for @ALL_FOLDERS.")
            for f in folders:
                actions.append(("FOLDER", f))
            continue

        if token_line.startswith("FOLDER:"):
            folder_path = token_line[len("FOLDER:"):].strip()
            if not folder_path:
                die("Invalid FOLDER: line with empty path.")
            actions.append(("FOLDER", folder_path))
            continue

        # Otherwise treat as Figshare ArticleID
        actions.append(("ID", token_line))

    print(f"Will process {len(actions)} item(s) from {IDS_TXT_PATH}.")

    # 4) Process each
    for mode, val in actions:
        try:
            if mode == "ID":
                article_id = val
                print(f"\n==== [ID] {article_id} ====")
                info = download_and_prepare_ingest_folder(
                    token=token,
                    article_id_from_sheet=article_id,
                    ingest_version=ingest_version,
                    ing_folder_path=ing_folder_path,
                    metadata_jsonpath=metadata_jsonpath,
                )

                ing_folder_name = info["ing_folder_name"]
                data_dir = info["data_directory_path"]
                ingest_no = info["ingest_no"]

                job_params = build_job_params(ing_folder_name, data_dir, ingest_no)
                run_dart_runner_and_copy(
                    dart_runner=dart_runner,
                    workflow_json=workflow_json,
                    scratch_out=scratch_out,
                    final_out=final_out,
                    job_params=job_params,
                )

            elif mode == "FOLDER":
                folder_path = val
                if not os.path.isdir(folder_path):
                    die(f"Folder not found: {folder_path}")

                ing_folder_name = os.path.basename(folder_path.rstrip("/"))
                # Try to extract ingest_no from folder name "VTDR_<ingestno>_..."
                ingest_no = "UNKNOWN"
                parts = ing_folder_name.split("_")
                if len(parts) >= 2 and parts[0] == "VTDR":
                    ingest_no = parts[1]

                print(f"\n==== [FOLDER] {folder_path} ====")
                job_params = build_job_params(ing_folder_name, folder_path, ingest_no)
                run_dart_runner_and_copy(
                    dart_runner=dart_runner,
                    workflow_json=workflow_json,
                    scratch_out=scratch_out,
                    final_out=final_out,
                    job_params=job_params,
                )

            else:
                die(f"Unknown mode: {mode}")

        except Exception as e:
            # keep going for batch use; comment out if you prefer fail-fast
            print(f"❌ Failed item ({mode}={val}): {e}", file=sys.stderr)
            continue

    print("\nAll done.")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
VTDR Figshare Ingest -> BagIt / Demo / Repo using dart-runner

Features:
- User puts only Figshare Article IDs into ids_to_process.txt
- At runtime, user chooses one of:
    1) JUST BAGIT
    2) DEMO
    3) REPO
- Script downloads/prepares ingest folder from Figshare
- Script runs dart-runner with the selected workflow
- Script copies resulting .tar from RunnerOutputDir to FinalOutputDir

ids_to_process.txt format:
- One Article ID per line
- Blank lines allowed
- Lines starting with # are comments
"""

import os
import sys
import json
import shutil
import subprocess
import configparser
from datetime import date, datetime
from dotenv import load_dotenv

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


# def read_targets_txt(txt_path: str) -> list[str]:
#     """
#     Returns list of article IDs excluding comments/blanks.
#     Only digits are accepted.
#     """
#     if not os.path.exists(txt_path):
#         die(f"IDs txt file not found: {txt_path}")

#     targets = []
#     with open(txt_path, "r", encoding="utf-8") as f:
#         for line in f:
#             s = line.strip()
#             if not s or s.startswith("#"):
#                 continue
#             if not s.isdigit():
#                 die(f"Invalid article ID in {txt_path}: {s}")
#             targets.append(s)

#     return targets


# ----------------------------- Terminal choice -----------------------------

def choose_destination_terminal() -> str:
    print("\nChoose upload option for this run:")
    print("  1) JUST BAGIT")
    print("  2) DEMO")
    print("  3) REPO")

    while True:
        choice = input("Enter 1, 2, 3, JUST BAGIT, DEMO, or REPO: ").strip().upper()

        if choice in {"1", "JUST BAGIT", "JUST_BAGIT", "BAGIT"}:
            return "JUST BAGIT"
        elif choice in {"2", "DEMO"}:
            return "DEMO"
        elif choice in {"3", "REPO"}:
            return "REPO"
        else:
            print("Invalid choice. Please enter 1, 2, 3, JUST BAGIT, DEMO, or REPO.")


def choose_workflow_json(
    destination: str,
    workflow_package_only: str,
    workflow_demo: str,
    workflow_repo: str,
) -> str:
    if destination == "JUST BAGIT":
        return workflow_package_only
    elif destination == "DEMO":
        return workflow_demo
    elif destination == "REPO":
        return workflow_repo
    else:
        die(f"Unknown destination: {destination}")


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
    final_out: str,
    job_params: dict,
):
    """
    Run dart-runner and write tar directly to FinalOutputDir.
    """
    ensure_dir(final_out)

    bag_tar = job_params["packageName"]

    cmd = [
        dart_runner,
        f"--workflow={workflow_json}",
        f"--output-dir={final_out}",
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

    if p.stdout.strip():
        print("dart-runner stdout:\n", p.stdout)

    if p.stderr.strip():
        print("dart-runner stderr:\n", p.stderr, file=sys.stderr)

    if p.returncode != 0:
        die(f"dart-runner failed for {bag_tar}, exit={p.returncode}")

    tar_path = os.path.join(final_out, bag_tar)

    if not os.path.exists(tar_path):
        die(f"Expected tar not found: {tar_path}")

    print(f"✅ Bag created at: {tar_path}")

    return tar_path


# ----------------------------- Main logic -----------------------------

def main():
    load_dotenv()
    # print("DEBUG KEY:", os.environ.get("DEMO_AWS_ACCESS_KEY_ID"))

    CONFIG_PATH = "configurations.ini"
    IDS_TXT_PATH = "ids_to_process.txt"

    cfg = load_config(CONFIG_PATH)

    # Required settings
    token = cfg["FigshareSettings"]["token"]
    ingest_version = cfg["FigshareSettings"]["IngestVersionNumber"]

    ing_folder_path = cfg["IngestBag_PathSettings"]["IngFolderPath"]
    metadata_jsonpath = cfg["IngestBag_PathSettings"]["metadatajsonpath"]

    dart_runner = cfg["dart_PathSettings"]["dart_runner_path"]
    workflow_package_only = cfg["dart_PathSettings"]["workflow_package_only"]
    workflow_demo = cfg["dart_PathSettings"]["workflow_demo"]
    workflow_repo = cfg["dart_PathSettings"]["workflow_repo"]

    # scratch_out = cfg["IngestBag_PathSettings"]["RunnerOutputDir"]
    final_out = cfg["IngestBag_PathSettings"]["FinalOutputDir"]

    # Quick sanity checks
    for key_path, label in [
        (dart_runner, "dart_runner_path"),
        (workflow_package_only, "workflow_package_only"),
        (workflow_demo, "workflow_demo"),
        (workflow_repo, "workflow_repo"),
    ]:
        if not os.path.exists(key_path):
            die(f"{label} not found: {key_path}")

    ensure_dir(ing_folder_path)
    ensure_dir(metadata_jsonpath)
    ensure_dir(final_out)

    # Choose workflow in terminal
    destination = "DEMO"
    # destination = choose_destination_terminal()
    workflow_json = choose_workflow_json(
        destination,
        workflow_package_only,
        workflow_demo,
        workflow_repo,
    )

    print(f"\nSelected option: {destination}")
    print(f"Workflow file: {workflow_json}")

    # Read article IDs
    # article_ids = read_targets_txt(IDS_TXT_PATH)
    article_id = cfg["FigshareSettings"]["FigshareArticleID"].strip()
    article_ids = [article_id]
    print("article ids from configurations.ini:", article_ids)
    if not article_ids:
        die(f"No article IDs found in {IDS_TXT_PATH}.")

    # Process each article ID
    for article_id in article_ids:
        try:
            print(f"\n==== [{destination}] [ID] {article_id} ====")

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
                final_out=final_out,
                job_params=job_params,
            )

        except Exception as e:
            print(f"❌ Failed article ID {article_id}: {e}", file=sys.stderr)
            continue

    print("\nAll done.")


if __name__ == "__main__":
    main()
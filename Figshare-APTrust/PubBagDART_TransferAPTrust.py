#!/usr/bin/env python3

import os
import sys
import json
import shutil
import subprocess
import configparser
from datetime import date, datetime

from Read_VTDR_Spreadsheet import vtpubsheet


def die(msg: str, code: int = 2):
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def load_config(path: str) -> configparser.ConfigParser:
    cfg = configparser.ConfigParser()
    if not os.path.exists(path):
        die(f"Config file not found: {path}")
    cfg.read(path)
    return cfg


def now_stamp():
    today = date.today().strftime("%Y%m%d")
    t = datetime.now().strftime("%H_%M_%S")
    return today, t


def choose_workflow_terminal() -> str:
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


def choose_workflow_json(destination: str, workflow_package_only: str, workflow_demo: str, workflow_repo: str) -> str:
    if destination == "JUST BAGIT":
        return workflow_package_only
    elif destination == "DEMO":
        return workflow_demo
    elif destination == "REPO":
        return workflow_repo
    else:
        die(f"Unknown destination: {destination}")


def build_publication_bag_name(pvtsheet: dict) -> str:
    pPubAccessionNumber = pvtsheet["gspubnum"]
    pIngAccessionNumber = pvtsheet["gsingestno"]
    pCorrespondingAuthorLFI = pvtsheet["gscorrlastfi"]
    pVersion = pvtsheet["gsversnum"]
    pDate = pvtsheet["gsdatepub"]
    pDOIsuffix = pvtsheet["gsdoisuffix"]

    return f"VTDR_{pPubAccessionNumber}_{pIngAccessionNumber}_DOI_{pDOIsuffix}_{pCorrespondingAuthorLFI}_v{pVersion}_{pDate}"


def build_job_params(aptrust_bag_name: str, pub_folder: str, pvtsheet: dict) -> dict:
    pPubAccessionNumber = pvtsheet["gspubnum"]

    return {
        "packageName": f"{aptrust_bag_name}.tar",
        "files": [pub_folder],
        "tags": [
            {"tagFile": "bag-info.txt", "tagName": "Bag-Group-Identifier", "value": f"VTDR_{pPubAccessionNumber}"},
            {"tagFile": "bag-info.txt", "tagName": "Source-Organization", "value": "Virginia Tech"},
            {"tagFile": "aptrust-info.txt", "tagName": "Access", "value": "Institution"},
            {"tagFile": "aptrust-info.txt", "tagName": "Storage-Option", "value": "Standard"},
            {"tagFile": "aptrust-info.txt", "tagName": "Title", "value": aptrust_bag_name},
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
        capture_output=True,
        env=os.environ.copy(),
    )

    if p.stdout.strip():
        print("dart-runner stdout:\n", p.stdout)
    if p.stderr.strip():
        print("dart-runner stderr:\n", p.stderr, file=sys.stderr)

    if p.returncode != 0:
        die(f"dart-runner failed for {bag_tar}, exit={p.returncode}")

    job_result = None
    stdout_lines = [line.strip() for line in p.stdout.splitlines() if line.strip()]
    if stdout_lines:
        try:
            job_result = json.loads(stdout_lines[-1])
        except json.JSONDecodeError:
            die("Could not parse dart-runner JSON stdout.")

    if job_result is None:
        die("No JSON result returned from dart-runner.")

    if not job_result.get("succeeded", False):
        upload_results = job_result.get("uploadResults", [])
        error_messages = []

        for upload in upload_results:
            errs = upload.get("errors", {})
            for _, msg in errs.items():
                error_messages.append(msg)

        if error_messages:
            die("dart-runner job failed during upload:\n" + "\n".join(error_messages))
        else:
            die("dart-runner reported succeeded=false.")

    scratch_tar_path = os.path.join(scratch_out, bag_tar)
    if not os.path.exists(scratch_tar_path):
        die(f"Expected tar not found: {scratch_tar_path}")

    final_tar_path = os.path.join(final_out, bag_tar)
    if os.path.exists(final_tar_path):
        base = bag_tar.replace(".tar", "")
        final_tar_path = os.path.join(final_out, f"{base}_{today}_{t}.tar")

    shutil.copy2(scratch_tar_path, final_tar_path)
    print(f"✅ Final tar copied to: {final_tar_path}")

    return final_tar_path


def main():
    CONFIG_PATH = "configurations.ini"
    cfg = load_config(CONFIG_PATH)

    ArticleID = cfg["FigshareSettings"]["FigshareArticleID"]
    PublishedVersionNumber = cfg["FigshareSettings"]["PublishedVersionNumber"]

    PubFolderPath = cfg["PubFolder_PathSettings"]["PubFolderPath"]

    dart_runner = cfg["dart_PathSettings"]["dart_runner_path"]
    workflow_package_only = cfg["dart_PathSettings"]["workflow_package_only"]
    workflow_demo = cfg["dart_PathSettings"]["workflow_demo"]
    workflow_repo = cfg["dart_PathSettings"]["workflow_repo"]

    scratch_out = cfg["PubBagDartAptrust_PathSettings"]["RunnerOutputDir"]
    final_out = cfg["PubBagDartAptrust_PathSettings"]["FinalOutputDir"]

    for key_path, label in [
        (dart_runner, "dart_runner_path"),
        (workflow_package_only, "workflow_package_only"),
        (workflow_demo, "workflow_demo"),
        (workflow_repo, "workflow_repo"),
    ]:
        if not os.path.exists(key_path):
            die(f"{label} not found: {key_path}")

    ensure_dir(PubFolderPath)
    ensure_dir(scratch_out)
    ensure_dir(final_out)

    Pvtsheet = vtpubsheet(ArticleID=ArticleID, PublishedVersionNumber=PublishedVersionNumber)

    aptrust_bag_name = build_publication_bag_name(Pvtsheet)
    pub_folder = os.path.join(PubFolderPath, aptrust_bag_name)

    if not os.path.isdir(pub_folder):
        die(f"Publication folder not found: {pub_folder}")

    print(f"\nPublication folder found: {pub_folder}")
    print(f"Bag name: {aptrust_bag_name}")

    destination = choose_workflow_terminal()
    workflow_json = choose_workflow_json(
        destination,
        workflow_package_only,
        workflow_demo,
        workflow_repo,
    )

    print(f"\nSelected upload option: {destination}")
    print(f"Workflow file: {workflow_json}")
    print(f"Runner output folder: {scratch_out}")
    print(f"Final output folder: {final_out}")

    job_params = build_job_params(aptrust_bag_name, pub_folder, Pvtsheet)

    final_tar_path = run_dart_runner_and_copy(
        dart_runner=dart_runner,
        workflow_json=workflow_json,
        scratch_out=scratch_out,
        final_out=final_out,
        job_params=job_params,
    )

    print("\nAll done.")
    print(f"Final tar location: {final_tar_path}")


if __name__ == "__main__":
    main()
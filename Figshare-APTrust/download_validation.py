import os
import sys


def get_local_files(directory):
    """
    Recursively retrieve all local files from the download directory.

    Returns a dictionary:
        relative_path -> absolute_path
    """

    local_files = {}

    for root, dirs, files in os.walk(directory):
        for filename in files:

            full_path = os.path.join(root, filename)

            relative_path = os.path.relpath(
                full_path,
                directory
            )

            local_files[relative_path] = full_path

    return local_files


def ask_to_proceed(message):
    """
    Ask the curator whether to continue the workflow.

    The prompt is displayed in the terminal.
    The curator response is printed so it will also be recorded
    in the VTDR log file.
    """

    while True:

        response = input(
            f"\n{message}\n"
            "Would you like to proceed? (yes/no): "
        ).strip().lower()

        # Print response so it is recorded in the log
        print(f"Curator response: {response}")

        if response == "yes":
            print("Proceeding with the workflow.")
            return True

        elif response == "no":
            print("Workflow stopped by curator.")
            return False

        else:
            print("Please enter 'yes' or 'no'.")


def verify_file_count(expected_files, download_directory):
    """
    Compare the files expected from Figshare with the files
    available in the local download directory.

    expected_files:
        The Figshare file_list returned by figshareDownload.download_files()

    download_directory:
        Local directory containing the downloaded Figshare files.
    """

    print("\n")
    print("=" * 80)
    print("FIGSHARE FILE COUNT CHECK")
    print("=" * 80)

    local_files = get_local_files(download_directory)

    # Expected filenames from Figshare
    expected_names = {
        file_info["name"]
        for file_info in expected_files
    }

    # Local filenames / relative paths
    local_names = set(local_files.keys())

    expected_count = len(expected_names)
    local_count = len(local_names)

    print(f"Expected Figshare file count: {expected_count}")
    print(f"Local downloaded file count:  {local_count}")

    missing_files = sorted(
        expected_names - local_names
    )

    unexpected_files = sorted(
        local_names - expected_names
    )

    # --------------------------------------------------
    # Everything matches
    # --------------------------------------------------

    if (
        expected_count == local_count
        and not missing_files
        and not unexpected_files
    ):

        print("\nFILE COUNT CHECK PASSED")
        print("All expected Figshare files are present.")

        return True

    # --------------------------------------------------
    # Something does not match
    # --------------------------------------------------

    print("\n")
    print("*" * 80)
    print("WARNING: FILE COUNT / FILE LIST DOES NOT MATCH FIGSHARE")
    print("*" * 80)

    print(f"\nExpected Figshare file count: {expected_count}")
    print(f"Local downloaded file count:  {local_count}")

    if missing_files:
        print("\nMissing files:")

        for filename in missing_files:
            print(f"    {filename}")
    else:
        print("\nMissing files: None")

    if unexpected_files:
        print("\nUnexpected local files:")

        for filename in unexpected_files:
            print(f"    {filename}")
    else:
        print("\nUnexpected local files: None")

    proceed = ask_to_proceed(
        "The downloaded file count/list does not match Figshare.\n"
        "Please review the file information above."
    )

    if not proceed:
        sys.exit(
            "Workflow stopped because file verification did not pass."
        )

    return False
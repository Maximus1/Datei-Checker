import argparse
import os
import asyncio
from core.processor import process_directory

def print_progress(current, total, result):
    """
    Console progress callback.
    """
    percent = (current / total) * 100
    status_icon = "✅" if result["status"] == "Success" else "❌"
    print(f"[{percent:3.0f}%] {status_icon} {os.path.basename(result['path'])} -> {result.get('final_path', result['path'])} ({result.get('type', 'Unknown')})")

async def run_cli(args):
    """
    Run CLI application.
    """
    print("--- Starting Datei Checker CLI ---")
    print(f"Target Directory: {args.directory}")
    print(f"Dry-Run: {args.dry_run}")
    print("-" * 34)

    results = await process_directory(args.directory, args.dry_run, print_progress)

    success_count = sum(1 for r in results if r["status"] == "Success")
    error_count = len(results) - success_count

    print("-" * 34)
    print("Processing Complete.")
    print(f"Total Files: {len(results)}")
    print(f"Renamed:     {success_count}")
    print(f"Errors:      {error_count}")

def main():
    parser = argparse.ArgumentParser(description="Datei Checker - File Signature & Recovery")
    parser.add_argument("directory", help="The directory to scan for recovered files")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Only show what would be done, no actual renaming")
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        return

    asyncio.run(run_cli(args))

if __name__ == "__main__":
    main()

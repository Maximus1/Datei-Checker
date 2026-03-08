import argparse
from ui import cli, app

def main():
    parser = argparse.ArgumentParser(description="Datei Checker - File Signature & Recovery")
    parser.add_argument("directory", nargs="?", help="The directory to scan for recovered files")
    parser.add_argument("-cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("-d", "--dry-run", action="store_true", help="Only show what would be done, no actual renaming")
    args = parser.parse_args()

    # If directory provided or -cli flag set, use CLI
    if args.directory or args.cli:
        if not args.directory:
            print("Error: Directory path required for CLI mode.")
            return
        cli.main()
    else:
        # Default: GUI
        app.main()

if __name__ == "__main__":
    main()

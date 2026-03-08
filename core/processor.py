import os
import asyncio
from concurrent.futures import ProcessPoolExecutor
from functools import partial
from .detector import detect_file_type
from .metadata import extract_metadata_name
from .renamer import safe_rename

def process_single_file(file_path, dry_run=False):
    """
    Worker function to process a single file (CPU-bound).
    """
    try:
        # 1. Detect file type
        ext, type_name = detect_file_type(file_path)
        if not ext:
            return {"path": file_path, "status": "Unknown", "msg": "Could not detect type"}

        # 2. Extract original name (optional)
        original_name = extract_metadata_name(file_path, ext)
        base_name = os.path.splitext(os.path.basename(file_path))[0]

        # If original name found, use it, else keep old base + detected extension
        if original_name:
            # Add extension if not present in extracted name
            if not original_name.endswith(ext):
                new_name = f"{original_name}{ext}"
            else:
                new_name = original_name
        else:
            new_name = f"{base_name}{ext}"

        # 3. Rename file
        success, msg, final_path = safe_rename(file_path, new_name, dry_run=dry_run)

        return {
            "path": file_path,
            "status": "Success" if success else "Error",
            "msg": msg,
            "final_path": final_path,
            "type": type_name
        }
    except OSError as e:
        return {"path": file_path, "status": "Error", "msg": f"File processing error: {str(e)}"}

async def process_directory(root_dir, dry_run=False, callback=None, stop_event=None):
    """
    Main async directory processor using ProcessPoolExecutor.
    """
    files_to_process = []
    for dirpath, _, filenames in os.walk(root_dir):
        if stop_event and stop_event.is_set():
            break
        for f in filenames:
            full_path = os.path.join(dirpath, f)
            # Only process if it has NO extension or a dummy one
            if "." not in f or f.endswith(".tmp"): # Adjust conditions as needed
                files_to_process.append(full_path)

    if not files_to_process:
        return []

    results = []
    # Use max cores - 1 (leave one for UI/System)
    max_workers = max(1, os.cpu_count() - 1)

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, partial(process_single_file, f, dry_run))
            for f in files_to_process
        ]

        for task in asyncio.as_completed(tasks):
            if stop_event and stop_event.is_set():
                # Try to cancel remaining tasks (only works if they haven't started)
                # ProcessPoolExecutor doesn't support easy cancellation of running tasks
                # but we can stop processing the results.
                break
            res = await task
            results.append(res)
            if callback:
                callback(len(results), len(files_to_process), res)

    return results

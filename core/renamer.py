import os

def safe_rename(old_path, new_name, dry_run=False):
    """
    Safely renames a file, handling conflicts.

    :param old_path: Current full path to file
    :param new_name: Desired new name (with extension)
    :param dry_run: If True, only log what would happen
    :return: (bool, str, str) -> (Success, Message, ResultPath)
    """
    if not os.path.exists(old_path):
        return False, f"Source file does not exist: {old_path}", old_path

    directory = os.path.dirname(old_path)
    base_name, extension = os.path.splitext(new_name)
    target_path = os.path.join(directory, new_name)

    # Conflict handling (add suffix if file exists)
    counter = 1
    while os.path.exists(target_path):
        if target_path == old_path: # Already renamed or correct
            break
        new_name = f"{base_name} ({counter}){extension}"
        target_path = os.path.join(directory, new_name)
        counter += 1

    if dry_run:
        return True, f"Dry-run: Would rename to {new_name}", target_path

    try:
        os.rename(old_path, target_path)
        return True, f"Successfully renamed to {new_name}", target_path
    except OSError as e:
        return False, f"Rename failed: {str(e)}", old_path

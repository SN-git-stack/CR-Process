import os
import argparse
import shutil
import re

TEMPLATE_PATH = os.path.join("templates", "cr_template.md")
CR_BASE_DIR = "change_requests"

def sanitize_filename(name):
    """Sanitizes a string to be safe for filenames."""
    # Replace spaces with underscores and remove non-alphanumeric chars (except _-)
    s = name.lower().replace(" ", "_")
    return re.sub(r'[^a-z0-9_-]', '', s)

def create_change_request(title):
    folder_name = sanitize_filename(title)
    target_dir = os.path.join(CR_BASE_DIR, folder_name)
    
    if os.path.exists(target_dir):
        print(f"Error: Directory '{target_dir}' already exists.")
        return

    # Create Directory
    os.makedirs(target_dir)
    print(f"Created directory: {target_dir}")

    # Copy Template
    target_file = os.path.join(target_dir, f"{folder_name}.md")
    if os.path.exists(TEMPLATE_PATH):
        shutil.copy(TEMPLATE_PATH, target_file)
        print(f"Created CR file: {target_file}")
    else:
        # Fallback if template is missing
        with open(target_file, "w") as f:
            f.write(f"# Change Request: {title}\n\n[Description]\n")
        print(f"Created CR file (blank): {target_file}")

    print("\nDone. You can now edit the file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new Change Request directory and file.")
    parser.add_argument("title", help="Title of the Change Request (e.g., 'New Payment Gateway')")
    
    args = parser.parse_args()
    create_change_request(args.title)

import os
import shutil
import subprocess
from pathlib import Path
from config import SEVEN_ZIP

def extract_chm(chm_file, dest_folder):
    cmd = [SEVEN_ZIP, 'x', '-y', str(chm_file), f'-o{dest_folder}']
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def extract_all(selected_folder):
    output_folder = Path(selected_folder) / 'html'
    output_folder.mkdir(exist_ok=True)

    chm_files = list(Path(selected_folder).glob('*.chm'))
    if not chm_files:
        return False

    for chm_file in chm_files:
        dest_folder = output_folder / chm_file.stem
        if dest_folder.exists():
            def on_rm_error(func, path, exc_info):
                import stat
                os.chmod(path, stat.S_IWRITE)
                func(path)
            shutil.rmtree(dest_folder, onerror=on_rm_error)
            print(f"Overwrite: {chm_file.name}")

        dest_folder.mkdir()
        print(f"Extracting: {chm_file.name} ...")
        if extract_chm(chm_file, dest_folder):
            print(f"Done: {chm_file.name}")
        else:
            print(f"Failed: {chm_file.name}")

    return True

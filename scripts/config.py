import os
import sys
import shutil
import tempfile

def get_resource_path(relative_path):
    """Get the path to a resource file, works for dev and PyInstaller."""
    if hasattr(sys, '_MEIPASS'):
        # Running as compiled exe
        base_path = sys._MEIPASS
    else:
        # Running in development
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

def extract_7z():
    """Extract 7z.exe from resources to temp folder if not found."""
    # Check if 7z is already in PATH or default locations
    seven_zip_paths = [
        r'C:\Program Files\7-Zip\7z.exe',
        r'C:\Program Files (x86)\7-Zip\7z.exe',
        '7z'
    ]
    
    for path in seven_zip_paths:
        if path == '7z':
            # Check if 7z command works
            import subprocess
            try:
                result = subprocess.run(['7z'], capture_output=True, timeout=5)
                if result.returncode in [0, 7]:  # 7 means no files specified
                    return '7z'
            except:
                continue
        elif os.path.exists(path):
            return path
    
    # Not found, try to extract from resources
    if hasattr(sys, '_MEIPASS'):
        # Running as compiled exe - extract from temp
        src_7z = get_resource_path('7z/7z.exe')
        if os.path.exists(src_7z):
            temp_dir = tempfile.mkdtemp()
            dest_7z = os.path.join(temp_dir, '7z.exe')
            shutil.copy2(src_7z, dest_7z)
            return dest_7z
    
    return None

# Try to find 7z on import
SEVEN_ZIP = extract_7z()

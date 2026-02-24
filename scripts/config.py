SEVEN_ZIP_PATHS = [
    r'C:\Program Files\7-Zip\7z.exe',
    r'C:\Program Files (x86)\7-Zip\7z.exe',
    '7z'
]

def find_7z():
    import os
    for path in SEVEN_ZIP_PATHS:
        if os.path.exists(path):
            return path
    return '7z'

SEVEN_ZIP = find_7z()

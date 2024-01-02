import glob

def find_latest_file(pattern):
    filenames = glob.glob(pattern)
    filenames = sorted(filenames)
    latest = filenames[-1]
    
    return latest
    

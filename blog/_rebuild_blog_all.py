import subprocess
import os 
from tqdm import tqdm

def main():
    files = os.listdir()
    md_files = []
    for f in files:
        if f.split('.')[-1] == 'md':
            md_files.append(f)
    
    for md_f in tqdm(md_files):
        subprocess.run(f"python _md_to_html.py {md_f}".split(" "))


if __name__ == "__main__":
    main()
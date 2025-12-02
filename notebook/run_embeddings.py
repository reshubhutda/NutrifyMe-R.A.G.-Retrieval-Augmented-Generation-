# Testing code

import subprocess

files = [
    "Nutrition_embed.py",
    "Health_embed.py",
    "Reference_embed.py"
]

for file in files:
    print(f"Running {file}...")
    subprocess.run(["python", file])
    print(f"Finished {file}\n")

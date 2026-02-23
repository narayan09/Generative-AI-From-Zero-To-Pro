import pandas as pd # type: ignore

def parse_csv(file_path):
    df = pd.read_csv(file_path)
    candidates = []
    for _, row in df.iterrows():
        candidates.append({
            "name": row["Name"],
            "text": row["ResumeText"]
        })
    return candidates

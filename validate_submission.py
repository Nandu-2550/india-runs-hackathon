import pandas as pd
import sys

def validate():
    file_path = r'C:\Projects\H2S_India_Run\submission.csv'
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print("FAIL: Could not read file", e)
        return
        
    if len(df) != 100:
        print(f"FAIL: Expected 100 rows, got {len(df)}")
        return
        
    expected_cols = ['candidate_id', 'rank', 'score', 'reasoning']
    if list(df.columns) != expected_cols:
        print(f"FAIL: Columns do not match exactly. Got: {list(df.columns)}")
        return
        
    ranks = df['rank'].tolist()
    if ranks != list(range(1, 101)):
        print("FAIL: Ranks are not 1-100 in order")
        return
        
    scores = df['score']
    if not (scores.between(0, 1).all()):
        print("FAIL: Scores not between 0 and 1")
        return
        
    if not df['candidate_id'].str.match(r'^CAND_\d{7}$').all():
        print("FAIL: Candidate IDs do not match CAND_XXXXXXX format")
        return
        
    print("PASS")

if __name__ == "__main__":
    validate()

import json
import pandas as pd
import os

def remove_json_duplicates(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # Remove exact match duplicates
    unique_data = list({json.dumps(item, sort_keys=True) for item in data})
    unique_json = [json.loads(item) for item in unique_data]
    print(f"[JSON] Removed {len(data) - len(unique_json)} duplicates. {len(unique_json)} unique records remain.")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unique_json, f, ensure_ascii=False, indent=2)

def remove_csv_duplicates(input_path, output_path):
    df = pd.read_csv(input_path)
    before = len(df)
    df_unique = df.drop_duplicates()
    after = len(df_unique)
    print(f"[CSV] Removed {before - after} duplicates. {after} unique rows remain.")
    df_unique.to_csv(output_path, index=False)

if __name__ == "__main__":
    # Paths
    json_in = "genai_jobs_results.json"
    json_out = "genai_jobs_results_deduped.json"
    csv_in = "genai_jobs_results.csv"
    csv_out = "genai_jobs_results_deduped.csv"

    if os.path.exists(json_in):
        remove_json_duplicates(json_in, json_out)
    else:
        print(f"[JSON] File not found: {json_in}")

    if os.path.exists(csv_in):
        remove_csv_duplicates(csv_in, csv_out)
    else:
        print(f"[CSV] File not found: {csv_in}") 
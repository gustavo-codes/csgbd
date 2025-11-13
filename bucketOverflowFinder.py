from HashIndex.ExtendibleHash import HashIndex
import random
import pandas as pd

total_overflows = 0

for attempt in range(1, 1001):
    table = HashIndex()
    randomNumbers = random.sample(range(1, 51), 50)
    overflow_rows = []

    for n in randomNumbers:
        table.insert(n)

        for idx, bucket in table.table.items():
            if len(bucket.items) == 5:
                overflow_rows.append({
                    "Execução": attempt,
                    "Diretório": idx,
                    "LocalDepth": bucket.localDepth,
                    "Itens": ", ".join(map(str, bucket.items))
                })

    if overflow_rows:
        total_overflows += 1
        df = pd.DataFrame(overflow_rows)
        print(f"\n--- Execução {attempt}: Buckets com 5 itens ---")
        print(df.to_markdown(index=False, tablefmt="grid"))

print(f"\nTotal de execuções com algum bucket de 5 itens: {total_overflows}/1000")

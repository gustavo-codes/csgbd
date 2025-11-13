from HashIndex.ExtendibleHash import HashIndex
import random

table = HashIndex()
randomNumbers = random.sample(range(1, 51), 50)
inserted = []

for n in randomNumbers:
    input(f"Pressione Enter para inserir {n} ({table.hash(n)})")
    table.insert(n)
    inserted.append(n)
    table.print_buckets()
    
    if inserted and random.random() < 0.2:
        to_remove = random.choice(inserted)
        table.remove(to_remove)
        inserted.remove(to_remove)
        print(f"Removido {to_remove}")
        table.print_buckets()

for n in range(51): 
    if n % 2 != 0: 
        table.remove(n)

table.print_buckets()

distinct_buckets = len(set(id(b) for b in table.table.values()))
print(f"\n--- Relatório Final ---")
print(f"Total de buckets distintos: {distinct_buckets}")
print(f"Global Depth atual: {table.globalDepth}")

from HashIndex.ExtendibleHash import HashIndex
import random

table = HashIndex()
randomNumbers = random.sample(range(1, 51), 50)

for n in randomNumbers:
    input(f"Pressione Enter para inserir {n} ({table.hash(n)})")
    table.insert(n)
    table.print_buckets()

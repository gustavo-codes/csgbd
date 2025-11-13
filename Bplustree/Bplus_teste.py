from b_plus import *

bpt = BPlusTree(3)
keys = [10, 20, 5, 6, 12, 30, 7, 17]
for key in keys:
    bpt.insert(key)

print("Percorrendo a árvore b+:")
bpt.display()
node, pos = bpt.search(7)
print("\nBusca por 12:", "Encontrado na folha", node.keys, "posição", pos)

bpt.remove(30)
bpt.display()


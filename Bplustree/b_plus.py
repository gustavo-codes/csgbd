class Node:
    def __init__(self, leaf = False):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BPlusTree:
    def __init__(self, order: int):
        self.root = Node(True)
        self.order = order

    def insert(self, key: int):
        root = self.root
        if(len(root.keys) == (2* self.order) - 1):
            temp = Node()
            self.root = temp
            temp.children.append(root)
            self.split_child(temp, 0)
            self.insert_non_full(temp, key)
        else:
            self.insert_non_full(root, key)

    def insert_non_full(self, node, key):
        if node.leaf:
            node.keys.append(key)
            node.keys.sort()
        else:
            i = len(node.keys) - 1
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.order) - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self.insert_non_full(node.children[i], key)

    def split_child(self, parent, index):
        order= self.order
        child = parent.children[index]
        new_child = Node(child.leaf)
        parent.keys.insert(index, child.keys[order-1])
        parent.children.insert(index + 1, new_child)
        new_child.keys = child.keys[order:(2*order) - 1]
        child.keys = child.keys[0:order-1]
        if not child.leaf:
            new_child.children = child.children[order:2*order]
            child.children = child.children[0:order]


    def in_order_traversal(self, node):
        keys = []
        if node.leaf:
            return node.keys
        for i, key in enumerate(node.keys):
            keys.extend(self.in_order_traversal(node.children[i]))
            keys.append(key)
        keys.extend(self.in_order_traversal(node.children[-1]))
        return keys

    def search(self, key: int) -> any:
        node = self.root
        while not node.leaf:
            # encontra o filho correto usando bisect (ou loop linear)
            i = 0
            while i < len(node.keys) and key >= node.keys[i]:
                i += 1
            node = node.children[i]

            # agora estamos em um nó folha
            try:
                idx = node.keys.index(key)
                return node, idx          # encontrado
            except ValueError:
                return None, None  
            
    def _min_keys(self):
        return (self.order + 1) // 2      # ceil(order/2)

    def _borrow_from_left(self, parent, idx, node, left_sibling):
        """Empresta a maior chave de left_sibling."""
        # move a última chave de left_sibling para node
        borrowed_key = left_sibling.keys.pop(-1)
        node.keys.insert(0, borrowed_key)

        # atualiza a chave separadora no pai
        parent.keys[idx - 1] = node.keys[0]

    def _borrow_from_right(self, parent, idx, node, right_sibling):
        """Empresta a menor chave de right_sibling."""
        borrowed_key = right_sibling.keys.pop(0)
        node.keys.append(borrowed_key)

        # atualiza a chave separadora no pai
        parent.keys[idx] = right_sibling.keys[0]

    def _merge_nodes(self, parent, idx, left_node, right_node):
        """Fundir left_node e right_node; a chave separadora do pai vai para o novo nó."""
        # a chave do pai que separa os dois filhos
        separator = parent.keys.pop(idx)
        left_node.keys.append(separator)
        left_node.keys.extend(right_node.keys)

        if not left_node.leaf:
            left_node.children.extend(right_node.children)

        # remover o ponteiro ao nó direito
        parent.children.pop(idx + 1)

        # Se a raiz ficou vazia, elevamos o filho único
        if parent is self.root and len(parent.keys) == 0:
            self.root = left_node
            
    def _find_parent(self, current, target, parent=None, idx=None):
        if current.leaf:
            return None, None

        for i, child in enumerate(current.children):
            if child is target:
                return current, i
            if not child.leaf:
                p, ci = self._find_parent(child, target, current, i)
                if p:
                    return p, ci
        return None, None

    def _fix_underflow(self, node):
        """Corrige sub‑fluxo em nós internos após uma fusão."""
        if node is self.root:
            # Se a raiz ficou sem chaves, elevamos seu único filho
            if len(node.keys) == 0 and len(node.children) > 0:
                self.root = node.children[0]
            return

        if len(node.keys) >= self._min_keys():
            return  # tudo ok

        # Encontrar pai novamente
        parent, idx = self._find_parent(self.root, node)

        left_sib = parent.children[idx - 1] if idx > 0 else None
        right_sib = parent.children[idx + 1] if idx + 1 < len(parent.children) else None

        if left_sib and len(left_sib.keys) > self._min_keys():
            # emprestar da esquerda (similar ao caso das folhas)
            borrowed_key = left_sib.keys.pop(-1)
            node.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = borrowed_key
            if not node.leaf:
                node.children.insert(0, left_sib.children.pop(-1))
            return

        if right_sib and len(right_sib.keys) > self._min_keys():
            borrowed_key = right_sib.keys.pop(0)
            node.keys.append(parent.keys[idx])
            parent.keys[idx] = borrowed_key
            if not node.leaf:
                node.children.append(right_sib.children.pop(0))
            return

        # Nenhum irmão tem chaves sobrando → fundir
        if left_sib:
            self._merge_nodes(parent, idx - 1, left_sib, node)
        else:
            self._merge_nodes(parent, idx, node, right_sib)

        # Propagar possível sub‑fluxo para cima
        self._fix_underflow(parent)

    def remove(self, key: int):
        leaf, idx = self.search(key)

        # chave inexistente
        if leaf is None:
            return "Chave não encontrada"

        # Excluir a chave da folha
        leaf.keys.pop(idx)

        # Se a folha ainda satisfaz a condição mínima, terminamos
        if leaf is self.root or len(leaf.keys) >= self._min_keys():
            return True

        # Caso contrário, precisamos corrigir o sub‑fluxo
        # Encontrar o pai e o índice do filho correspondente
        parent, child_idx = self._find_parent(self.root, leaf)

        # Tentar emprestar de irmãos
        left_sib = parent.children[child_idx - 1] if child_idx > 0 else None
        right_sib = parent.children[child_idx + 1] if child_idx + 1 < len(parent.children) else None

        if left_sib and len(left_sib.keys) > self._min_keys():
            self._borrow_from_left(parent, child_idx, leaf, left_sib)
            return True
        if right_sib and len(right_sib.keys) > self._min_keys():
            self._borrow_from_right(parent, child_idx, leaf, right_sib)
            return True

        # Nenhum irmão tem chaves suficientes → fundir
        if left_sib:
            self._merge_nodes(parent, child_idx - 1, left_sib, leaf)
        else:
            self._merge_nodes(parent, child_idx, leaf, right_sib)

        # Depois da fusão pode ser que o pai também precise de correção.
        # Propagamos recursivamente enquanto houver sub‑fluxo.
        self._fix_underflow(parent)
        return True

    def display(self):
        if self.root is not None:
            print(self.in_order_traversal(self.root)) 
        else:
            print("Vazio")

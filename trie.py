class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False

class TrirTree:
    def __init__(self):
        self.root = TrieNode()

    def search(self, prefix):
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return []
        match = []
        stack = [(node, prefix)]
        while stack:
            curr_node, chars_match = stack.pop()
            if curr_node:
                if curr_node.end:
                    match.append(chars_match)
                for char, next_node in curr_node.children.items():
                    stack.append((next_node, chars_match + char))
        return match

    def add(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        if node.end:# already exists
            return False
        node.end = True
        return True

    def delete(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False #doesn't exist
            node = node.children[char]
        if not node.end:
            return False
        node.end = False
        return True
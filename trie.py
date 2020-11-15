class TrieNode:
    def __init__(self):
        self.children = {}
        self.end = False
        self.popularity = 0
        self.word = None

class TrirTree:
    def __init__(self):
        self.root = TrieNode()

    def search(self, prefix):
        """ search a prefix """
        node = self.root
        for char in prefix:
            equivalent_char = self.equivalent(char)
            if not equivalent_char:
                equivalent_char = char
            if char in node.children or equivalent_char in node.children:
                if char in node.children:
                    node = node.children[char]
                else:
                    node = node.children[equivalent_char]
            else:
                return []
        match = []
        stack = [node]
        while stack:
            curr_node = stack.pop()
            if curr_node:
                if curr_node.end:
                    match.append((curr_node.word, curr_node.popularity))
                for char, next_node in curr_node.children.items():
                    stack.append(next_node)
        sorted_match = sorted(match, key=lambda x: x[0])
        result = [k for k, _ in sorted(sorted_match, key=lambda x: x[1], reverse=True)]
        final = []
        for loc in result:
            new_loc = ""
            for c in loc:
                if c == '_':
                    new_loc += ' '
                else:
                    new_loc += c
            final.append(new_loc)
        return final

    def add(self, word, popularity):
        """ add a word """
        node = self.root
        for char in word:
            equivalent_char = self.equivalent(char)
            if not equivalent_char:
                equivalent_char = char
            if char not in node.children and equivalent_char not in node.children:
                node.children[char] = TrieNode()
            if char in node.children:
                node = node.children[char]
            else:
                node = node.children[equivalent_char]
        if node.end:
            """ already exists """
            return False
        node.end = True
        node.popularity = popularity
        node.word = word
        return True

    def delete(self, word):
        """ delete a word """
        node = self.root
        for char in word:
            equivalent_char = self.equivalent(char)
            if not equivalent_char:
                equivalent_char = char
            if char not in node.children and equivalent_char not in node.children:
                """ the word doesn't exist """
                return False
            if char in node.children:
                node = node.children[char]
            else:
                node = node.children[equivalent_char]
        if not node.end:
            """ the word doesn't exist """
            return False
        node.end = False
        node.popularity = 0
        return True

    def equivalent(self, char):
        if char == '_':
            return ' '
        if char == ' ':
            return '_'
        if 96 < ord(char) < 123:
            """ lower letter to  upper letter """
            return chr(ord(char) - 32)
        if 64 < ord(char) < 91:
            """ upper letter to  lower letter """
            return chr(ord(char) + 32)
        return None
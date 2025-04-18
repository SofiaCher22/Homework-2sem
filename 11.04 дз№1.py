#1
class TrieNode:
    def __init__(self):
        self.children = {} 
        self.is_end = False 
        self.suffix_index = -1  

class Trie:
    def __init__(self, alphabet='$abcdn'):
        self.root = TrieNode()
        self.alphabet = alphabet
        self.pos = {char: idx for idx, char in enumerate(alphabet)}
        self.suffix_array_cache = {}
        self.lcp_cache = {}
    def _calc_position(self, count):
        for i in range(1, len(count)):
            count[i] += count[i-1]
        return count

    def _build_suffix_array(self, s):
        if s in self.suffix_array_cache:
            return self.suffix_array_cache[s]
        
        s = s + '$'
        count = [0] * len(self.alphabet)
        for char in s:
            count[self.pos[char]] += 1
        count = self._calc_position(count)

        p = [0] * len(s)
        for i in range(len(s)-1, -1, -1):
            count[self.pos[s[i]]] -= 1
            p[count[self.pos[s[i]]]] = i

        c = [0] * len(s)
        cn = 0
        last_char = '$'
        for i in range(len(p)):
            if s[p[i]] != last_char:
                last_char = s[p[i]]
                cn += 1
            c[p[i]] = cn

        cur_len = 1
        while cur_len <= len(s):
            sorted2 = [(p[i] - cur_len) % len(s) for i in range(len(s))]
            
            count = [0] * len(s)
            for i in sorted2:
                count[c[i]] += 1
            count = self._calc_position(count)
            
            new_p = [0] * len(s)
            for i in range(len(sorted2)-1, -1, -1):
                count[c[sorted2[i]]] -= 1
                new_p[count[c[sorted2[i]]]] = sorted2[i]
            p = new_p
            
            new_c = [0] * len(s)
            cN = 0
            for i in range(1, len(p)):
                mid1 = (p[i] + cur_len) % len(s)
                mid2 = (p[i-1] + cur_len) % len(s)
                if c[p[i]] != c[p[i-1]] or c[mid1] != c[mid2]:
                    cN += 1
                new_c[p[i]] = cN
            c = new_c
            cur_len *= 2

        self.suffix_array_cache[s[:-1]] = p
        return p

    def _build_lcp(self, s):
        if s in self.lcp_cache:
            return self.lcp_cache[s]
        
        sa = self._build_suffix_array(s)
        s = s + '$'
        lcp = [0] * len(sa)
        pos = [0] * len(sa)
        
        for i in range(len(sa)):
            pos[sa[i]] = i
        
        k = 0
        for i in range(len(s)):
            k = max(k-1, 0)
            if pos[i] == len(s)-1:
                lcp[pos[i]] = 0
                k = 0
                continue
            else:
                j = sa[pos[i]+1]
                while i+k < len(s) and j+k < len(s) and s[i+k] == s[j+k]:
                    k += 1
                lcp[pos[i]] = k
        
        self.lcp_cache[s[:-1]] = lcp
        return lcp

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        self.suffix_array_cache.clear()
        self.lcp_cache.clear()

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def delete(self, word):
        def _delete_helper(node, word, index):
            if index == len(word):
                if not node.is_end:
                    return False
                node.is_end = False
                return len(node.children) == 0
            char = word[index]
            if char not in node.children:
                return False
            should_delete = _delete_helper(node.children[char], word, index+1)
            if should_delete:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end
            return False

        _delete_helper(self.root, word, 0)
        self.suffix_array_cache.clear()
        self.lcp_cache.clear()

    def count_unique_substrings(self, s):
        lcp = self._build_lcp(s)
        total = (len(s) * (len(s) + 1)) // 2 - sum(lcp)
        return int(total)

    def compare_substrings(self, s, l1, r1, l2, r2):
        if (r1 - l1) != (r2 - l2):
            return False
        lcp = self._build_lcp(s)
        sa = self._build_suffix_array(s)
        pos = {sa[i]: i for i in range(len(sa))}
        min_lcp = min(lcp[min(pos[l1], pos[l2]):max(pos[l1], pos[l2])])
        return min_lcp >= (r1 - l1 + 1)
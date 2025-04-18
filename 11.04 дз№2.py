#2
class PatternMatcher:
    def __init__(self, alphabet='$abcdefghijklmnopqrstuvwxyz'):
        self.alphabet = alphabet
        self.pos = {char: idx for idx, char in enumerate(alphabet)}
    
    def _calc_position(self, count):
        for i in range(1, len(count)):
            count[i] += count[i-1]
        return count
    
    def build_suffix_array(self, text):
        text = text + '$'
        count = [0] * len(self.alphabet)
        for char in text:
            count[self.pos[char]] += 1
        count = self._calc_position(count)

        p = [0] * len(text)
        for i in range(len(text)-1, -1, -1):
            count[self.pos[text[i]]] -= 1
            p[count[self.pos[text[i]]]] = i

        c = [0] * len(text)
        cn = 0
        last_char = '$'
        for i in range(len(p)):
            if text[p[i]] != last_char:
                last_char = text[p[i]]
                cn += 1
            c[p[i]] = cn

        cur_len = 1
        while cur_len <= len(text):
            sorted2 = [(p[i] - cur_len) % len(text) for i in range(len(text))]
            
            count = [0] * len(text)
            for i in sorted2:
                count[c[i]] += 1
            count = self._calc_position(count)
            
            new_p = [0] * len(text)
            for i in range(len(sorted2)-1, -1, -1):
                count[c[sorted2[i]]] -= 1
                new_p[count[c[sorted2[i]]]] = sorted2[i]
            p = new_p
            
            new_c = [0] * len(text)
            cN = 0
            for i in range(1, len(p)):
                mid1 = (p[i] + cur_len) % len(text)
                mid2 = (p[i-1] + cur_len) % len(text)
                if c[p[i]] != c[p[i-1]] or c[mid1] != c[mid2]:
                    cN += 1
                new_c[p[i]] = cN
            c = new_c
            cur_len *= 2

        return p
    
    def build_lcp_array(self, text, sa):
        text = text + '$'
        lcp = [0] * len(sa)
        pos = [0] * len(sa)
        
        for i in range(len(sa)):
            pos[sa[i]] = i
        
        k = 0
        for i in range(len(text)):
            k = max(k-1, 0)
            if pos[i] == len(text)-1:
                lcp[pos[i]] = 0
                k = 0
                continue
            else:
                j = sa[pos[i]+1]
                while i+k < len(text) and j+k < len(text) and text[i+k] == text[j+k]:
                    k += 1
                lcp[pos[i]] = k
        
        return lcp
    
    def count_occurrences(self, text, pattern):

        rotations = [pattern[i:] + pattern[:i] for i in range(len(pattern))]
        unique_rotations = list(set(rotations))  
        
        sa = self.build_suffix_array(text)
        lcp = self.build_lcp_array(text, sa)
        
        total_count = 0
        
        for rot in unique_rotations:

            count = self._find_pattern_occurrences(text, rot, sa, lcp)
            total_count += count
        
        return total_count
    
    def _find_pattern_occurrences(self, text, pattern, sa, lcp):
        n = len(text)
        m = len(pattern)
        left = 0
        right = n
        first_occurrence = -1
        

        while left < right:
            mid = (left + right) // 2
            suffix = text[sa[mid]:sa[mid]+m]
            if suffix < pattern:
                left = mid + 1
            else:
                right = mid
        
        if left == n or not text[sa[left]:sa[left]+m].startswith(pattern):
            return 0
        
        first_occurrence = left
        right = n
        

        while left < right:
            mid = (left + right) // 2
            suffix = text[sa[mid]:sa[mid]+m]
            if suffix > pattern:
                right = mid
            else:
                left = mid + 1
        
        last_occurrence = right - 1
        return last_occurrence - first_occurrence + 1

matcher = PatternMatcher()
text = "abacabaabacab"
pattern = "aba"

print(f"Общее количество вхождений и циклических сдвигов '{pattern}':")
print(matcher.count_occurrences(text, pattern))  
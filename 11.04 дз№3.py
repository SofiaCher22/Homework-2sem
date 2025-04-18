#3
def string_from_z(z_array):
    if not z_array:
        return ""
    
    n = len(z_array)
    if z_array[0] != 0 and z_array[0] != n:
        raise ValueError()
    
    s = [''] * n
    if z_array[0] == n:
        return 'a' * n
    s[0] = 'a'
    
    cur_char = ord('b')
    
    for i in range(1, n):
        if z_array[i] > 0:
            for j in range(i, i + z_array[i]):
                if j >= n:
                    break
                if s[j] == '':
                    s[j] = s[j - i]
                elif s[j] != s[j - i]:
                    raise ValueError()
        elif s[i] == '':
            s[i] = chr(cur_char)
            cur_char += 1
    
    return ''.join(s)

z = [0, 0, 2, 0, 1, 0]
print(string_from_z(z))
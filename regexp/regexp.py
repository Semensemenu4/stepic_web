
def calculate(data, findall):
    matches = findall( r"([abc])([-+]?)=([abc]?)([-+]?[\d]*)" )
    for v1, s, v2, n in matches:  # Если кортеж такой структуры: var1, [sign]=, [var2], [[+-]number]
        right = data.get(v2, 0) + int(n or 0)
        if s == '+':
            data[v1] = data[v1] + right
        elif s == '-':
            data[v1] = data[v1] - right
        else:
            data[v1] = right

    return data
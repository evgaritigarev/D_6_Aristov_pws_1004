def Censor(value):
    filter = ['пипец', 'даун', 'блин', 'дурак']
    arr = value.split(' ')
    for i in range(len(arr)):
        if arr[i] in filter:
            arr[i] = '*'*len(arr[i])
        print(arr[i])
    return ' '.join(arr)

str = 'Полный пипец, или почем в Голубково шампиньоны.'
print(Censor(str))
from django import template
 
register = template.Library()


@register.filter(name='censor')
def censor(value):
    filter = ['пипец', 'клоун', 'блин', 'дурак']
    arr = value.split(' ')
    for i in range(len(arr)):
        if arr[i] in filter:
            arr[i] = '*'*len(arr[i])
    return ' '.join(arr)
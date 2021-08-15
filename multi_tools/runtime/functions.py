

def lambda_statement(code: str, args=('self', 'value')):

    if args == ('self', 'value'):
        def inner(self, value):

            exec(code, {'self': self, 'value': value})
        return inner
    elif args == ('self',):
        def inner(self):

            eval(code)

        return inner


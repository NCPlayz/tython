from lark import Lark, Transformer
import _ast
from pathlib import Path
import astor


class TythonTransformer(Transformer):
    def start(self, items):
        return _ast.Module(body=items)

    def stmts(self, items):
        return items[0]

    def class_structure(self, items):
        (name,body) = items
        
        return _ast.ClassDef(name=name, body=body, decorator_list=[], bases=[])

    def inherited_class_structure(self, items):
        (name,bases,body) = items

        return _ast.ClassDef(name=name, body=body, decorator_list=[], bases=[bases])

    def class_body(self, items):
        return items

    def field(self, items):
        (identifier,_type) = items[0]
        return _ast.AnnAssign(target=_ast.Name(id=identifier), annotation=_ast.Name(id=_type), value=None, simple=True)

    def class_declarations(self, items):
        (items,) = items
        return items

    def constructor_method(self, items):
        (args,body) = items
        
        method_args = [_ast.arg(arg='self', annotation=None)]
        method_args.extend(args)
        
        return _ast.FunctionDef(name='__init__', args=_ast.arguments(args=method_args, defaults=[], vararg=None, kwarg=None), body=body, decorator_list=[])

    def method(self, items):
        f = self.function(items)

        method_args = [_ast.arg(arg='self', annotation=None)]
        method_args.extend(f.args.args)
        f.args.args = method_args

        return f

    def async_method(self, items):
        f = self.async_function(items)

        method_args = [_ast.arg(arg='self', annotation=None)]
        method_args.extend(f.args.args)
        f.args.args = method_args

        return f

    def decorated_method(self, items):
        (call,meth) = items
        meth.decorator_list.append(call)
        return meth

    def function(self, items):
        if len(items) == 2:
            (name, body) = items
            args = []
        else:
            (name,args,body) = items
        return _ast.FunctionDef(name=name, args=_ast.arguments(args=args, defaults=[], vararg=None, kwarg=None), body=body, decorator_list=[])

    def async_function(self, items):
        if len(items) == 2:
            (name, body) = items
            args = []
        else:
            (name,args,body) = items
        return _ast.AsyncFunctionDef(name=name, args=_ast.arguments(args=args, defaults=[], vararg=None, kwarg=None), body=body, decorator_list=[])

    def constructor_args(self, items):
        return items

    def func_args(self, items):
        return self.constructor_args(items)

    def public_arg(self, items):
        # TODO: sort out public later
        (items,) = items
        return items

    def func_arg(self, items):
        (items,) = items
        identifier = items[0]
        if len(items) == 2:
            type_ = items[1]
        else:
            type_ = None
        
        return _ast.arg(arg=identifier, annotation=type_)

    def func_body(self, items):
        return items

    def func_stmts(self, items):
        (items,) = items
        return items

    def reassign(self, items):
        (attrs,val,_) = items
        
        return _ast.Assign(targets=[attrs], value=val)

    def this_dotted_access(self, items):
        (items,) = items
        return _ast.Attribute(value=_ast.Name(id='self'), attr=items)

    def ret_expr(self, items):
        (items,) = items
        return items

    def return_expr(self, items):
        (items,) = items
        return _ast.Return(value=items)

    def expr(self, items):
        (items,) = items
        return items

    def add(self, items):
        (left,right) = items
        return _ast.BinOp(left=left, op=_ast.Add(), right=right)

    def access(self, items):
        (items,) = items
        return _ast.Name(id=items)

    def dotted_access(self, items):
        attr = None
        for item in items:
            if attr is None:
                attr = item
                continue
            attr = _ast.Attribute(value=attr, attr=item.id)
        return attr

    def types_repr(self, items):
        (items,) = items
        return items

    def str(self, items):
        (items,) = items
        items = items[1:-1]
        return _ast.Constant(value=items)

    def explicit_type(self, items):
        (identifier, _type) = items
        return identifier, _type

    def string(self, items):
        return _ast.Name(id='str')

    def object(self, items):
        (items,) = items
        return _ast.Name(id=items)

    def identifier(self, items):
        (identifier,) = items
        return str(identifier)

    def var(self, items):
        (_,identifier,expr,_) = items
        return _ast.Assign(targets=[_ast.Name(identifier)], value=expr)

    def new_class(self, items):
        identifier = items[0]
        if len(items) > 1:
            args = items[1]
        else:
            args = []
        return _ast.Call(func=_ast.Name(id=identifier), args=args, keywords=[])

    def function_call(self, items):
        return self.new_class(items)

    def async_await(self, items):
        return _ast.Await(value=self.new_class(items))

    def function_call_expr(self, items):
        (items,_) = items
        return _ast.Expr(value=items)

    def call_args(self, items):
        return items

    def call_arg(self, items):
        (items,) = items
        return items

    def terminator(self, items):
        return

    def interface(self, items):
        return self.class_structure(items)

    def interface_body(self, items):
        return self.class_body(items)

    def interface_declarations(self, items):
        return self.class_declarations(items)

    def interface_declaration(self, items):
        return self.field(items)

    def import_reg(self, items):
        (identifier,module,__) = items
        if module.value == identifier:
            names = [_ast.alias(name=module.value, asname=None)]
        else:
            names = [_ast.alias(name=module.value, asname=identifier)]
        return _ast.Import(names=names)

    def import_from(self, items):
        (import_names,_,__) = items
        return _ast.ImportFrom(module=_.value.replace('/', '.'), names=import_names, level=0) # TODO: determine the level properly

    def import_names(self, items):
        return items

    def import_name(self, items):
        (items,) = items
        return _ast.alias(name=items, asname=None)

    def import_as_name(self, items):
        (import_name,as_name) = items
        return _ast.alias(name=import_name, asname=as_name)

grammar = Path(__file__).parent.joinpath('grammar.lark')
parser = Lark.open(grammar)

def parse(code: str, debug: bool = False) -> str:
    tree = parser.parse(code)
    if debug:
        print('TREE' + '-' * 53 + 'TREE')
        print(tree.pretty())
        print('END TREE' + '-' * 45 + 'END TREE')
    program = TythonTransformer().transform(tree)
    code = astor.to_source(program)
    return code

import re
import collections
from copy import deepcopy

class transform(object):
    """
    Transform a datastructure in another using a transformation model
    Inspired from JSON/T
    """
    def __init__(self, *ruless):
        self.rules = dict()
        for rules in ruless:
            for (name, expr) in rules.iteritems():
                self.rules[name] = expr
                if name.find('self'):
                    self.rules['self.%s' % name] = expr

    def __call__(self, data, trim=()):
        self.trim = trim
        self.root = data
        return self.apply(self.root, 'self')

    def apply(self, context, path):
        rule_id = re.sub('\[[0-9]+\]', '[*]', path)
        if rule_id in self.rules:
            rule = self.rules[rule_id]

            if isinstance(rule, collections.Callable):
                rule = rule(context)
            return self.process(rule, context, path)
        else:
            return context

    def execute(self, rule, obj):
        return self.rules[rule](obj)

    def process(self, target, context, path):
        if isinstance(target, e):
            return target.resolve(context, path, self)[0]
        else:
            iter = None
            if isinstance(target, collections.Mapping):
                iter = target.items()
            elif isinstance(target, collections.Sequence) and not isinstance(target, basestring):
                iter = enumerate(target)

            if iter:
                target = deepcopy(target)
                for (k, v) in iter:
                    v = self.process(v, context, path)

                    if v in self.trim:
                        del target[k]
                    else:
                        target[k] = v

            return target

    def eval(self, context, current_path, path=''):
        # Ideally, we would iterate all over the fields to transform them
        if len(path):
            if path[0] == '$':
                return (eval('context'+path[1:]), current_path+path[1:])
            elif not path.find('self'):
                return (eval('self.root'+path[4:]), path)
            else:
                return (eval('self.root.'+path), 'self.'+path)
        else:
            return (context, current_path)

class e(object):
    def __init__(self, expr):
        self.expr = expr

    def resolve(self, context, path, transformer):
        if self.expr and self.expr[0] == '@':
            (func, expr) = re.match('@([^(]+)\(([^)]+)\)', self.expr).groups()
        else:
            (func, expr) = (None, self.expr)
        (evaluated, expanded_path) = transformer.eval(context, path, expr)

        # We avoid recursion by calling apply only if we're not evaluating the same
        # expression as the current_path
        if expanded_path != path:
            evaluated = transformer.apply(evaluated, expanded_path)

        if func:
            evaluated = transformer.execute(func, evaluated)
        return (evaluated, expanded_path)

class s(e):
    def resolve(self, context, path, transformer):
        (evaluated, expanded_path) = super(s, self).resolve(context, path, transformer)

        target = []
        for idx, item in enumerate(evaluated):
            target.append(transformer.apply(item, '%s[%d]' % (expanded_path, idx)))
        return (target, expanded_path+'[*]')


import re
from itertools import product, combinations

def tokenize(s):
    s = s.replace(" ", "")
    if not s:
        raise ValueError("Enter a Boolean expression.")
    t = re.findall(r"[A-Za-z]|[()+.*~'!]", s)
    if "".join(t) != s:
        raise ValueError("Invalid character in expression.")
    out = []
    isvar = lambda x: len(x) == 1 and x.isalpha()
    for i, x in enumerate(t):
        if i:
            p = t[i-1]
            if (isvar(p) or p in (")", "'")) and (isvar(x) or x in ("(", "~", "!")):
                out.append(".")
        out.append(x)
    return out

class Parser:
    def __init__(self, tokens):
        self.t, self.i = tokens, 0
    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None
    def take(self, x=None):
        v = self.peek()
        if v is None or (x is not None and v != x):
            raise ValueError(f"Expected {x or 'a term'}, got {v}.")
        self.i += 1
        return v
    def parse(self):
        n = self.or_expr()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()}")
        return n
    def or_expr(self):
        n = self.and_expr()
        while self.peek() == "+":
            self.take("+")
            n = ("or", n, self.and_expr())
        return n
    def and_expr(self):
        n = self.unary()
        while self.peek() in (".", "*"):
            self.take()
            n = ("and", n, self.unary())
        return n
    def unary(self):
        if self.peek() in ("~", "!"):
            self.take()
            n = ("not", self.unary())
        elif self.peek() == "(":
            self.take("(")
            n = self.or_expr()
            self.take(")")
        elif self.peek() and self.peek().isalpha() and len(self.peek()) == 1:
            n = ("var", self.take().upper())
        else:
            raise ValueError(f"Unexpected token: {self.peek()}")
        while self.peek() == "'":
            self.take("'")
            n = ("not", n)
        return n

def ev(n, vals):
    if n[0] == "var": return bool(vals[n[1]])
    if n[0] == "not": return not ev(n[1], vals)
    if n[0] == "and": return ev(n[1], vals) and ev(n[2], vals)
    if n[0] == "or": return ev(n[1], vals) or ev(n[2], vals)

def binary(n, width):
    return format(n, f"0{width}b")

def combine(a, b):
    diff, out = 0, []
    for x, y in zip(a, b):
        if x == y: out.append(x)
        elif x != "-" and y != "-":
            diff += 1
            out.append("-")
        else: return None
    return "".join(out) if diff == 1 else None

def covers(pattern, bits):
    return all(a == "-" or a == b for a, b in zip(pattern, bits))

def pattern_term(p, variables):
    parts = []
    for bit, v in zip(p, variables):
        if bit == "1": parts.append(v)
        elif bit == "0": parts.append(v + "'")
    return "".join(parts) or "1"

def qm(minterms, variables):
    if not minterms:
        return "0", [], [], []
    w = len(variables)
    current = {binary(m, w): {m} for m in sorted(set(minterms))}
    stages, primes = [], set()
    while True:
        used, nxt, pairs = set(), {}, []
        keys = sorted(current)
        for i, a in enumerate(keys):
            for b in keys[i+1:]:
                c = combine(a, b)
                if c is not None:
                    used.update((a,b))
                    nxt.setdefault(c, set()).update(current[a] | current[b])
                    pairs.append((a,b,c,sorted(current[a] | current[b])))
        new_primes = sorted(p for p in keys if p not in used)
        primes.update(new_primes)
        stages.append({"terms": [(p, sorted(current[p])) for p in keys],
                       "combinations": pairs, "primes": new_primes})
        if not nxt: break
        current = nxt

    target = set(minterms)
    cov = {p: {m for m in target if covers(p, binary(m,w))} for p in sorted(primes)}
    cov = {p:c for p,c in cov.items() if c}
    best = None
    keys = list(cov)
    for size in range(1, len(keys)+1):
        valid = []
        for subset in combinations(keys, size):
            if set().union(*(cov[p] for p in subset)) == target:
                literals = sum(ch != "-" for p in subset for ch in p)
                valid.append((literals, subset))
        if valid:
            best = min(valid)[1]
            break
    selected = list(best or [])
    result = " + ".join(pattern_term(p, variables) for p in selected) or "0"
    return result, stages, sorted(primes), selected

def simplify(expression, max_variables=6):
    tokens = tokenize(expression)
    tree = Parser(tokens).parse()
    variables = sorted({x.upper() for x in tokens if len(x)==1 and x.isalpha()})
    if not variables: raise ValueError("Use at least one variable.")
    if len(variables) > max_variables:
        raise ValueError(f"Maximum supported variables: {max_variables}.")
    rows, mins = [], []
    for bits in product((0,1), repeat=len(variables)):
        vals = dict(zip(variables,bits))
        output = int(ev(tree, vals))
        row = dict(vals)
        row["Output F"] = output
        rows.append(row)
        if output: mins.append(int("".join(map(str,bits)),2))
    result, stages, primes, selected = qm(mins, variables)
    return {"variables":variables, "truth_table":rows, "minterms":mins,
            "result":result, "stages":stages, "prime_patterns":primes,
            "selected_patterns":selected,
            "prime_implicants":[pattern_term(p,variables) for p in primes]}

def evaluate(expression, values):
    tree = Parser(tokenize(expression)).parse()
    return int(ev(tree, {str(k).upper():int(v) for k,v in values.items()}))

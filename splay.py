"""
This code is based on Danny Sleator's public domain Java splay tree code, ported by Anoop Johnson.
See http://www.link.cs.cmu.edu/link/ftp-site/splaying/SplayTree.java

Additional enhancements by Dan Greening
"""

# TODO: Iterator
# TODO: Implement tree['key'] = value behavior (insert includes key and value)

class DuplicateKeyError(Exception):
    pass

class _Node(object):

    def __init__(self, key):
        self.key = key
        self.left = self.right = None

    def __eq__(self,other):
        return isinstance(other, _Node) and self.key == other.key


class SplayTree(object):

    def __init__(self, lessthan=None, equals=None):
        """:lessthen: is a function defining a strict ordering on keys. If not defined, keys are
        compared using __lt__
         "equals: is a function defining equality. If not defined, equality is tested by (not
        (lessthan(a,b) or lessthan(b,a)).

        Typically you would define these using a lambda."""

        self.root = None
        self.header = _Node(None) #For splay()
        if lessthan:
            self.lessthan = lessthan
            if equals:
                self.equals = equals
            else:
                self.equals = lambda a,b: (not self.lessthan(a,b)) and (not self.lessthan(b,a))
        else:
            self.lessthan = lambda a,b: a < b
            if equals:
                raise ValueError("Cannot define equals without defining lessthan for SplayTree")
            self.equals = lambda a,b: a == b

    def insert(self, key):
        if (self.root == None):
            self.root = _Node(key)
            return

        self.splay(key)
        if self.equals(self.root.key, key):
            raise DuplicateKeyError("Key {} already exists".format(key))

        n = _Node(key)
        if self.lessthan(key, self.root.key):
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None
        self.root = n

    def remove(self, key):
        if not self.root:
            raise KeyError('key {} not found in empty SplayTree'.format(key))

        self.splay(key)
        if not self.equals(key, self.root.key):
            raise KeyError('key {} not found in SplayTree'.format(key))

        # Now delete the root.
        if self.root.left == None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x

    def findMin(self):
        if self.root == None:
            return None
        x = self.root
        while x.left != None:
            x = x.left
        self.splay(x.key)
        return x.key

    def findMax(self):
        if self.root == None:
            return None
        x = self.root
        while (x.right != None):
            x = x.right
        self.splay(x.key)
        return x.key

    def find(self, key):
        if self.root == None:
            return None
        self.splay(key)
        if self.equals(self.root.key, key):
            return self.root.key
        return None

    def isEmpty(self):
        return self.root == None
    
    def splay(self, key):
        l = r = self.header
        t = self.root
        self.header.left = self.header.right = None
        while True:
            if self.lessthan(key, t.key):
                if t.left == None: break
                if self.lessthan(key, t.left.key):
                    y = t.left
                    t.left = y.right
                    y.right = t
                    t = y
                    if t.left == None:
                        break
                r.left = t
                r = t
                t = t.left
            elif self.lessthan(t.key, key):
                if t.right == None: break
                if self.lessthan(t.right.key, key):
                    y = t.right
                    t.right = y.left
                    y.left = t
                    t = y
                    if t.right == None: break
                l.right = t
                l = t
                t = t.right
            else:
                break # must be equal!
        l.right = t.left
        r.left = t.right
        t.left = self.header.right
        t.right = self.header.left
        self.root = t

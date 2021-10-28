# Python-ADT-Sugar
A simple preprocessor that extends python with a Haskell-like sintacitc sugar for algebraic data types (kinda).  
🐍 + 🍬 = ❤️  

## Usage
```bash
$ python3 adt.py source.py > target.py
``` 

## Sintaic sugar example

The file `source.py` should looks like this:  
```python
data Tree:
    Empty()
    Node(val, left, rigth)

example = Node(100, Empty(), Empty())

def is_in_tree(x, tree : Tree):

    if isinstance(tree, Empty):
        return False

    if isinstance(tree, Node):
        if tree.val == x:
            return True
        else:
            return is_in_tree(x, tree.left) or is_in_tree(x, tree.rigth)
```

After preprocessing the sintactic sugar, `target.py` would look like this:  
```python
class Tree:
   def __init__(self):
      self.root = True

class Empty(Tree):
   def __init__(self):
      self.root = False

class Node(Tree):
   def __init__(self, val,  left,  rigth):
      self.root = False
      self.val = val
      self.left = left
      self.rigth = rigth

example = Node(100, Empty(), Empty())

def is_in_tree(x, tree : Tree):

    if isinstance(tree, Empty):
        return False

    if isinstance(tree, Node):
        if tree.val == x:
            return True
        else:
            return is_in_tree(x, tree.left) or is_in_tree(x, tree.rigth)
```

from collections import deque 
import math

class Node:
    def __init__(self, depth, value=None, left=None, right=None):
        self.depth = depth
        self.value = value
        self.left = left
        if left:
            self.left.parent = self
        self.right = right
        if right:
            self.right.parent = self
        self.parent = None
    def add(self, Node):
        Node.parent = self
        if not self.left:
            self.left = Node
        else:
            self.right = Node
def parse(line):
    depth = 0
    root = None
    currentNode = None
    for c in line:
        if c == '[':
            newNode = Node(depth)
            if not currentNode:
                root = newNode
            if currentNode:
                currentNode.add(newNode)
            currentNode = newNode
            depth += 1
        elif c == ']':
            depth -= 1
        elif c != ',' and c != ' ':
            newNode = Node(depth, int(c))
            if currentNode:
                currentNode.add(newNode)
            while currentNode and currentNode.right:
                currentNode = currentNode.parent
    return root
def incrementDepth(root):
    if not root:
        return
    else:
        root.depth += 1
        incrementDepth(root.left)
        incrementDepth(root.right)
def printTree(root):
    if not root:
        return ""
    elif root.value is not None:
        return str(root.value)
    else:
        return "[" + printTree(root.left) + "," + printTree(root.right) + "]"
def magnitude(root):
    if not root:
        return
    elif root.value is not None:
        return root.value
    else:
        return 3*magnitude(root.left) + 2*magnitude(root.right)
def reduce(root):
    moreReduction = True
    while moreReduction:
        moreReduction = reduceStep(root)
def reduceStep(root):
    stack = deque()
    currentNode = root
    #find explode candidate
    found = False
    lastLeafFound = None
    explodeRight = None
    while True:
        if not found and currentNode is not None and currentNode.depth >= 4 and currentNode.value is None:
            found = True
            if lastLeafFound:
                lastLeafFound.value += currentNode.left.value
            explodeRight = currentNode.right.value
            currentNode.left = None
            currentNode.right = None
            currentNode.value = 0
            if len(stack) == 0:
                break
            currentNode = stack.popleft()
            currentNode = currentNode.right
        elif currentNode is not None:
            stack.appendleft(currentNode)
            currentNode = currentNode.left
        elif len(stack) > 0:
            currentNode = stack.popleft()
            if currentNode.value is not None:
                if found: #explode right and finish
                    currentNode.value += explodeRight
                    break
                lastLeafFound = currentNode
            currentNode = currentNode.right
        else:
            break
    if found:
        return True
    #find split candidate
    stack.clear()
    currentNode = root
    while not found:
        if currentNode is not None:
            stack.appendleft(currentNode)
            currentNode = currentNode.left
        elif len(stack) > 0:
            currentNode = stack.popleft()
            if currentNode.value is not None and currentNode.value >= 10:
                split(currentNode)
                found = True
            currentNode = currentNode.right
        else:
            break
    return found
def split(node):
    val = node.value
    node.value = None
    node.add(Node(node.depth+1, math.floor(val/2)))
    node.add(Node(node.depth+1, math.ceil(val/2)))

def part1():
    f = open("input18.txt")
    root = None
    for line in f:
        current = parse(line.strip())
        if not root:
            root = current
        else:
            incrementDepth(root)
            incrementDepth(current)
            newRoot = Node(0, None, root, current)
            root = newRoot
        reduce(root)
    return magnitude(root)
def part2():
    f = open("input18.txt").readlines()
    maxMagnitude = 0
    for i in range(0,len(f)):
        for j in range(0,len(f)):
            if i != j:
                tree1 = parse(f[i].strip())
                tree2 = parse(f[j].strip())
                incrementDepth(tree1)
                incrementDepth(tree2)
                root = Node(0,None,tree1,tree2)
                reduce(root)
                mag = magnitude(root)
                maxMagnitude = mag if mag > maxMagnitude else maxMagnitude
    return maxMagnitude

print("Part 1:",part1())
print("Part 2:",part2())
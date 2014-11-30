#!/usr/local/bin/python
import sys

def bin2dll(node):
    """
    :Side-Effects:
        Converts node into a sorted double linked list.
    :Parameters:
        node : `Node`
            The root of a binary search tree.
    :Returns:
        The first node in a sorted doubly linked list.
    :Rtype:
        `Node`
    """
    prev = _bin2dll(node, None)
    while node.left:
        node = node.left
    return node

def _bin2dll(node, prev):
    """
    :Parameters:
        node : `Node`
        prev : `Node`
    """
    if node.left:
        prev = _bin2dll(node.left, prev)
    if prev:
        prev.right = node
    node.left = prev
    prev = node
    if node.right:
        prev = _bin2dll(node.right, prev)
    return prev


class Node(object):
    """
    A node with a left and a right, fit for a Binary Tree or Doubly Linked
    List.
    """
    def __init__(self, data, left, right):
        self.data = data
        self.left = left
        self.right = right

    def printInBstOrder(self):
        if self.left:
            self.left.printInBstOrder()
        print self.data,
        if self.right:
            self.right.printInBstOrder()

    def printLeftToRight(self):
        print self.data,
        if self.right:
            self.right.printLeftToRight()

    @classmethod
    def makeBst(cls, nums):
        nums = sorted(nums)
        return cls._makeBst(nums, 0, len(nums)-1)
        
    @classmethod
    def _makeBst(cls, nums, start, end):
        mid = (start+end)/2
        
        # Left.
        if mid-1 >= start:  
            left = cls._makeBst(nums, start, mid-1)
        else:
            left = None

        # Right.
        if mid+1 <= end:
            right = cls._makeBst(nums, mid+1, end)
        else:
            right = None
        
        return Node(nums[mid], left, right)
    
def main(args):
    nums = [int(arg) for arg in args[1:]]
    node = Node.makeBst(nums)

    print "Nodes as a tree:" 
    node.printInBstOrder()

    print "Nodes as a list:"
    start = bin2dll(node)
    start.printLeftToRight()

if __name__ == '__main__':
    main(sys.argv)

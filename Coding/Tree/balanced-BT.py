# # Given a binary tree, determine if it is height-balanced.

 

# # Example 1:


# # Input: root = [3,9,20,null,null,15,7]
# # Output: true
# # Example 2:


# # Input: root = [1,2,2,3,3,null,null,4,4]
# # Output: false
# # Example 3:

# # Input: root = []
# # Output: true
 

# # Constraints:

# # The number of nodes in the tree is in the range [0, 5000].


# A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.



# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

root = TreeNode(1)
root.left = TreeNode(2)
root.right = TreeNode(3)

root.left.left = TreeNode(4)
root.left.right = TreeNode(5)

root.right.left = TreeNode(6)
root.right.right = TreeNode(7)



class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        
        if root is None:
            return 0
        

        left_subtree = self.isBalanced(root.left)

        if left_subtree == -1:
            return -1 
        right_subtree = self.isBalanced(root.right)

        if right_subtree == -1:
            return -1

        if abs(left_subtree - right_subtree) > 1:
            return -1

        return 1 + max(left_subtree, right_subtree)




obj = Solution()
print(obj.isBalanced(root))
        
        
        
        
        
        
        
        
        
# 103. Binary Tree Zigzag Level Order Traversal
# Solved
# Medium
# Topics
# premium lock icon
# Companies
# Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

 

# Example 1:


# Input: root = [3,9,20,null,null,15,7]
# Output: [[3],[20,9],[15,7]]
# Example 2:

# Input: root = [1]
# Output: [[1]]
# Example 3:

# Input: root = []
# Output: []
 

# Constraints:

# The number of nodes in the tree is in the range [0, 2000].
# -100 <= Node.val <= 100


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

from typing import Optional, List

root = TreeNode(3)
root.left = TreeNode(9)
root.right = TreeNode(20)
root.right.left = TreeNode(15)
root.right.right = TreeNode(7)

from collections import deque

class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        
        if root is None:
            return []
        
        queue = deque([root])
        toggle = True
        res = []
        
        
        while queue:
            curr_length = len(queue)
            level = [-1] * len(queue)

            
            for i in range(len(queue)):
                node = queue.popleft()

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
                
                index = i if toggle else curr_length - i -1

                level[index] = node.val
            res.append(level)
            toggle = not toggle
        
        
        return res

solution = Solution()
print(solution.zigzagLevelOrder(root))
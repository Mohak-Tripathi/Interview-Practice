# 437. Path Sum III
# Medium
# Topics
# premium lock icon
# Companies
# Given the root of a binary tree and an integer targetSum, return the number of paths where the sum of the values along the path equals targetSum.

# The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

 

# Example 1:


# Input: root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
# Output: 3
# Explanation: The paths that sum to 8 are shown.
# Example 2:

# Input: root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
# Output: 3
 

# Constraints:

# The number of nodes in the tree is in the range [0, 1000].
# -109 <= Node.val <= 109
# -1000 <= targetSum <= 1000



# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.

root = TreeNode(10)
root.left = TreeNode(5)
root.right = TreeNode(-3)
root.left.left = TreeNode(3)
root.left.right = TreeNode(2)
root.right.right = TreeNode(11)
root.left.left.left = TreeNode(3)
root.left.left.right = TreeNode(-2)
root.left.right.right = TreeNode(1)


from typing import Optional


class Solution:
    
    def __init__(self):
        self.count = 0
        self.running_sum = 0
        self.counter = {0:1}
    

    def findPath(self, root: Optional[TreeNode], targetSum: int) -> int:

        if root is None:
            return 0
        
        self.running_sum += root.val 
        
        self.count += self.counter.get(self.running_sum - targetSum, 0) 
        
        self.counter[self.running_sum] = self.counter.get(self.running_sum,0) + 1
        
        self.findPath(root.left, targetSum)
        self.findPath(root.right, targetSum)
        
        
        self.counter[self.running_sum] = self.counter.get(self.running_sum) - 1
        self.running_sum -= root.val
        
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> int:

        self.findPath(root, targetSum)
        return self.count



solution = Solution()
print(solution.pathSum(root, 8))
        
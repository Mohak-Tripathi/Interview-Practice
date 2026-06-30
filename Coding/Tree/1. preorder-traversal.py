from typing import Optional, List
class Solution:
    
    def __init__(self):
        self.res = []
   
    def preorderTraversal(self, root) -> List[int]:
        
        
        if root is None:
            return []
        
        self.res.append(root.val)
        
        if root.left:
            self.preorderTraversal(root.left)
        if root.right:
            self.preorderTraversal(root.right)
        
        return self.res



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

obj = Solution()
print(obj.preorderTraversal(root))

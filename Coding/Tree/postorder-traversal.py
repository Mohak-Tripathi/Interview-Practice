from typing import Optional, List
class Solution:
    
    def __init__(self):
        self.res = []
   
    def postorderTraversal(self, root) -> List[int]:
        
        if root is None:
            return []
        
        
        if root.left:
            self.postorderTraversal(root.left)
        if root.right:
            self.postorderTraversal(root.right)
        self.res.append(root.val)
        
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
print(obj.postorderTraversal(root))

from typing import Optional, List
from collections import deque   


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

class Solution:
    
    def __init__(self):
        self.res = []
   
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        
        if root is None:
            return []
        
        queue = deque([root])
        res = []
        
        while queue:
            curr = []
            size_of_curr = len(queue)
            
            for i in range(size_of_curr):
                node  = queue.popleft()
                
                if node.left:
                    queue.append(node.left)
                
                if node.right:
                    queue.append(node.right)
                
                curr.append(node.val)
            
            res.append(curr)
        
        return res
            
        
        


obj = Solution()
print(obj.levelOrder(root))



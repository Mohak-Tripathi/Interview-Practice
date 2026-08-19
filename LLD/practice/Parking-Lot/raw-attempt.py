# # # Online Python compiler (interpreter) to run Python online.
# # # Write Python 3 code in this online editor and run it.
# # print("Start small. Ship something.")

# # class Solution:
# #     def pattern7(self, n):

# #         for i in range(n):
            

# #             for j in range(n-i-1):
# #                 print("", end="")
            
# #             for j in range(2*i+1):
# #                 print("*", end="")
            
# #             for j in range(n-i-1):
# #                 print(" ", end="")
            
# #             print()
    
# #     def pattern8(self, n):

# #         for i in range(n-1,-1,-1):
            

# #             for j in range(n-i-1):
# #                 print("", end="")
            
# #             for j in range(2*i+1):
# #                 print("*", end="")
            
# #             for j in range(n-i-1):
# #                 print(" ", end="")
            
# #             print()
                

# # obj = Solution()
# # obj.pattern7(5)
# # obj.pattern8(5)






# # class Solution:
# #     def selectionSort(self, nums):

# #         n = len(nums)

# #         for i in range(n):

# #             curr_min = i 
# #             for j in range(i+1, n):

# #                 if nums[j]<nums[curr_min]:
# #                     curr_min = j
            

# #             nums[i], nums[curr_min] = nums[curr_min], nums[i] 
        
# #         return nums



# # obj = Solution()
# # print(obj.selectionSort([5, 2, 3, 1, 4]))




# class Solution:
#     def bubbleSort(self, nums):

#         n = len(nums)
#         for i in range(n):

#             for j in range(n-i-1):

#                 if nums[j] > nums[j+1]:

#                     nums[j], nums[j+1] = nums[j+1], nums[j]
        
#         return nums



# obj = Solution()
# print(obj.bubbleSort([5, 2, 3, 1, 4]))







# class Solution:
#     def pattern11(self, n):

#         for i in range(n):

#             start_num =  i % 2 == 0 

#             for j in range(i+1):

#                 print("1" if start_num==True else "0", end="")

#                 start_num = not start_num

#             print()

# obj = Solution()
# obj.pattern11(5)






# class Solution:
#     def pattern10(self, n):
        
        
#         for i in range(1, 2*n):
#             if i > n:
#                 for j in range(2*n-i):
#                     print("*", end="")
#                 print()

#             else:
#                 for j in range(i):
#                     print("*", end="")
#                 print()

# obj = Solution()
# print(obj.pattern10(5))






# class Solution:
#     def pattern12(self, n):

#         for i in range(1, n+1):
#             for j in range(1, i+1):
#                 print(j, end="")
#             for j in range(2*(n-i)):
#                 print(" ", end="")
#             for j in range(i, 0,-1):
#                 print(j, end="")
#             print()

# obj = Solution()
# obj.pattern12(5)





# class Solution:
#     def pattern13(self, n):

#         counter = 1

#         for i in range(1, n+1):
#             char = 97
#             for j in range(1, i+1):
#                 print(counter, end="")
#                 counter += 1
#             print()

# obj = Solution()
# obj.pattern13(5)



# class Solution:
#     def pattern14(self, n):

#         for i in range(1, n+1):
#             char = 64 
#             for j in range(1, i+1):
#                 print(chr(char+j), end="")
#             print()

# obj = Solution()
# obj.pattern14(5)




# # class Solution:
# #     def pattern17(self, n):

# #         for i in range(1, n+1):
# #             start_char = 69- i
# #             for j in range(1, i+1):
# #                 print(chr(start_char+j), end="")
# #             print()

# # obj = Solution()
# # obj.pattern17(5)



# # 1     1
# # 12   21
# # 123 321
# # 12344321




# # class Solution:
# #     def smallestNumber(self, n: int, t: int) -> int:


# #         def digit_product(num):

# #             product = 1
# #             while num >0:
# #                 product *= (num % 10)

# #                 num = num//10 
            
# #             return product
      



# #         while True:

# #             digit_prod = digit_product(n)
# #             print(digit_prod)

# #             if digit_prod % t == 0:
# #                 return n
# #             else:
# #                 n +=1

# # obj = Solution()
# # print(obj.smallestNumber(10, 2))








# class Solution:
#     def mergeSort(self, nums):

#         def merge(nums, left, mid, right):

#             temp = []

#             low = left 
#             high = mid+1

#             while low <= mid and high <= right:

#                 if nums[low] <= nums[high]:
#                     temp.append(nums[low])
#                     low+=1
#                 else:
#                     temp.append(nums[high])
#                     high+=1
            
#             while low <= mid:
#                 temp.append(nums[low])
#                 low+=1
            
#             while high <= right:
#                 temp.append(nums[high])
#                 high+=1
            
#             for i in range(left, right+1):
#                 nums[i] = temp[i-left]
                
#         def MergeSortFunction(nums, left, right):

#             if left >= right:
#                 return 


#             mid = (left+right)//2

#             MergeSortFunction(nums, left, mid)
#             MergeSortFunction(nums, mid+1, right)

#             merge(nums, left, mid, right)
        
#         MergeSortFunction(nums, 0, len(nums)-1)
#         return nums

# obj = Solution()
# print(obj.mergeSort([5, 2, 3, 1, 4]))





# class Solution:
#     def bubbleSort(self, nums):
#         def recursive_bubble_sort(nums, i, n):

#             if i >= n:
#                 return

            

#             for j in range(n-i-1):

#                 if nums[j] > nums[j+1]:
#                     nums[j], nums[j+1] = nums[j+1], nums[j]

#             recursive_bubble_sort(nums, i+1, n)


#         recursive_bubble_sort(nums, 0, len(nums))   
#         return nums
# obj = Solution()
# print(obj.bubbleSort([5, 2, 3, 1, 4,9,7,6,8]))







# from typing import List

# class Solution:
#     def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:

#         result = []

#         def MyCombinationSum(candidates, num, target, i):

      
#             if target==0:

#                 result.append(num.copy())
#                 return 
            
#             if target <0:
#                 return 
            
#             for start in range(i, len(candidates)):
#                 num.append(candidates[start])
#                 MyCombinationSum(candidates, num, target-candidates[start], start)
#                 num.pop()

        
#         MyCombinationSum(candidates, [], target, 0)
#         return result


            

# obj = Solution()
# print(obj.combinationSum([2, 3, 6, 7], 7))






class Solution:
    def countSubsequenceWithTargetSum(self, nums, k):
        #your code goes here
        


        def CountSubsequence(nums, target, i):

            if target == 0:
                return 1
            
            if target < 0 or i >= len(nums):
                return 0
            

            pick = CountSubsequence(nums, target - nums[i], i+1)

            non_pick = CountSubsequence(nums, target, i+1)
            return pick + non_pick

        
        return CountSubsequence(nums, k, 0)


obj = Solution()
print(obj.countSubsequenceWithTargetSum([4, 9, 2, 5, 1] , 10))








class Solution:
    def checkSubsequenceSum(self, nums, k):
        #your code goes here

        def CheckSubsequence(nums, target, i):

            if target == 0:
                return True
            
            if target < 0 or i >= len(nums):
                return False
            
            pick = CheckSubsequence(nums, target - nums[i], i+1)
            non_pick = CheckSubsequence(nums, target, i+1)
            return pick or non_pick 
        
        return CheckSubsequence(nums, k, 0)

obj = Solution()
print(obj.checkSubsequenceSum([4, 9, 2, 5, 1] , 10))







# # Definition for a Node.
# class ListNode:
#     def __init__(self, data, prev=None, next=None):
#         self.data = data
#         self.prev = prev
#         self.next = next


# class Solution:
#     def insertBeforeHead(self, head: ListNode, X: int) -> ListNode:
#         # Your code goes here
#         new_node =  ListNode(X, None, head)

#         new_node.next = head 
#         head.prev = new_node
#         return new_node

# obj = Solution()
# print(obj.insertBeforeHead(ListNode(1), 2))




# class Solution:
#     def climbStairs(self, n: int) -> int:



#         def recursiveFunction(n, i,dp):

#             if i ==n:
#                 return 1
#             if i >n:
#                 return 0

            
#             if dp[i] != -1:
#                 return dp[i]
#             dp[i] = recursiveFunction(n, i+1, dp) + recursiveFunction(n,i+2, dp)
#             return dp[i]

             

#         dp = [-1] * (n+1)
#         return recursiveFunction(n,0, dp)
        

# obj = Solution()
# print(obj.climbStairs(3))



from typing import List



class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:



        def backtrack(n,k,ans,ds, i):

            if len(ds) == k and sum(ds)==n:

                ans.append(ds.copy())
                return 
            
            if sum(ds) > n:
                return 

            
            for start in range(i, 10):

                ds.append(start)
                backtrack(n,k,ans,ds, start+1)
                ds.pop()

        ans = []
        ds = []
        backtrack(n,k,ans,ds, 1)
        return ans

obj = Solution()
print(obj.combinationSum3(3, 9))




# 

class Solution:
    def partition(self, s: str) -> List[List[str]]:

        def ifPalindrome(st):
            
            for i in range(len(st)//2):
                if st[i] != st[len(st)-1-i]:
                    return False
            
            return True


        def palindromicPartition(start, path,s,ans):

            if start == len(s):

                ans.append(path.copy())
                return
            
            for i in range(start, len(s)):
                piece = s[start:i+1]

                if ifPalindrome(piece):
                    path.append(piece)
                    palindromicPartition(i+1, path,s,ans)
                    path.pop()
            

        path = []
        ans = []
        palindromicPartition(0, path,s,ans)

        return ans
        

        
obj = Solution()
print(obj.partition("aab"))





from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:

        #powerset

        n = len(nums)
        ans = []

        subsetsCount = 1 << n

        for num in range(subsetsCount):

            subset = []

            for j in range(n):
                if (num & (1 << j)):
                    subset.append(nums[j])
            
            ans.append(subset)
        
        return ans
        
obj = Solution()
print(obj.subsets([1, 2, 3]))



















# ==================

# Job sequencing Problem
# Subscribe to TUF+

# Hints
# Company
# Given an 2D array Jobs of size Nx3, where Jobs[i][0] represents JobID , Jobs[i][1] represents Deadline , Jobs[i][2] represents Profit associated with that job. Each Job takes 1 unit of time to complete and only one job can be scheduled at a time.



# The profit associated with a job is earned only if it is completed by its deadline. Find the number of jobs and maximum profit.


# Example 1

# Input : Jobs = [ [1, 4, 20] , [2, 1, 10] , [3, 1, 40] , [4, 1, 30] ]

# Output : 2 60

# Explanation : Job with JobID 3 can be performed at time t=1 giving a profit of 40.

# Job with JobID 1 can be performed at time t=2 giving a profit of 20.

# No more jobs can be scheduled, So total Profit = 40 + 20 => 60.

# Total number of jobs completed are two, JobID 1, JobID 3.

# So answer is 2 60.

class Solution:
    def JobScheduling(self, Jobs):
        #your code goes here

        count, max_profit = 0, 0 
        n = len(Jobs)

        max_deadline = 0 
        for idx, deadline, profit  in Jobs:
            max_deadline = max(max_deadline, deadline)
            
        job_assertion = [-1] * (max_deadline + 1)


        Jobs.sort(key=lambda x:x[2], reverse=True)
        for idx, deadline, profit  in Jobs:

            while deadline > 0 and job_assertion[deadline] != -1:
                deadline -=1
            
            if deadline >0:
                job_assertion[deadline] = idx 
                count += 1
                max_profit += profit 
        
        return count, max_profit

obj = Solution()
print(obj.JobScheduling( [ [1, 2, 100] , [2, 1, 19] , [3, 2, 27] , [4, 1, 25] , [5, 1, 15] ]))




class Solution:
    def findPages(self, nums, m):

        def allocation_posssibility(nums, k, m):

            pages = 0
            count = 1

            for i in range(len(nums)):

                current_pages = pages + nums[i]

                if current_pages <= k:
                    pages += nums[i]
                else:
                    pages = nums[i]
                    count+=1
                
            print(count, pages)
            print("--------------------------------")
            return True if count <= m else False
                

        n = len(nums)
        if m > n:
            return -1
        
        low = max(nums)
        high = sum(nums)
        ans = -1

        while low <= high:

            k = (low+high)//2

    
            if allocation_posssibility(nums,k,m):
                ans = k
                high = k -1
            else:
                low = k + 1
        
        return ans
        



obj = Solution()
print(obj.findPages([12, 34, 67, 90], 2))








class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        n = len(matrix)
        m = len(matrix[0])
        top = 0
        left  = 0
        right = m-1
        bottom = n-1
        count = 0
        res = []

        while left <= right and top <= bottom and count <= m * n:


            for i in range(left, right+1):
                if count < m *n:
                    res.append(matrix[top][i])
                    count+=1
            
            top +=1

            for i in range(top, bottom+1):
                if count < m * n:
                    res.append(matrix[i][right])
                    count+=1
            
            right -= 1

            for i in range(right, left-1, -1):
                if count < m * n:
                    res.append(matrix[bottom][i])
                    print(matrix[bottom][i], "kooko")
                    count+=1
            bottom -=1

            for i in range(bottom, top-1,-1):
                if count < m * n:
                    res.append(matrix[i][left])
                    count +=1
            left+=1
        
        return res



obj = Solution()
print(obj.spiralOrder([[1, 2, 3], [4, 5, 6], [7, 8, 9]]))











       
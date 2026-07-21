nums1=input('请输入数组： ').split(',')
nums1_list=[int(i) for i in nums1]
nums2=input('请输入数组： ').split(',')
nums2_list=[int(i) for i in nums2]
nums3_list=nums1_list+nums2_list
nums3_list.sort()
if len(nums3_list)%2==0:
    median=(nums3_list[len(nums3_list)//2-1]+nums3_list[len(nums3_list)//2])/2 #/返回浮点数，//向下取整。而切片时，索引必须是整数。

    print('中位数为：',median)
else:
    median=nums3_list[len(nums3_list)//2]
    print('中位数为：',median)
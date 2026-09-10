import numpy as np
import scipy.stats 
import matplotlib.pyplot as plt

# 计算并绘制 pmf（以二项为例）
x = np.arange(0, 16)
y = scipy.stats.binom.pmf(x, 15, 0.5) # 二项 pmf

# 图1：pmf 折线图
plt.figure()
plt.plot(x, y, 'o-')
plt.title('pmf_line')   

# 图2：pmf 竖线图
plt.figure()
plt.vlines(x, 0, y)
plt.title('pmf_vlines')

# 图3：pmf 柱状图
plt.figure()
plt.bar(x, y)
plt.title('pmf_bar')

# 图4：随机样本直方图
plt.figure()
sim = scipy.stats.binom.rvs(n=15, p=0.5, size=50000)
plt.hist(sim, bins=15)
plt.title('sample_hist')

plt.show()  

"""
其他分布的 pmf
y = scipy.stats.geom.pmf(x, p) # 几何分布(x 从 1 开始，不是 0)
y = scipy.stats.poisson.pmf(x, a) # 泊松分布
y = scipy.stats.randint.pmf(low, high) # 离散均匀，取值 [low, high-1]
"""

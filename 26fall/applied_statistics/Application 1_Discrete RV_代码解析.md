# Application 1: Discrete Random Variables — 代码解析

> 源文件：`Application 1_Discrete RV.ipynb`
> 主题：用计算机仿真 + 概率论研究离散随机变量（二项分布、几何分布、泊松分布在通信系统中的应用）

---

## 一、实验目标

- 计算事件的**经验概率**（empirical，仿真统计）与**理论概率**（theoretical，公式计算）。
- 绘制离散随机变量的**经验直方图**并与**概率质量函数（pmf）** 对比。
- 计算离散随机变量的**经验均值**与**理论均值**。

背景场景：模拟电子邮件的传输过程。邮件被编码为比特流（01 序列），在有噪声的信道上传输会出错；接收方检测到错误后要求重传（TCP 协议），直到收到完全正确的消息为止。

---

## 二、整体代码流程

```
source (随机产生消息)
      │
      ▼
repetition_coder.encode (可选：信道编码，每比特重复 code_length 次)
      │
      ▼
binary_channel.transmit (噪声信道：以 p_error 概率翻转每个比特)
      │
      ▼
repetition_coder.decode (可选：译码，多数表决)
      │
      ▼
count_errors (统计误码数)
      │
      ▼
tcp_connection.transmit (若有误码则整体重传，直到成功；返回传输次数)
      │
      ▼
大量重复试验 → 直方图(经验) vs pmf(理论) 对比
```

三个实验部分：
- **Part a**：单个比特块中的误码数 → **二项分布** Binomial(n, p)
- **Part b**：TCP 成功前所需的传输次数 → **几何分布** Geometric(q)，其中 q = (1-p)^n 是"一次传输完全正确"的概率
- **Part c**：重复编码长度对"平均所需传输总比特数"的影响 → 存在最优码长

---

## 三、类与函数详解

### 3.1 `class source` — 随机消息源

产生随机比特流，相当于"待发送的邮件"。

| 成员 | 作用 |
|---|---|
| `__init__(self, p=0.5, nbits=20)` | 初始化：`p` 为每个比特为 1 的概率，`nbits` 为消息长度（比特数） |
| `message(self)` | 生成并返回一条随机比特流（list） |

关键语法：

```python
list(1*(np.random.rand(self.nbits) > self.p))
```

- `np.random.rand(self.nbits)`：生成 `nbits` 个 [0,1) 均匀分布随机数的 numpy 数组。
- `> self.p`：逐元素比较，得到布尔数组。True 的概率为 `1-p`，即每个比特以 `1-p` 的概率为 1。
- `1 * (...)`：把布尔数组转成 0/1 整数（`True→1, False→0`）。
- `list(...)`：转成 Python 列表返回。

---

### 3.2 `class binary_channel` — 二进制噪声信道

模拟比特在传输中被"翻转"（0↔1）的物理信道。

| 成员 | 作用 |
|---|---|
| `__init__(self, p_error=0.1)` | 初始化为**对称信道**：输入 0 和输入 1 的误码率相同，均为 `p_error` |
| `set_assymmetric(self, p_error0, p_error1)` | 改为**非对称信道**：输入 0 的误码率为 `p_error0`，输入 1 的误码率为 `p_error1` |
| `transmit(self, input_bitstream)` | 逐比特传输，每个比特按对应误码率随机翻转，返回输出比特流 |

关键语法（transmit 内部）：

```python
if b == 1:
    output_bitstream.append( 1 * (np.random.rand() >= self.p_error1) )
else:
    output_bitstream.append( 1 * (np.random.rand() < self.p_error0) )
```

- 输入为 1 时：以 `p_error1` 的概率出错（输出 0），即 `rand() < p_error1` 时翻转；`rand() >= p_error1` 时正确输出 1。
- 输入为 0 时：以 `p_error0` 的概率出错（输出 1），即 `rand() < p_error0` 时输出 1。
- 同样用 `1 * (布尔)` 完成 True/False 到 1/0 的转换。

---

### 3.3 `count_errors(msg_in, msg_out)` — 误码计数函数

统计两条等长比特流之间不同比特的个数。

```python
sum( np.array(msg_in) != np.array(msg_out) )
```

- 先把两个 list 转成 numpy 数组，才能做**逐元素比较** `!=`（list 直接用 `!=` 只会比较整体是否相等）。
- 比较结果是布尔数组，`sum()` 对布尔数组求和时 True 按 1 计，即得到不同位置的个数。

---

### 3.4 `class repetition_coder` — 重复码信道编码器

最简单的信道编码：每个比特重复 `code_length` 次，用冗余换取可靠性。

| 成员 | 作用 |
|---|---|
| `__init__(self, code_length=1)` | 初始化，设定重复次数。`code_length=1` 等于不编码 |
| `encode(self, input_msg)` | 编码：每个比特连续重复 `code_length` 次 |
| `decode(self, input_msg)` | 译码：按 `code_length` 分组，组内**多数表决**（1 的个数超过一半则判为 1） |

关键语法：

```python
# encode
output_msg.extend([b]*self.code_length)   # [b]*n 生成含 n 个 b 的列表，extend 追加到末尾

# decode
for i in range(0, len(input_msg), self.code_length):       # 步长为 code_length，逐块遍历
    output_msg.append( 1 * (sum(input_msg[i:i+self.code_length]) > self.code_length/2.0) )
```

- `range(0, len, step)`：以码长为步长取每块的起始下标。
- `input_msg[i:i+self.code_length]`：列表切片，取出当前块。
- 多数表决：块内 1 的和 > 码长/2 判 1，否则判 0。码长取**奇数**可避免平局。

---

### 3.5 `class tcp_connection` — TCP 可靠传输连接

把编码器 + 信道组合起来，实现"出错就重传，直到完全正确"的 TCP 机制。

| 成员 | 作用 |
|---|---|
| `__init__(self, coder=None, channel=None)` | 初始化。若不传入，默认使用 `repetition_coder()`（码长 1）和 `binary_channel()`（p_error=0.1） |
| `transmit(self, message=[], verbose=False)` | 传输消息直到成功，**返回所需的传输次数**（本实验的核心随机变量） |

transmit 内部逻辑：

1. 空消息检查：`if len(message) == 0: raise Exception(...)` —— 主动抛出异常。
2. `bitstream = self.coder.encode(message)` —— 编码只需做一次，重传的都是同一条编码后的比特流。
3. `while not success` 循环：
   - 经信道传输、译码、`count_errors` 检查；
   - 误码数为 0 → 成功退出循环；否则 `xmit_count += 1` 重传。
4. 保险机制：超过 1000 次仍未成功则强制停止，防止死循环。
5. 返回 `xmit_count`。

关键语法：

- `verbose` 标志位：True 时打印每次尝试的结果，方便观察；批量仿真时设为 False 避免刷屏。
- `raise Exception(...)`：抛出异常终止非法调用。
- 默认参数处理：`if coder == None: self.coder = repetition_coder()` —— 允许用户只传信道、不传编码器。

---

## 四、各代码单元逐步解析

### 4.1 基础演示（cell 4–14）

1. **生成消息**（cell 4）：`source(nbits=10).message()` 产生一条 10 比特随机消息。
2. **信道传输**（cell 6）：用 `p_error=0.5` 的信道传输，然后
   ```python
   errors = list( 1 * (np.array(msg) != np.array(output_msg)) )
   ```
   得到逐比特的误码指示向量（1 表示该位出错），再用 `count_errors` 统计总数。
3. **编码演示**（cell 8）：`[1,0,1]` 经码长 3 的重复码编码为 `[1,1,1,0,0,0,1,1,1]`。
4. **抗错演示**（cell 10）：手工翻转编码后比特流中的 2 个比特：
   ```python
   coded_msg[1] = 1-coded_msg[1]   # 0变1、1变0 的常用写法
   ```
   译码后仍恢复原消息 —— 重复码能容忍每块内少于一半的错误。
5. **TCP 演示**（cell 12）：`p_error=0.15` 信道 + 无编码，`verbose=True` 观察重传过程。
6. **编码 + TCP**（cell 14）：加入码长 3 的重复码，通常重传次数明显减少。

### 4.2 scipy.stats 中的分布（cell 18）

```python
from scipy.stats import binom, geom, poisson
```

三个离散分布的两个核心方法：

| 方法 | 作用 | 示例 |
|---|---|---|
| `.pmf(x, ...)` | 概率质量函数 P(X = x) | `binom.pmf(x, n=10, p=0.4)` |
| `.mean(...)` | 理论均值 E[X] | `geom.mean(p=0.4)` |

绘图要点：

```python
fig, ax = plt.subplots()                        # 同时创建画布和坐标轴
ax.plot(x, pmfs[i,:], '-o', label=..., color=...)  # 实线+圆点
ax.plot(means[i]*np.ones(2), [0, 0.5], ':', ...)   # 用两个相同 x 值画均值竖直虚线
ax.legend(); ax.grid(); plt.show()
```

- `means[i]*np.ones(2)` 构造 `[m, m]` 作为两个点的 x 坐标，配合 y = [0, 0.5] 画出竖线。
- `pmfs = np.zeros((3, npts+1))`：3 行分别存三个分布在各 x 处的 pmf 值，`pmfs[i,:]` 取第 i 行。

### 4.3 Part a：误码数 ~ 二项分布（cell 20）

**问题**：11 个比特经 p=0.25 的信道，误码个数服从什么分布？
**答案**：Binomial(n=11, p=0.25)，每个比特出错是一次伯努利试验。

仿真流程：

```python
error_record = np.zeros(num_trials)          # 预分配数组（比 list.append 高效）
for i in range(num_trials):
    msg = src.message()
    received = ch.transmit(msg)
    error_record[i] = count_errors(msg, received)
```

理论对比：

```python
x = np.arange(0, num_bits+1)                 # pmf 取值点 0..11
y = binom.pmf(x, num_bits, p)                # 理论 pmf
bin_edges = np.arange(-0.5, num_bits+1, 1)   # 直方图边界取 -0.5, 0.5, 1.5, ...
ax.hist(error_record, bins=bin_edges, density=True, ...)
ax.plot(x, y, '-o', ...)
```

关键语法：

- **直方图 bin 边界设在半整数处**（-0.5, 0.5, ...），让每个整数值恰好落在一个 bin 中央 —— 离散数据直方图的标准技巧。
- `density=True`：直方图归一化为概率（面积和为 1），才能与 pmf 直接比较。

后续练习（cell 22/24 留白）：用 `np.mean(error_record > num_bits/2)` 算"超过一半比特出错"的经验频率；理论值用 `1 - binom.cdf(5, 11, 0.25)` 或 `sum(binom.pmf(6:11, ...))`。

### 4.4 Part b：传输次数 ~ 几何分布（cell 26）

**问题**：无编码 TCP，成功所需的传输次数服从什么分布？
**答案**：几何分布 Geometric(q)，参数 q 为"单次传输完全正确"的概率：

```
q = P(11 个比特全对) = (1 - p)^num_bits
```

对应代码：

```python
y = geom.pmf(x, p=np.power((1-p), num_bits))   # np.power 做幂运算
```

仿真循环与 Part a 相同，只是记录的是 `tcp1.transmit(...)` 的返回值（传输次数）。

### 4.5 Part c：最优重复码长（cell 30）

**问题**：编码降低重传次数，但增加了每次传输的比特数。总代价（平均传输总比特数）是否存在最小值？

双重循环结构：

```python
code_lengths = np.arange(1, 15, 2)        # 1,3,5,...,13（取奇数避免译码平局）
for j in range(len(code_lengths)):        # 外层：遍历码长
    coder = repetition_coder(code_length=code_lengths[j])
    tcp = tcp_connection(channel=ch, coder=coder)
    for i in range(num_trials):           # 内层：该码长下做 num_trials 次仿真
        msg = src.message()
        transmit_record[i] = tcp.transmit(message=msg, verbose=False)
    bits_required[j] = num_bits * code_lengths[j] * np.average(transmit_record)
    model[j] = num_bits * code_lengths[j]  # 简单模型：假设一次就成功
```

- 平均总比特数 = 消息比特数 × 码长 × 平均传输次数。
- 简单 model 假设"一次必成功"，只反映比特数随码长线性增长；码长小时严重低估（因为短码重传多），码长大时吻合较好（因为此时一次成功率已接近 1）。

**结论**：经验曲线呈 U 形，存在最优码长；练习（cell 32）要求用概率论改进理论模型（如用几何分布均值 1/q 修正：bits ≈ n·L / q_L，其中 q_L 为码长 L 下单次成功概率）。

---

## 五、核心知识点小结

1. **布尔数组 ↔ 0/1 转换**：`1 * (condition)` 是 numpy 中把条件结果数值化的惯用法。
2. **经验 vs 理论**：`density=True` 的直方图逼近 pmf；仿真均值逼近理论均值（大数定律）。
3. **三大离散分布**：
   - 二项分布 Binomial(n, p)：n 次独立试验中成功次数 → 块内误码数
   - 几何分布 Geometric(q)：首次成功所需试验次数 → TCP 传输次数，q = (1-p)^n
   - 泊松分布 Poisson(μ)：单位时间稀有事件发生次数（本实验仅演示）
4. **信道编码的权衡**：冗余 ↑ ⇒ 单次成功率 ↑、传输次数 ↓，但每次比特数 ↑ ⇒ 总比特数存在最优码长。
5. **离散直方图技巧**：bin 边界取半整数，使整数取值居中。
6. **scipy.stats 接口**：`分布名.pmf(x, 参数)`、`.mean(参数)`、`.cdf(x, 参数)`。

---

## 六、常用语法速查

| 语法 | 含义 |
|---|---|
| `np.random.rand(n)` | n 个 [0,1) 均匀随机数 |
| `np.arange(a, b, step)` | 等差数组 [a, b)，步长 step |
| `np.zeros(shape)` | 全零数组，预分配用 |
| `np.array(list)` | 列表转数组，支持逐元素运算 |
| `np.mean / np.average` | 求均值 |
| `np.power(x, n)` | x 的 n 次幂 |
| `list.extend([b]*n)` | 列表末尾追加 n 个 b |
| `range(0, len, step)` | 按步长遍历下标 |
| `f'...{var}...'` | f-string 格式化输出 |
| `ax.hist(..., bins=..., density=True)` | 归一化直方图 |
| `fig, ax = plt.subplots()` | 面向对象方式创建图形 |

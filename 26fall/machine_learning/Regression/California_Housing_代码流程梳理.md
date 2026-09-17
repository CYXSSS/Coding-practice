# 加州房价回归（California Housing Price Regression）代码流程梳理

对应文件：`California Housing Price Reg - Instructor Version.ipynb`

## 一、任务概览

- **任务**：用回归模型预测加州房价中位数（单位：10 万美元）
- **对比模型**：K 近邻回归（KNN）、线性回归、决策树、神经网络（MLP）
- **调参方法**：用 K 折交叉验证选择神经网络的隐藏层结构和激活函数
- **数据集**：`sklearn.datasets.fetch_california_housing`，20640 个样本，8 个特征
- **评估指标**：MSE、RMSE、R 方（R^2）

8 个输入特征：

| 特征 | 含义 |
|---|---|
| MedInc | 街区收入中位数 |
| HouseAge | 房屋房龄中位数 |
| AveRooms | 平均房间数 |
| AveBedrms | 平均卧室数 |
| Population | 街区人口 |
| AveOccup | 平均居住人数 |
| Latitude | 纬度 |
| Longitude | 经度 |

## 二、整体流程

```text
加载库
    -> Part 1 加载并查看加州房价数据集
    -> Part 2 划分训练集 / 测试集（70% / 30%）
    -> 单独的线性回归演示（先单独训练一次线性回归）
    -> Part 3 定义四个回归模型
    -> Part 4 用相同数据训练并评估四个模型
    -> Part 5 绘制四个模型的测试 MSE 柱状图
    -> Part 6 用 5 折交叉验证为神经网络调参（GridSearchCV）
    -> Part 7 查看全部交叉验证结果
    -> Part 8 用选出的最优神经网络在测试集上做最终评估
```

## 三、各步骤详解

### 加载库

主要使用 scikit-learn：

- 数据与划分：`fetch_california_housing`、`train_test_split`、`KFold`、`GridSearchCV`
- 四个模型：`KNeighborsRegressor`、`LinearRegression`、`DecisionTreeRegressor`、`MLPRegressor`
- 预处理与流程：`StandardScaler`、`Pipeline`
- 评估：`mean_squared_error`、`r2_score`

### Part 1：加载并查看数据集

- `fetch_california_housing(as_frame=True)` 返回 pandas 对象，便于查看
- `X = housing.data`（8 个特征），`y = housing.target`（房价中位数，单位 10 万美元）
- 打印特征名、样本数、特征数和前 5 行样本

### Part 2：划分训练集和测试集

- `train_test_split(X, y, test_size=0.30, random_state=42)`
- 70% 训练、30% 测试，随机种子固定保证可复现

### 线性回归单独演示

在对比四个模型之前，先单独完整走一遍线性回归流程，作为教学示范：

1. `LinearRegression()` 建模（普通最小二乘不需要特征缩放）
2. `fit` 训练后对训练集和测试集分别预测
3. 计算训练 MSE、测试 MSE、测试 RMSE、测试 R 方
4. 结果存入 DataFrame 展示

这部分与 Part 4 的循环逻辑完全一致，是先让学生看清单个模型的完整步骤。

### Part 3：定义四个回归模型

| 模型 | 是否需要标准化 | 关键设置 |
|---|---|---|
| KNN (k=5) | 需要（基于距离计算） | `Pipeline(StandardScaler + KNeighborsRegressor(n_neighbors=5))` |
| 线性回归 | 不需要 | 直接使用 `LinearRegression()` |
| 决策树 | 不需要（按单特征阈值分裂） | `max_depth=10` 限制深度，缓解过拟合 |
| 神经网络 | 需要（训练更稳定） | `Pipeline(StandardScaler + MLPRegressor((50,), relu, max_iter=500, early_stopping=True))` |

**Pipeline 的作用**：把标准化和模型合成一个对象，保证 scaler 只在训练数据上拟合，防止数据泄露。

四个模型存入字典 `models`，方便后面用一个循环统一训练。

### Part 4：训练并评估四个模型

对字典中每个模型执行相同流程：

1. `fit(X_train, y_train)` 训练
2. 分别预测训练集和测试集
3. 计算训练 MSE、测试 MSE、测试 RMSE、测试 R 方
4. 结果追加到 `results` 列表

最后转成 DataFrame，按测试 MSE 从小到大排序打印对比表。

**评估指标含义**：

- **MSE**：平均平方误差，越小越好
- **RMSE**：MSE 开平方，与目标变量同单位，更直观（这里的单位是 10 万美元）
- **R 方**：模型解释目标变异的比例，越接近 1 越好
- **训练 MSE vs 测试 MSE**：两者差距大说明过拟合（决策树会表现得很典型）

### Part 5：可视化对比

用柱状图展示四个模型的测试 MSE，直观对比误差大小。

### Part 6：K 折交叉验证调神经网络超参数

**核心原则：调参只用训练集，测试集不参与。**

1. **新建 Pipeline**：`StandardScaler + MLPRegressor(max_iter=500, early_stopping=True)`。交叉验证时，scaler 会在每个训练折内重新拟合，防止验证折信息泄露。
2. **定义候选参数网格**（共 3 x 3 = 9 种组合）：

   | 参数 | 候选值 |
   |---|---|
   | `model__hidden_layer_sizes` | `(50,)`、`(50, 50)`、`(50, 50, 50)`（1/2/3 个隐藏层，每层 50 神经元） |
   | `model__activation` | `relu`、`tanh`、`logistic` |

   注意前缀 `model__` 表示参数属于 Pipeline 中名为 `model` 的步骤。
3. **5 折交叉验证**：`KFold(n_splits=5, shuffle=True, random_state=42)`，训练集分 5 折，每折轮流做验证，其余 4 折训练。
4. **GridSearchCV**：遍历全部 9 种组合，`scoring="neg_mean_squared_error"`（GridSearchCV 追求分数最大化，所以 MSE 存成负数），`n_jobs=-1` 并行加速。
5. **输出结果**：`best_params_` 给出最优结构，`best_score_` 乘以 -1 还原为正 MSE。GridSearchCV 会自动用最优参数在完整训练集上重新训练，得到 `best_estimator_`。

### Part 7：查看全部交叉验证结果

从 `grid_search.cv_results_` 提取关键列（隐藏层结构、激活函数、验证 MSE、标准差、排名），把负分转回正 MSE，按排名排序打印，便于比较：增加隐藏层是否总是更好？哪种激活函数表现最佳？

### Part 8：最优模型的最终评估

只有在调参完成后，才用选出的最优神经网络 `best_mlp` 在测试集上评估，输出测试 MSE、RMSE、R 方。这才是模型对未见数据泛化能力的可靠估计。

## 四、关键知识点

1. **哪些模型需要特征标准化**：KNN 和神经网络需要（距离/梯度对特征尺度敏感）；线性回归（普通最小二乘）和决策树不需要。
2. **Pipeline 的作用**：把预处理和模型绑定，交叉验证时 scaler 在每折内重新拟合，避免数据泄露。
3. **过拟合**：决策树训练误差远小于测试误差是典型过拟合现象，`max_depth` 可缓解。
4. **调参与评估分离**：超参数选择只能用训练集（交叉验证），测试集只在最后用一次，否则会对测试集过拟合，评估结果失真。
5. **5 折交叉验证**：每个训练样本恰好被用作验证 1 次、用于训练 4 次。
6. **更多隐藏层不一定更好**：可通过交叉验证结果表实证检验。
7. **neg_mean_squared_error**：GridSearchCV 内部最大化分数，MSE 越小越好所以取负号，读结果时要乘 -1 还原。

## 五、可尝试的扩展

- 把决策树换成 `RandomForestRegressor` 或 `GradientBoostingRegressor`，通常会明显优于单棵树
- 扩大神经网络的参数网格（神经元数量、学习率、正则化 `alpha`）
- 绘制真实值 vs 预测值散点图，观察误差的分布形态
- 分析特征重要性（树模型）或排列重要性（permutation importance），理解哪些因素影响房价最大

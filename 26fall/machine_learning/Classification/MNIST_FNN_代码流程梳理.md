# MNIST 手写数字分类（FNN）代码流程梳理

对应文件：`MNIST_FNN_Instructor.ipynb`

## 一、任务概览

- **任务**：手写数字图像分类（0–9 共 10 类）
- **模型**：全连接神经网络（FNN），用 scikit-learn 的 `MLPClassifier` 实现
- **数据**：本地 MNIST NumPy 文件（训练集 60000 张、测试集 10000 张，每张 28×28 灰度图）
- **依赖**：仅 NumPy、Matplotlib、scikit-learn（不需要 TensorFlow）

数据文件目录结构：

```text
Classification/
├── MNIST_FNN_Instructor.ipynb
└── MNIST_Data/
    ├── x_train.npy
    ├── y_train.npy
    ├── x_test.npy
    └── y_test.npy
```

## 二、整体流程

```text
导入库并固定随机种子
    -> Step 1 加载并预处理本地 MNIST 数据
    -> Step 2 可视化样本图像
    -> Step 3 将图像展平为 784 维向量
    -> Step 4 从训练集划分出验证集
    -> Step 5 构建 MLPClassifier 模型
    -> Step 6 训练模型 fit()
    -> Step 7 绘制训练损失曲线
    -> Step 8 绘制内部验证准确率曲线
    -> Step 9 在独立验证集上评估
    -> Step 10 在原始测试集上评估 + 分类报告
    -> Step 11 单张图像预测演示
```

## 三、各步骤详解

### Step 0：导入库并固定随机种子

导入 `numpy`、`matplotlib`、`train_test_split`、`MLPClassifier`，以及评估指标（`accuracy_score`、`classification_report`、`log_loss`）。设置 `RANDOM_STATE = 42` 保证结果可复现。

### Step 1：加载本地 MNIST 数据并预处理

1. 用 `np.load` 读取四个 `.npy` 文件。
2. **归一化**：像素值由 `[0, 255]` 除以 255 缩放到 `[0, 1]`。
3. **增加通道维**：`(n, 28, 28)` 变为 `(n, 28, 28, 1)`，使灰度图的表示更明确（对 MLP 并非必需）。
4. **标签保持整数**（0–9）：scikit-learn 做多分类时不需要像 Keras 那样做 one-hot 编码。
5. 打印各数据形状和类别标签，确认加载正确。

数据规模：

| 数据集 | 图像形状 | 标签形状 |
|---|---|---|
| 训练集 | (60000, 28, 28, 1) | (60000,) |
| 测试集 | (10000, 28, 28, 1) | (10000,) |

### Step 2：可视化样本图像

绘制前 9 张训练图像的 3×3 网格，用 `squeeze()` 去掉通道维（`(28,28,1) -> (28,28)`），`cmap="gray"` 灰度显示，标题显示对应标签。

### Step 3：展平图像

`MLPClassifier` 要求输入是二维矩阵 `(样本数, 特征数)`，因此将每张 28×28×1 的图像展平为 **784 维向量**：

```text
(n, 28, 28, 1) -> (n, 784)
```

同时保存 `image_shape = (28, 28, 1)` 供后续可视化时还原图像使用。

### Step 4：划分验证集

MNIST 已有独立测试集，因此**保持测试集不动**，用 `train_test_split` 从原训练集中再划出 20% 作为验证集：

- `test_size=0.20`：60000 张训练集 -> 48000 训练 + 12000 验证
- `stratify=y_train_full`：按标签分层抽样，保证各类别比例一致
- `random_state=42`：划分可复现

验证集用于开发阶段评估模型，避免反复使用测试集导致"调参过拟合测试集"。

### Step 5：构建神经网络

网络结构：

```text
784 输入 -> 128 个隐藏神经元 -> 10 个输出类别
```

`MLPClassifier` 主要参数：

| 参数 | 取值 | 说明 |
|---|---|---|
| `hidden_layer_sizes` | `(128,)` | 一个隐藏层，128 个神经元 |
| `activation` | `"relu"` | 隐藏层 ReLU 激活函数 |
| `solver` | `"adam"` | Adam 优化器 |
| `alpha` | `0.0001` | L2 正则化强度 |
| `batch_size` | `64` | 小批量大小 |
| `learning_rate_init` | `0.001` | 初始学习率 |
| `max_iter` | `30` | 最大训练轮数 |
| `early_stopping` | `True` | 开启早停 |
| `validation_fraction` | `0.10` | 内部划出 10% 训练数据供早停判断 |
| `n_iter_no_change` | `5` | 连续 5 轮无足够改进则停止 |

### Step 6：训练模型

`model.fit(X_train, y_train)` 一次调用完成完整的学习循环：

1. 前向传播（forward propagation）
2. 损失计算（loss computation）
3. 反向传播（backpropagation）
4. 用 Adam 更新权重

训练结束后打印实际完成的轮数 `model.n_iter_`（早停时小于 30）和最终训练损失 `model.loss_`。

### Step 7：绘制训练损失曲线

`model.loss_curve_` 保存每一轮的训练损失，画折线图观察损失是否持续下降、收敛情况。

### Step 8：绘制内部验证准确率曲线

因为开启了 `early_stopping`，scikit-learn 内部会留出一个验证子集，`model.validation_scores_` 记录每一轮后的内部验证准确率。画出曲线观察泛化能力的变化趋势。

### Step 9：在独立验证集上评估

- `model.predict(X_val)`：得到预测类别
- `model.predict_proba(X_val)`：得到各类别概率
- 用 `accuracy_score` 计算验证准确率，用 `log_loss` 计算验证对数损失

### Step 10：在原始测试集上评估

对 10000 张测试图像做同样评估，输出：

- **测试准确率**和**测试对数损失**
- **分类报告** `classification_report`：每个数字类别的精确率（precision）、召回率（recall）、F1 值及整体均值，用于发现模型在哪几个数字上容易混淆

### Step 11：单张图像预测演示

定义 `predict_sample(idx)` 函数，对测试集中指定样本：

1. 取出展平后的样本，用 `predict_proba` 得到 10 个类别的概率
2. 取概率最大的类别作为预测结果
3. 将向量 reshape 回图像形状并显示
4. 标题显示真实标签、预测标签和置信度，并打印每个数字的概率

演示调用了 `predict_sample(42)` 和 `predict_sample(87)`。

## 四、关键知识点

1. MNIST 每张图像是 28×28 灰度图。
2. 像素值从 `[0,255]` 归一化到 `[0,1]`（代码中的实际实现）。
3. FNN 的输入必须是一维向量，因此图像要展平成 784 个特征。
4. `MLPClassifier` 学习的是从 784 个输入到 10 个类别的非线性映射。
5. 整数标签即可，无需 one-hot 编码。
6. `predict()` 返回预测类别，`predict_proba()` 返回类别概率。
7. MNIST 较简单，基础 FNN 通常就能达到较高准确率（约 97%–98%）。
8. 更复杂的图像数据集一般使用 CNN，因为 CNN 能利用图像的空间结构信息。

## 五、一处值得注意的代码与注释不一致

notebook 中 Markdown 说明及 `predict_sample` 内的注释都声称像素被归一化到 `[-0.5, 0.5]`，并在显示前"加 0.5 还原"。但 Step 1 的实际代码只做了 `/ 255.0`，即归一化到 `[0, 1]`，并未做减 0.5 的平移。因此：

- 训练数据实际范围是 `[0, 1]`，模型训练不受影响；
- `predict_sample` 中 `display_image = normalized_image + 0.5` 会把像素加到 `[0.5, 1.5]`，显示时图像偏亮（`imshow` 会自动裁剪或归一化，视觉效果仍可辨认），属于注释遗留的问题，若要严谨应去掉这行 `+ 0.5`。

## 六、可尝试的改进方向

- 加深/加宽网络，如 `hidden_layer_sizes=(256, 128)`，观察准确率与过拟合变化
- 调整学习率、batch size、正则化强度 `alpha`
- 绘制混淆矩阵，直观查看哪些数字容易互相混淆
- 与 CNN（如 Keras/PyTorch 实现）对比，体会空间结构带来的提升

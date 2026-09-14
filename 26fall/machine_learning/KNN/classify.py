import numpy as np
from sklearn.neighbors import KNeighborsClassifier


if __name__ == "__main__":
    # 简单二分类示例
    X_train = np.array([
        [1, 2], [2, 3], [3, 3],   # A 类
        [6, 6], [7, 8], [8, 7],   # B 类
    ])
    y_train = np.array(["A", "A", "A", "B", "B", "B"])

    # 使用 sklearn 的 KNN 分类器
    knn = KNeighborsClassifier(n_neighbors=3)
    knn.fit(X_train, y_train)

    X_test = np.array([[2, 2], [7, 7], [5, 5]])
    predictions = knn.predict(X_test)
    for x, p in zip(X_test, predictions):
        print(f"样本 {x.tolist()} -> 预测类别: {p}")

    # 也可以输出预测概率
    probabilities = knn.predict_proba(X_test)
    print("\n预测概率:")
    print(probabilities)

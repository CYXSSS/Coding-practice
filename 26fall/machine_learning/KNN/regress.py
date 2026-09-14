from sklearn.neighbors import KNeighborsRegressor
estimator = KNeighborsRegressor(n_neighbors=2)

X = [[0,0,1],
    [1,1,0],
    [3,10,10],
    [4,11,12]]
y = [0.1,0.2,0.3,0.4]

estimator.fit(X, y)
y_pred = estimator.predict([[3,11,10]])
print(y_pred)

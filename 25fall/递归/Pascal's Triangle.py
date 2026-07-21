def pascal_triangle(n):
    if n == 1:  ### Base case: the first row
        return [[1]]
    else:   ### Recursive case: build the triangle up to (n-1) rows
        triangle = pascal_triangle(n - 1)
        prev_row = triangle[-1]
        # generate the new row with edge 1s and inner elements as sum of two above
        new_row = [1]
        for i in range(1, len(prev_row)):
            new_row.append(prev_row[i-1] + prev_row[i])
        new_row.append(1)
        triangle.append(new_row)
        return triangle

# test
for row in pascal_triangle(5):
    print(row)
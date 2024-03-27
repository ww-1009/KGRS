
my_dict = {'a': 10, 'b': 20, 'c': 5}

# 获取值最大的前五个键值对
sorted_items = sorted(my_dict.items(), key=lambda x: x[1], reverse=True)[:5]

# 输出结果
for key, value in sorted_items:
    print(f"Key: {key}, Value: {value}")
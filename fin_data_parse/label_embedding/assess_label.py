# 加载模型
from gensim.models import KeyedVectors

model = KeyedVectors.load_word2vec_format("node2vec_model32.bin", binary=True)

# 指定标签
specific_label = 'Administrator'  # 确保这个标签存在于你的图中
print(model[specific_label])
# 获取与'specific_label'最相似的3个标签
similar_labels = model.most_similar(specific_label, topn=3)

print("与标签 '{}' 最相似的3个标签及其相似度分别是：".format(specific_label))
for label, similarity in similar_labels:
    print("标签: {}, 相似度: {:.4f}".format(label, similarity))
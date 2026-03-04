from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# 1. 配置全局嵌入模型
Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")

# 2. 创建示例文档
texts = [
    "张三是法外狂徒",
    "LlamaIndex是一个用于构建和查询私有或领域特定数据的框架。",
    "我也不知道LlamaIndex是什么，但它听起来很有趣。",
    "它提供了数据连接、索引和查询接口等工具。"
]
docs = [Document(text=t) for t in texts]

# 3. 创建索引并持久化到本地
index = VectorStoreIndex.from_documents(docs)
persist_path = "./llamaindex_index_store"
index.storage_context.persist(persist_dir=persist_path)
print(f"LlamaIndex 索引已保存至: {persist_path}")

# 4. 从本地加载索引并进行相似性搜索
storage_context = StorageContext.from_defaults(persist_dir=persist_path)
loaded_index = load_index_from_storage(storage_context)

query = "什么是LlamaIndex"
retriever = loaded_index.as_retriever(similarity_top_k=2)
results = retriever.retrieve(query)

print(f"查询: {query}")
for i, r in enumerate(results, start=1):
    print("-" * 60)
    print(f"Top {i} score: {r.score}")
    print(r.node.get_content())

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter

loader = TextLoader("../../docs/chapter2/05_text_chunking.md", encoding="utf-8")
docs = loader.load()

# 使用已加载的 Markdown 内容
md_text = docs[0].page_content

# 1) 按标题分块（保留层级元数据）
headers = [
    ("#", "Header1"),
    ("##", "Header2"),
    ("###", "Header3"),
]
md_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)
md_docs = md_splitter.split_text(md_text)

# 2)进一步按长度细分（继承元数据）
res_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", "。", "，", " ", ""],
    chunk_size=200,
    chunk_overlap=10,
)

final_chunks = []
for d in md_docs:
    # 递归切分会自动保留 d.metadata
    final_chunks.extend(res_splitter.split_documents([d]))

print(f"文本被切分为 {len(final_chunks)} 个块。\n")
print("--- 前5个块内容示例 ---")
for i, chunk in enumerate(final_chunks[:5]):
    print("=" * 60)
    print(f'块 {i + 1} \n (元数据: {chunk.metadata}) \n (长度: {len(chunk.page_content)}) \n "{chunk.page_content}"')

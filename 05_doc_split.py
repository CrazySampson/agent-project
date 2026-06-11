import os
from langchain_community.document_loaders import TextLoader,PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 加载文本文件
def load_document(file_path):
    """根据文件类型加载文档内容，目前支持 .txt 和 .pdf"""
    if file_path.endswith(".txt"):
        return TextLoader(file_path).load()
    elif file_path.endswith(".pdf"):
        return PyPDFLoader(file_path).load()
    else:
        raise ValueError("不支持的文件类型")
    

# 文本分割
def split_document(documents, chunk_size=500, chunk_overlap=50):
    """
    使用递归字符分割器将文档分为语义块
    - chunk_size: 每个块的最大字符数
    - chunk_overlap: 块之间的重叠字符数，保持上下文连续性
    """
    test_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", "。", "！", "？", "；", "，", " ", ""], # 优先按段落、行、空格等分割
        length_function=len
        )
    chunks=test_splitter.split_documents(documents)
    print(f"文档已分割成 {len(chunks)} 个块，每块约 {chunk_size} 字符。")

    return chunks

if __name__=="__main__":
    file_path="docs/agent_intro.pdf"

    if not os.path.exists(file_path):
        print(f"文件 {file_path} 不存在，请检查路径。")
    else:
        # 加载文档并分割
        docs = load_document(file_path)
        chunks = split_document(docs, chunk_size=300, chunk_overlap=30)
    # 打印前3个块的内容预览
    print("\n=== 前3个块的内容预览 ===")
    for i,chunk in enumerate(chunks[:3]):
        print(f"\n---块{i+1}--")
        print(f"长度“{len(chunk.page_content)} 字符")
        print(f"内容预览：{chunk.page_content[:200]}...")
        print(f"元数据：{chunk.metadata}")
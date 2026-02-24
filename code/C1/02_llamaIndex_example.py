import os
# os.environ['HF_ENDPOINT']='https://hf-mirror.com'
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.openai_like import OpenAILike
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

load_dotenv()

# 使用 AIHubmix
Settings.llm = OpenAILike(
    model="glm-4.7-flash-free",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    api_base="https://aihubmix.com/v1",
    is_chat_model=True
)

# Settings.llm = OpenAI(
#     model="deepseek-chat",
#     api_key=os.getenv("DEEPSEEK_API_KEY"),
#     api_base="https://api.deepseek.com"
# )

# 加载中文嵌入模型
Settings.embed_model = HuggingFaceEmbedding("BAAI/bge-small-zh-v1.5")

# 加载本地markdown文件并构建索引
docs = SimpleDirectoryReader(input_files=["../../data/C1/markdown/easy-rl-chapter1.md"]).load_data()

index = VectorStoreIndex.from_documents(docs)

query_engine = index.as_query_engine()

print(query_engine.get_prompts())
# {'response_synthesizer:text_qa_template': SelectorPromptTemplate(metadata={'prompt_type': <PromptType.QUESTION_ANSWER: 'text_qa'>}, template_vars=['context_str', 'query_str'], kwargs={}, output_parser=None, template_var_mappings={}, function_mappings={}, default_template=PromptTemplate(metadata={'prompt_type': <PromptType.QUESTION_ANSWER: 'text_qa'>}, template_vars=['context_str', 'query_str'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template='Context information is below.\n---------------------\n{context_str}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {query_str}\nAnswer: '), conditionals=[(<function is_chat_model at 0x0000013994439A80>, ChatPromptTemplate(metadata={'prompt_type': <PromptType.CUSTOM: 'custom'>}, template_vars=['context_str', 'query_str'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, message_templates=[ChatMessage(role=<MessageRole.SYSTEM: 'system'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text="You are an expert Q&A system that is trusted around the world.\nAlways answer the query using the provided context information, and not prior knowledge.\nSome rules to follow:\n1. Never directly reference the given context in your answer.\n2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.")]), ChatMessage(role=<MessageRole.USER: 'user'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text='Context information is below.\n---------------------\n{context_str}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {query_str}\nAnswer: ')])]))]), 'response_synthesizer:refine_template': SelectorPromptTemplate(metadata={'prompt_type': <PromptType.REFINE: 'refine'>}, template_vars=['query_str', 'existing_answer', 'context_msg'], kwargs={}, output_parser=None, template_var_mappings={}, function_mappings={}, default_template=PromptTemplate(metadata={'prompt_type': <PromptType.REFINE: 'refine'>}, template_vars=['query_str', 'existing_answer', 'context_msg'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, template="The original query is as follows: {query_str}\nWe have provided an existing answer: {existing_answer}\nWe have the opportunity to refine the existing answer (only if needed) with some more context below.\n------------\n{context_msg}\n------------\nGiven the new context, refine the original answer to better answer the query. If the context isn't useful, return the original answer.\nRefined Answer: "), conditionals=[(<function is_chat_model at 0x0000013994439A80>, ChatPromptTemplate(metadata={'prompt_type': <PromptType.CUSTOM: 'custom'>}, template_vars=['context_msg', 'query_str', 'existing_answer'], kwargs={}, output_parser=None, template_var_mappings=None, function_mappings=None, message_templates=[ChatMessage(role=<MessageRole.USER: 'user'>, additional_kwargs={}, blocks=[TextBlock(block_type='text', text="You are an expert Q&A system that strictly operates in two modes when refining existing answers:\n1. **Rewrite** an original answer using the new context.\n2. **Repeat** the original answer if the new context isn't useful.\nNever reference the original answer or context directly in your answer.\nWhen in doubt, just repeat the original answer.\nNew Context: {context_msg}\nQuery: {query_str}\nOriginal Answer: {existing_answer}\nNew Answer: ")])]))])}


print(query_engine.query("文中举了哪些例子?"))
# 文中举了选择餐馆、做广告、挖油以及玩游戏的例子。
# temparature默认0.1，因此回答比较保守
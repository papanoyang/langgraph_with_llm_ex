import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

class BaseAgent:
  def __init__(self, name: str) -> None:
    self.name = name
    if "VERBOSE" in os.environ:
      if os.environ.get("VERBOSE") == "1":
        self.verbose = True
      else:
        self.verbose = False
    else:
      self.verbose = False
    if "MODEL" in os.environ:
      self.model = os.environ.get("MODEL")
    else:
      self.model = "gpt-3.5-turbo"
  
  def call_model(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_retries: int = 1, response_format: str = None) -> str:
    # 出力をJSON形式と指定した場合、LLMにOUTPUT形式を指定する。
    optional_params = {}
    if response_format == "json":
      optional_params = {
        "response_format": {"type": "json_object"}
      }
    
    # ChatOpenAIを宣言
    llm = ChatOpenAI(
      model=self.model,
      temperature=temperature,
      max_retries=max_retries,
      model_kwargs=optional_params,
    )

    # PromptTemplateを宣言
    prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("human", "{input}")
    ])

    # Chainning
    chain = prompt | llm

    return chain.invoke({"input": user_prompt}).content
  
  def call_agent(self, system_prompt: str, user_prompt: str, temperature: float = 0.7, max_retries: int = 1) -> str:
    # ChatOpenAIを宣言
    llm = ChatOpenAI(
      model=self.model,
      temperature=temperature,
      max_retries=max_retries,
    )
    # PromptTemplateを宣言
    prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("user", "{input}"),
      ("placeholder", "{agent_scratchpad}")
    ])
    # Search Toolを宣言
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)
    # Agent構成
    agent = create_openai_functions_agent(
      llm=llm, prompt=prompt, tools=[tavily_tool]
    )
    agent_exxcutor = AgentExecutor.from_agent_and_tools(
      agent=agent, tools=[tavily_tool], verbose=self.verbose
    )
    # 実行
    result = agent_exxcutor.invoke({"input": user_prompt, "agent_scratchpad": ""})['output']
    return result

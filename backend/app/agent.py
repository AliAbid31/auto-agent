from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from app.config import GROQ_API_KEY, TAVILIY_API_KEY
from app.rag_engine import get_auto_retriever_tool

def car_agent():
    llm = ChatGroq(
        model="qwen/qwen3.8-27b",
        api_key=GROQ_API_KEY,
        temperature=0.1,
    )

    rag_tool = get_auto_retriever_tool()
    tavily_tool = TavilySearchResults(
        api_key=TAVILIY_API_KEY,
        max_results=3,
        description="Un outil pour rechercher des informations sur l'histoire et l'actualité de l'automobile."
    )

    tools = [rag_tool, tavily_tool]

    system_prompt = (
        "Tu es un expert mondial de l'automobile, historien et ingénieur technique.\n"
        "Consignes de décision strictes :\n"
        "1. Pour l'histoire, les dates, les inventeurs, les fondateurs et le passé des marques, "
        "utilise impérativement l'outil 'archives_histoire_automobile'.\n"
        "2. Pour l'actualité en direct, les prix actuels du marché ou les modèles récents, "
        "utilise l'outil 'tavily_search_results_json'.\n"
        "3. Pour les salutations ou discussions générales, réponds directement sans outil.\n"
        "4. Sois clair, rigoureux, enthousiaste et réponds toujours en Français."
    )

    return create_agent(llm, tools, system_prompt=system_prompt)
import os
from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages

# Checks for the Gemini key you just saved in your .env
if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError("Missing API key in .env file.")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    code_generated: str
    iterations: int

# Instantiating the free Gemini engine
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.environ.get("OPENAI_API_KEY"), temperature=0)

def researcher_node(state: AgentState):
    print("\n[Node: Researcher] Simulating target documentation gathering...")
    user_prompt = state['messages'][0].content
    context_message = SystemMessage(content=f"Context: Optimized structure for processing: {user_prompt}")
    return {"messages": [context_message]}

def coder_node(state: AgentState):
    current_iteration = state.get('iterations', 0) + 1
    print(f"\n[Node: Coder] Generating script solution via Gemini (Attempt #{current_iteration})...")
    
    system_instruction = SystemMessage(
        content="You are an expert software developer. Generate clean, efficient Python code. "
                "Return ONLY clean python lines without markdown block styling formatting."
    )
    full_prompt = [system_instruction] + state['messages']
    response = llm.invoke(full_prompt)
    
    return {
        "messages": [response],
        "code_generated": response.content,
        "iterations": current_iteration
    }

def reviewer_routing_logic(state: AgentState):
    code = state.get('code_generated', '')
    iterations = state.get('iterations', 0)
    print("\n[Edge Router: Reviewer] Checking script syntax...")
    if "def " in code or "import " in code or iterations >= 2:
        print("-> Decision: Finalizing workflow loop.")
        return "end"
    return "loop_back"

builder = StateGraph(AgentState)
builder.add_node("Researcher", researcher_node)
builder.add_node("Coder", coder_node)
builder.set_entry_point("Researcher")
builder.add_edge("Researcher", "Coder")
builder.add_conditional_edges("Coder", reviewer_routing_logic, {"loop_back": "Coder", "end": END})
app = builder.compile()

if __name__ == "__main__":
    task_input = "Write a Python script using pandas to find rows where the 'Age' column is over 30."
    initial_inputs = {"messages": [HumanMessage(content=task_input)], "iterations": 0}
    print("=== Starting LangGraph Gemini Agent System App ===")
    for event in app.stream(initial_inputs):
        for node_name, state_snapshot in event.items():
            if 'code_generated' in state_snapshot:
                print("\n--- Output Code Preview ---")
                print(state_snapshot['code_generated'])
import asyncio
from langchain_core.messages import HumanMessage
from app.agents.graph import finance_agent


async def test_chat():
    print("🤖 FinAgent Started (LangGraph Mode)...")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit"]: break

        # LangGraph 接收的参数是 {"messages": [...]}
        inputs = {"messages": [HumanMessage(content=user_input)]}

        try:
            result = await finance_agent.ainvoke(inputs)

            final_msg = result["messages"][-1]
            print(f"AI: {final_msg.content}")

        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_chat())
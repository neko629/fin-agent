from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from app.agents.graph import finance_agent

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat 接口:
    1. 接受用户文本
    2. 调用 agent
    3. 返回结果
    """

    try:
        inputs = {
            "messages": [
                HumanMessage(content=request.message)
            ]
        }

        # 调用 agent
        result = await finance_agent.ainvoke(inputs)

        # 取最后一条 ai 回复
        final_message = result["messages"][-1]

        return ChatResponse(response=final_message.content)

    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))
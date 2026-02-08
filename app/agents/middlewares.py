from langchain.agents.middleware import PIIMiddleware


# 配置 PIIMiddleware, 用于检测和处理信用卡号敏感信息
pii_middleware = PIIMiddleware(
    "credit_card",
    detector = r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
    strategy = "mask",
    apply_to_input = True,
    apply_to_output = False
)

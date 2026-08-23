from config import Config


def analyze_with_ai(text, rule_result):
    if not Config.AI_ENABLED:
        return None

    if not Config.AI_API_KEY:
        print("AI_ENABLED is true but AI_API_KEY is missing.")
        return None

    try:
        return call_ai_model(text, rule_result)
    except Exception as error:
        print("AI analysis failed:", error)
        return None


def call_ai_model(text, rule_result):
    raise NotImplementedError("AI provider has not been configured.")

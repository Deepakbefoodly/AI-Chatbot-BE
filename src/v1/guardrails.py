import re

# Simplified placeholder guardrails

def is_valid_input(question: str) -> (bool, str):
    if len(question) > 500:
        return False, "Question too long"
    if re.search(r"(?:<script>|drop\s+table|select\s+\*|insert\s+into)", question, re.IGNORECASE):
        return False, "Potential injection detected"
    if re.search(r"(?:offensiveword1|offensiveword2)", question, re.IGNORECASE):
        return False, "Inappropriate content detected"
    return True, ""

def is_valid_output(response: str) -> (bool, str):
    if len(response) > 2000:
        return False, "Response too long"
    if re.search(r"(?:offensiveword1|offensiveword2|hallucination)", response, re.IGNORECASE):
        return False, "Potentially unsafe or hallucinated response"
    return True, ""

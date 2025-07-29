from fastapi import APIRouter, HTTPException

from v1.schemas import QuestionRequestGenAI, ResponseBody
import guardrails, rag_pipeline

router = APIRouter(prefix="/v1")

@router.post("/chat")
def stream(body: QuestionRequestGenAI) -> ResponseBody:
    question = body.question
    is_valid, reason = guardrails.is_valid_input(question)

    if not is_valid:
        raise HTTPException(status_code=400, detail=f"Invalid question: {reason}")

    try:
        response = rag_pipeline.run_rag_pipeline(body)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    is_valid_out, reason_out = guardrails.is_valid_output(response)

    if not is_valid_out:
        raise HTTPException(status_code=400, detail=f"Unsafe output: {reason_out}")

    return ResponseBody(answer=response)
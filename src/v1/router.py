from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from openai_utils.schemas import QuestionRequestGenAI
import guardrails, rag_pipeline

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/chat")
def stream(body: QuestionRequestGenAI):
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

    return StreamingResponse(response, media_type="text/event-stream")
# chatbot_view.py
from flask import Blueprint, render_template, request, jsonify
from ..models import db, ChatHistory
from datetime import datetime
from sqlalchemy import text
from ..llm_utils import generate_sql_from_query, summarize_result_to_natural_language, classify_containers
from ..llm_utils import extract_query_date, summarize_terminal_stats

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chatbox")
def chatbox():
    return render_template("chatbox.html")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data["message"]

    # ✅ 인사나 일반 대화인 경우: 조건 누적 없이 간단 응답 반환
    if user_msg.lower() in ["안녕", "안녕하세요", "하이", "hello", "hi"]:
        return jsonify({
            "response": "안녕하세요. 컨테이너 관련해서 궁금하신 내용을 자유롭게 질문해주세요!",
            "sql": None,
            "raw_result": []
        })

    # ✅ 사용자 질문에서 날짜 추출 (예: "6월 7일부터")
    query_date = extract_query_date(user_msg)

    # ✅ 맥락 프롬프트 구성
    context_prompt = f"사용자가 이렇게 물어요: {user_msg}\n- 기준 날짜: {query_date}"

    sql_query = generate_sql_from_query(user_msg)

    try:
        result = db.session.execute(text(sql_query)).fetchall()
        result_data = [dict(row._mapping) for row in result]
    except Exception as e:
        return jsonify({"response": f"SQL 실행 오류: {str(e)}", "sql": sql_query})

    normal_containers, one_way_containers = classify_containers(result_data)

    context_prompt += f"\n\n이번 조건에 해당하는 컨테이너 중:\n"
    context_prompt += f"- 일반 대여 가능(내항) 컨테이너: {len(normal_containers)}대\n"
    context_prompt += f"- 외항 원웨이 전용 컨테이너: {len(one_way_containers)}대\n"

    # ✅ 날짜 기반 필터링 context 추가
    context_prompt += summarize_terminal_stats(one_way_containers, query_date)

    response = summarize_result_to_natural_language(
        context=context_prompt,
        user_query=user_msg,
        result=result_data
    )

    chat_record = ChatHistory(
        user_id="anonymous",
        message=user_msg,
        response=response,
        timestamp=datetime.utcnow()
    )
    db.session.add(chat_record)
    db.session.commit()

    return jsonify({
        "response": response,
        "sql": sql_query,
        "raw_result": result_data
    })

def summarize_terminal_stats(containers, base_date=None):
    from datetime import datetime
    one_way_count = 0
    one_way_terminals = {}

    for c in containers:
        is_one_way = (
            (c.get("price") == 0)
            or ("원웨이" in (c.get("remarks") or ""))
            or (c.get("region") == "외항")
        )
        is_20ft = "20" in c.get("size", "")
        is_available = c.get("available_from") and (not base_date or c["available_from"] <= base_date)

        if is_one_way and is_20ft and is_available:
            terminal = c.get("terminal", "미확인")
            one_way_terminals[terminal] = one_way_terminals.get(terminal, 0) + 1
            one_way_count += 1

    if not one_way_terminals:
        return "\n\n 조건에 맞는 원웨이 20ft 컨테이너는 없습니다."

    terminal_summary = "\n\n 원웨이 20ft 컨테이너 수량 (반납 없음):\n"
    for terminal, count in sorted(one_way_terminals.items(), key=lambda x: -x[1]):
        terminal_summary += f"- {terminal}: {count}대\n"
    return terminal_summary
# chatbot_view.py
from flask import Blueprint, render_template, request, jsonify
from ..models import db, ChatHistory
from datetime import datetime

chatbot_bp = Blueprint('chatbot', __name__)

@chatbot_bp.route("/chatbox")
def chatbox():
    return render_template("chatbox.html")

@chatbot_bp.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data["message"]
    
    # TODO: RAG+LLM 연결
    response = f"이건 예시 응답이야: '{user_msg}'에 대한 대답!"

    chat_record = ChatHistory(
        user_id="anonymous",
        message=user_msg,
        response=response,
        timestamp=datetime.utcnow()
    )
    db.session.add(chat_record)
    db.session.commit()

    return jsonify({"response": response})

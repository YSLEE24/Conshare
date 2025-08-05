# llm_utils.py
import os, re
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from sqlalchemy import text
from datetime import datetime

# ✅ .env에서 API 키 로딩
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),  # .env에 저장
    temperature=0.2
)

def extract_query_date(user_query: str):
    """
    예: "6월 7일" → datetime.date(2025, 6, 7)
    """
    match = re.search(r"(\d{1,2})월\s*(\d{1,2})일", user_query)
    if match:
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime(2025, month, day).date()
    return datetime.utcnow().date()

def summarize_terminal_stats(containers, target_date):
    """
    - 20ft 원웨이 컨테이너 중 해당 날짜 이전에 사용 가능한 것 요약
    """
    filtered = [
        c for c in containers
        if "20" in c.get("size", "") and c.get("available_from") and c["available_from"] <= target_date
    ]
    terminal_count = {}
    for c in filtered:
        terminal = c.get("terminal", "미확인")
        terminal_count[terminal] = terminal_count.get(terminal, 0) + 1

    if not filtered:
        return "\n\n해당 날짜 기준 반납 없는 20ft 컨테이너는 없습니다.\n"

    lines = [f"\n\n해당 날짜 기준 반납 없는 20ft 컨테이너 수: {len(filtered)}대"]
    lines.append("- 터미널별 분포:")
    for terminal, count in terminal_count.items():
        lines.append(f"  * {terminal}: {count}대")
    return "\n".join(lines)


def parse_date_condition(user_query: str) -> dict:
    """
    사용자 문장에서 날짜를 파악하고,
    SQL 조건식과 의미를 추출해 리턴.
    """
    # 예시: "6월 7일부터", "6월 7일에", "6월 7일까지만"
    # → date: 2025-06-07

    # 💡 실제로는 NLP 모델이나 dateparser를 써서 처리해야 함
    if "부터" in user_query or "이후" in user_query:
        direction = "from"  # 시작일 조건
        comparator = ">="
    elif "까지" in user_query or "이전" in user_query:
        direction = "until"
        comparator = "<="
    else:
        direction = "on"  # 해당 날짜에 사용 가능해야 함
        comparator = "between"

    # # 날짜 파싱 (예시는 하드코딩)
    # parsed_date = "2025-06-07"  # 👉 실제로는 NLP/정규식으로 추출해야 함

    # # SQL 표현
    # if comparator == "between":
    #     sql = f"available_from <= '{parsed_date}' AND (available_to IS NULL OR available_to >= '{parsed_date}')"
    # else:
    #     sql = f"available_from {comparator} '{parsed_date}'"

    # return {
    #     "parsed_date": parsed_date,
    #     "sql_condition": sql,
    #     "logic_type": direction,
    #     "description": f"{parsed_date} {('이후' if comparator == '>=' else '이전')} 사용할 수 있는 컨테이너"
    # }

    # 날짜 파싱
    today = datetime.utcnow().date()

    # 반납 없는 20ft 컨테이너만 필터링 (날짜 포함)
    filtered = [
        c for c in one_way_containers 
        if "20" in c["size"] and c["available_from"].date() <= today
    ]

    # 터미널별 개수 정리
    terminal_count = {}
    for c in filtered:
        terminal = c["terminal"]
        terminal_count[terminal] = terminal_count.get(terminal, 0) + 1

    # context에 추가
    if filtered:
        context_prompt += "\n\n추가 정보:\n"
        context_prompt += f"- 현재 날짜 기준 반납 없는 20ft 컨테이너 수: {len(filtered)}대\n"
        context_prompt += "- 터미널별 분포:\n"
        for terminal, count in terminal_count.items():
            context_prompt += f"  * {terminal}: {count}대\n"
    else:
        context_prompt += "\n\n현재 날짜 기준, 반납 없는 20ft 컨테이너는 없습니다.\n"

def classify_containers(containers):
    """
    컨테이너 데이터를 일반 대여 가능(내항) / 외항 원웨이 전용으로 분류합니다.

    - price가 0이면 원웨이
    - region이 "외항"이면 원웨이
    - remarks에 "원웨이"가 포함되어 있으면 원웨이

    나머지는 모두 일반 대여 가능 컨테이너로 분류합니다.
    """
    normal = []
    one_way = []

    for row in containers:
        price = row.get("price", None)
        region = row.get("region", "")
        remarks = row.get("remarks", "")

        # 안전하게 조건 체크
        is_one_way = (
            (price == 0) or
            ("원웨이" in remarks) or
            (region == "외항")
        )

        if is_one_way:
            one_way.append(row)
        else:
            normal.append(row)

    return normal, one_way


def generate_sql_from_query(user_query: str) -> str:
    prompt = f"""
다음은 사용자 질문을 기반으로 SQL 쿼리를 생성하는 예시입니다.
스키마는 다음과 같습니다:

class Container(db.Model):
    __tablename__ = 'containers'
    id = db.Column(db.Integer, primary_key=True)
    container_number = db.Column(db.String(20), nullable=False)
    size = db.Column(db.String(10), nullable=False)
    tare = db.Column(db.Integer)
    terminal = db.Column(db.String(50))
    region = db.Column(db.String(20))
    type = db.Column(db.String(20))
    available_from = db.Column(db.Date)
    available_to = db.Column(db.Date)
    price = db.Column(db.Integer)

너는 SQL 전문가야. 아래 사용자 질문을 보고 적절한 SQL 쿼리문을 하나 생성해줘.

조건:
- SQL 쿼리만 출력해줘.
- 절대로 ```sql 또는 ``` 같은 마크다운 문법을 포함하지 마.
- 설명하지 마. 쿼리만 딱 한 줄 또는 여러 줄로 보여줘.
- 테이블 이름은 containers야.
- 모든 날짜는 2025년 기준이라 가정하고, 반드시 'YYYY-MM-DD' 형식의 문자열로 자동 변환했다고 가정해줘.
- size, region, 날짜는 문자열이므로 따옴표로 묶어줘.
- size 조건은 ILIKE '%20%' 형태로 비교해줘 (대소문자 구분하지 않게).
- region도 ILIKE '%부산%' 형태로 작성해줘.
- "반납하지 않아도 되는 컨테이너"는 available_to IS NULL 조건을 포함해야 한다. 예시 : SELECT * FROM containers WHERE available_to IS NULL;
- 반드시 PostgreSQL 문법을 따르고, 날짜 계산 시에는 available_to - DATE 'YYYY-MM-DD' 형식을 써. DATEDIFF, JULIANDAY, STR_TO_DATE 등은 쓰지 마.
- 사용자가 이전에 말한 조건이 있다면 그 조건이 현재 질문에 누적되어야 할지, 새로운 조건으로 대체되어야 할지를 먼저 판단하고 그에 맞춰 쿼리를 구성해줘.

질문:
{user_query}
"""
    raw = llm.invoke(prompt).content.strip()
    return raw.replace("```sql", "").replace("```", "").strip()


def summarize_result_to_natural_language(context: str, user_query: str, result: list) -> str:
    context_part = f"대화 맥락:\n{context}\n" if context else ""

    prompt = f"""
너는 SQL 분석 결과를 바탕으로 사용자에게 자연스럽고 정확한 요약을 제공하는 전문가야.

다음은 (대화 맥락이 있을 수도 있고 없을 수도 있는) 상황에서 사용자의 질문과 SQL 결과야.

{context_part}
사용자의 새 질문: {user_query}
SQL 결과: {result}

이 조건들을 바탕으로 사용자의 질문에 정확하게 응답해줘.

 조건 해석 원칙:
1. **질문이 이전 질문의 연장선**이라면, 기존 조건들을 그대로 유지하고 새 조건을 누적해 적용해.
   - 예: "6월 7일부터 부산항 20ft" → 이어서 "반납 안 해도 되는 건?"이면, ‘부산 + 20ft + 6월 7일’ 조건 유지 + ‘반납 없음’ 조건 추가.
2. **질문에 날짜/지역/사이즈 등이 명시적으로 바뀐 경우**에는 해당 항목만 새로 적용하고, 나머지 조건은 유지해.
   - 예: "그럼 인천은?" → 지역만 인천으로 교체. 나머지는 유지.
3. 명시적 변경 없이 단독 질문이라면, 이전 조건이 유지된 상태로 누적 해석해야 해.

 날짜 조건:
- 대여 가능 여부 판단 기준:
  available_from <= '날짜' AND (available_to IS NULL OR available_to >= '날짜')
- 사용자가 날짜를 다시 언급하지 않으면, 이전 조건의 날짜를 그대로 유지해.

 반납 없는 컨테이너 조건:
- 반납이 필요 없는 컨테이너는 일반적으로 available_to IS NULL 조건을 만족해.
- 가격이 0원이거나 '외항', '원웨이' 등의 표시가 있는 경우도 ‘가격 문의 필요’ 또는 ‘반납 없음’으로 간주 가능.
- 단, **이 조건은 반드시 다른 조건(날짜, 지역, 사이즈 등)과 함께 필터링해서 적용해야 해.**

 사이즈 조건:
- 사용자가 40ft를 찾으면 40HQ도 함께 포함해서 판단해야 해.

 응답 방식:
- 아래 항목들을 반드시 포함해서 자연어로 요약해줘:
- 조건에 없는 정보는 추측하지 마.
- 새로운 날짜로 질문하지 않는다면 조건을 쌓아서 기억했다가 조건에 근거해서 대답해줘.
- "SQL 결과"등과 같은 말은 생략해.
- 관련없는 질문을 할때는 컨테이너 예약 정보에 대해서만 답변할 수 있다고 해줘.
- 마지막엔 "더 궁금한 조건이 있다면 알려주세요" 식으로 마무리해줘.


"""
    return llm.invoke(prompt).content.strip()

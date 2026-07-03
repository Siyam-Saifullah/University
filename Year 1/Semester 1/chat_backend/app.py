from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from datetime import datetime

app = Flask(__name__)
CORS(app)

chat_history = []
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def generate_local_reply(user_message: str) -> str:
    lower = user_message.lower()
    topic = ""
    action = ""

    # Explicit commands
    if any(k in lower for k in ["start study", "let's study", "begin study", "study now"]):
        action = "start"
    elif any(k in lower for k in ["stop study", "end study", "break", "pause"]):
        action = "stop"
    elif any(k in lower for k in ["status", "progress", "how am i doing"]):
        action = "status"
    elif any(k in lower for k in ["reset", "restart", "clear progress"]):
        action = "reset"
    elif any(k in lower for k in ["help", "what can you do", "commands"]):
        action = "help"

    # 13 topics
    topic_keywords = {
        "ct": ["ct", "class test", "continuous assessment"],
        "mid": ["mid", "sessional exam", "midterm"],
        "final": ["final", "final exam", "semester exam"],
        "mse1111": ["introduction to mse", "mse1111", "intro mse"],
        "mse1121": ["crystallography", "mse1121"],
        "mse1122": ["crystallography sessional", "mse1122"],
        "math1111": ["matrices", "vector analysis", "geometry", "math1111", "mathematics"],
        "phy1111": ["electricity and magnetism", "phy1111"],
        "phy1112": ["electricity sessional", "magnetism sessional", "phy1112"],
        "chem1111": ["organic chemistry", "chem1111"],
        "chem1112": ["organic chemistry sessional", "chem1112"],
        "eng1111": ["technical english", "eng1111", "english"],
        "mse1112": ["engineering drawing", "mse1112", "drawing"],
    }

    for key, kws in topic_keywords.items():
        if any(k in lower for k in kws):
            topic = key
            break

    # Topic recommendations
    topic_recommendations = {
        "ct": {
            "title": "Class Test Strategy",
            "subtitle": "30% of theory course marks",
            "bullet_points": [
                "Attend every class — attendance directly boosts CT/quiz marks",
                "Solve at least 10 problems per topic from tutorials and past CTs",
                "Revise within 24 hours after each lecture",
                " Aim for full marks in CT; they are the easiest way to protect your GPA"
            ],
            "problem_questions": [
                "What topics are covered in upcoming CTs?",
                "Show me a 3-day CT prep schedule",
                "List common CT question patterns"
            ],
            "motivation": "CTs are easy marks. Do not skip them.",
            "study_plan": "Day 1: list topics. Day 2: solve 10 problems. Day 3: revise formulas and write a mini-test."
        },
        "mid": {
            "title": "Mid/Sessional Exam Strategy",
            "subtitle": "20% of theory course marks",
            "bullet_points": [
                " revise CT notes first before starting mid prep",
                "Solve previous year mid questions topic-wise",
                "Focus on derivations, definitions, and numerical methods",
                "Keep a 1-page formula sheet per subject"
            ],
            "problem_questions": [
                "Create a 1-week mid exam timetable",
                "List the most repeated mid questions",
                "Show me how to make a 1-page formula sheet"
            ],
            "motivation": "Mids are about consistency, not cramming.",
            "study_plan": "Week 1: syllabus mapping and past papers. Week 2: problem solving and full revision."
        },
        "final": {
            "title": "Final Exam Strategy",
            "subtitle": "50% of theory course marks",
            "bullet_points": [
                "Start at least 4 weeks before the exam",
                "Solve full past papers under timed conditions",
                "Prepare model answers for long questions",
                "Group weak topics into 2-day sprints"
            ],
            "problem_questions": [
                "Draft a 30-day final-exam study plan",
                "Rank subjects by difficulty and suggest order",
                "Suggest a daily target for each subject"
            ],
            "motivation": "Final exams decide your semester. Treat them like a project with milestones.",
            "study_plan": "4 weeks out: syllabus scan. 3 weeks: chapter-wise questions. 2 weeks: past papers. 1 week: mock tests and revision."
        },
        "mse1111": {
            "title": "Introduction to MSE",
            "subtitle": "MSE1111",
            "bullet_points": [
                "Focus on bonding, crystal structures, and defects",
                "Use Callister chapters 1–3 as base material",
                "Draw crystal structures repeatedly until automatic",
                "Link textbook examples to real engineering materials"
            ],
            "problem_questions": [
                "Which chapter is most important from past exams?",
                "Give me a 2-week plan for MSE1111",
                "Summarize bonding types with examples"
            ],
            "motivation": "Intro MSE builds your entire foundation. Master it now.",
            "study_plan": "Week 1: bonding and structure. Week 2: defects and properties. Solve 15 problems per chapter."
        },
        "mse1121": {
            "title": "Crystallography I",
            "subtitle": "MSE1121",
            "bullet_points": [
                "Miller indices and stereographic projection are high-yield",
                "Practice symmetry operations and point groups daily",
                "Use worked examples from the textbook and lecture notes",
                "Draw projections by hand until they become fast"
            ],
            "problem_questions": [
                "Explain Miller indices step-by-step",
                "List symmetry operations for cubic system",
                "Give me a 1-week plan for Crystallography"
            ],
            "motivation": "Crystallography is visual — practice drawing more than reading.",
            "study_plan": "Days 1-2: Miller indices. Days 3-4: symmetry. Days 5-7: stereographic problems."
        },
        "mse1122": {
            "title": "Crystallography I Sessional",
            "subtitle": "MSE1122",
            "bullet_points": [
                "Lab reports are graded for clarity, not just answers",
                "Prepare standard observation formats in advance",
                "Focus on microscope operation and specimen preparation",
                "Link lab observations with lecture theory"
            ],
            "problem_questions": [
                "Show a sample lab report format",
                "List common viva questions for this lab",
                "Give me a pre-lab checklist"
            ],
            "motivation": "Sessional labs are 70% practical. Attendance and preparation matter most.",
            "study_plan": "Before each lab: read theory. After each lab: write report same day. Weekly: review microscope techniques."
        },
        "math1111": {
            "title": "Matrices, Vector Analysis and Geometry",
            "subtitle": "MATH1111",
            "bullet_points": [
                "Matrix algebra and eigenvalues are heavily tested",
                "Vector calculus is useful for physics and mechanics links",
                "Practice problem solving every day without gaps",
                "Create a formula notebook and revise it weekly"
            ],
            "problem_questions": [
                "List the most important matrix methods",
                "Show me a 3-week MATH1111 study timetable",
                "Summarize vector operators with examples"
            ],
            "motivation": "Math supports physics and future MSE courses. Weak math will slow you down later.",
            "study_plan": "Week 1: matrices and determinants. Week 2: vectors. Week 3: geometry. Solve 12 problems per day."
        },
        "phy1111": {
            "title": "Electricity and Magnetism",
            "subtitle": "PHY1111",
            "bullet_points": [
                "Maxwell equations are conceptually important",
                "Practice circuit problems and field calculations",
                "Link EM concepts to MSE applications like sensors and devices",
                "Draw diagrams for every problem before solving"
            ],
            "problem_questions": [
                "Summarize Coulomb and Gauss laws with examples",
                "Give me a 2-week plan for EM",
                "List common final exam question types"
            ],
            "motivation": "EM is problem-heavy. Speed comes from pattern recognition.",
            "study_plan": "Week 1: electrostatics. Week 2: magnetism. Week 3: Maxwell and circuits. Solve 15 problems daily."
        },
        "phy1112": {
            "title": "Electricity and Magnetism Sessional",
            "subtitle": "PHY1112",
            "bullet_points": [
                "Circuit building and measurement accuracy are graded",
                "Know the lab instruments inside out before viva",
                "Keep calculations neat and show error analysis",
                "Write observations during the experiment, not after"
            ],
            "problem_questions": [
                "List common instrument viva questions",
                "Show error calculation steps",
                "Give me a pre-lab checklist"
            ],
            "motivation": "Practical exams test skill, not memorization. Practice builds confidence.",
            "study_plan": "Before lab: read theory and instrument manual. During lab: note readings. After lab: analyze immediately."
        },
        "chem1111": {
            "title": "Organic Chemistry",
            "subtitle": "CHEM1111",
            "bullet_points": [
                "Reaction mechanisms and nomenclature are high priority",
                "Make reaction flashcards and review them daily",
                "Use functional group patterns to reduce memorization",
                "Link organic chemistry to polymers in MSE later"
            ],
            "problem_questions": [
                "List essential reactions for final exam",
                "Summarize aromatic substitution mechanisms",
                "Give me a 2-week study plan"
            ],
            "motivation": "Organic chemistry rewards repetition. Small daily reviews beat cramming.",
            "study_plan": "Week 1: basic mechanisms. Week 2: functional groups. Week 3: named reactions and problem sets."
        },
        "chem1112": {
            "title": "Organic Chemistry Sessional",
            "subtitle": "CHEM1112",
            "bullet_points": [
                "Titration precision and purity checks matter most",
                "Write clear step-by-step procedures in reports",
                "Review common reagent properties before viva",
                "Connect lab techniques to industrial chemistry applications"
            ],
            "problem_questions": [
                "List common titration viva questions",
                "Show titration calculation steps",
                "Give me a pre-lab checklist"
            ],
            "motivation": "Accuracy and documentation decide sessional grades.",
            "study_plan": "Before lab: review theory. During lab: follow standard procedure. After lab: calculate and write report same day."
        },
        "eng1111": {
            "title": "Technical English",
            "subtitle": "ENG1111",
            "bullet_points": [
                "Write reports in formal technical style",
                "Practice summarizing graphs and procedures",
                "Build academic vocabulary from your course readings",
                "Keep writing templates for common task types"
            ],
            "problem_questions": [
                "Give me a report writing template",
                "List common technical English topics",
                "Show me how to summarize a graph in 3 sentences"
            ],
            "motivation": "Clear communication improves grades in every subject.",
            "study_plan": "Week 1: vocabulary. Week 2: paragraphs. Week 3: reports. Write 2 short pieces each week."
        },
        "mse1112": {
            "title": "Engineering Drawing",
            "subtitle": "MSE1112",
            "bullet_points": [
                "Practice orthographic projections daily with pencil first",
                "Learn standard dimensioning and tolerancing rules",
                "Use CAD practice only after hand-drawing is fast",
                "Compare your drawings with textbook solutions"
            ],
            "problem_questions": [
                "List common drawing exam questions",
                "Give me a CAD practice plan",
                "Show dimensioning rules summary"
            ],
            "motivation": "Drawing speed comes from repetition. Draw every day.",
            "study_plan": "Daily: 30 minutes hand drawing. Weekly: one full sheet practice. Check against standard layouts."
        }
    }

    if action == "start":
        return (
            "Let's begin your focused study block now.\n"
            "1. Pick one topic.\n"
            "2. Set a 25-minute timer.\n"
            "3. Work without phone.\n"
            "4. After the timer, take a 5-minute break.\n"
            "After 4 blocks, take a long 20-minute break.\n"
            "Reply STOP when you want to end."
        )
    if action == "stop":
        return "Study block paused. Short break. Stretch, drink water, then reply START when you're ready."
    if action == "status":
        return (
            "You are building momentum. Keep a simple log: subject, minutes studied, and one win from the session."
        )
    if action == "reset":
        return "Progress reset. No problem. Pick one small topic and complete it now."
    if action == "help":
        return (
            "You can ask about CT, mid, final, or any course code: MSE1111, MSE1121, MSE1122, MATH1111, PHY1111, PHY1112, CHEM1111, CHEM1112, ENG1111, MSE1112.\n"
            "Commands: START, STOP, STATUS, RESET, HELP."
        )

    selected = topic_recommendations.get(topic)

    if selected:
        lines = [f"{selected['title']} ({selected['subtitle']})", selected["motivation"], "", "Action steps:"]
        for i, b in enumerate(selected["bullet_points"], 1):
            lines.append(f"{i}. {b}")
        lines += ["", "Quick study plan:", selected["study_plan"], "", "Try one of these to continue:"]
        for i, q in enumerate(selected["problem_questions"], 1):
            lines.append(f"{i}. {q}")
        return "\n".join(lines)

    # fallback for unknown topics
    return (
        "This is a very broad question.\n"
        "Pick one course topic first, or choose a target like CT, mid, or final.\n"
        "You can also type HELP."
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    payload = request.get_json() or {}
    user_message = (payload.get("message") or "").strip()
    if not user_message:
        return jsonify({"error": "message is required"}), 400

    chat_history.append({"role": "user", "content": user_message, "ts": datetime.utcnow().isoformat()})
    reply = generate_local_reply(user_message)
    chat_history.append({"role": "assistant", "content": reply, "ts": datetime.utcnow().isoformat()})
    return jsonify({"reply": reply, "history": chat_history[-20:]})


@app.route("/api/history", methods=["GET"])
def history():
    return jsonify({"history": chat_history[-50:]})


@app.route("/api/history", methods=["DELETE"])
def clear_history():
    chat_history.clear()
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), debug=True)

import sys
import os
import json
import streamlit as st

# Handle paths for .exe and script
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(__file__)

json_path = os.path.join(base_path, "questions.json")

# Load questions
with open(json_path, "r") as f:
    questions = json.load(f)

st.title("MCQ Test App 📝")

# Store answers and submission state
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "submitted" not in st.session_state:
    st.session_state.submitted = False

# Show questions (if not submitted yet)
if not st.session_state.submitted:
    for i, q in enumerate(questions):
        st.write(f"**Q{i+1}: {q['question']}**")
        st.session_state.answers[i] = st.radio(
    "Choose an option:",
    q["options"],
    index=None,   # 👈 ensures nothing is pre-selected
    key=f"q{i}"
)


    # Submit button
if st.button("Submit Test"):
    # Check for unanswered questions
    unanswered = [i+1 for i in range(len(questions)) if st.session_state.answers.get(i) is None]
    
    if unanswered:
        st.warning(f"⚠️ Please answer all questions before submitting. Unanswered: Q{', Q'.join(map(str, unanswered))}")
    else:
        st.session_state.submitted = True
        st.rerun()


# Show results after submission
else:
    score = 0
    st.subheader("📊 Results:")
    for i, q in enumerate(questions):
        user_answer = st.session_state.answers[i]
        if user_answer == q["answer"]:
            st.success(f"Q{i+1}: Correct ✅ ({user_answer})")
            score += 1
        else:
            st.error(f"Q{i+1}: Wrong ❌ (Your answer: {user_answer}, Correct: {q['answer']})")

    total = len(questions)
    st.write(f"### Final Score: {score} / {total}")

    # Pass/Fail message (threshold = 50%)
    if score >= total / 2:
        st.balloons()
        st.success("🎉 Congratulations! You Passed ✅")
    else:
        st.error("❌ You Failed. Try Again!")

    # Restart button
    if st.button("Restart Test 🔄"):
        st.session_state.answers = {}
        st.session_state.submitted = False
        st.rerun()

# --- Signature at bottom ---
st.markdown("---")
st.markdown(
    "<h4 style='text-align: center; color: grey;'>Created by: S. Mamoon</h4>",
    unsafe_allow_html=True
)
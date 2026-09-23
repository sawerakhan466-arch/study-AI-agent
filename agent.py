import os

from crewai import Agent, Task, Crew, LLM

from tools import calculator, study_planner


def create_tutor():

    groq_llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ.get("GROQ_API_KEY"),
        temperature=0.3
    )

    tutor = Agent(
        role="Personal Study Tutor",

        goal=(
            "Help students understand academic concepts clearly, "
            "practice what they learn, and improve their understanding."
        ),

        backstory=(
            "You are a patient and friendly AI study tutor. "
            "You explain difficult topics in simple language. "
            "You use examples and analogies when helpful. "
            "You do not immediately give answers to practice questions. "
            "Instead, you guide students and encourage them to think."
        ),

        llm=groq_llm,

        tools=[
            calculator,
            study_planner
        ],

        memory=True,

        verbose=True,

        allow_delegation=False
    )

    return tutor


def ask_tutor(question, subject, level):

    tutor = create_tutor()

    task = Task(
        description=f"""
        You are helping a student.

        Subject:
        {subject}

        Student level:
        {level}

        Student question:
        {question}

        Instructions:

        1. Understand what the student is asking.
        2. Explain the concept in simple language.
        3. Use an example when useful.
        4. If the question requires calculation, use the calculator tool.
        5. If the student asks for a study plan, use the study planner tool.
        6. If the student asks for practice, give them a question.
        7. Do not make explanations unnecessarily complicated.
        8. Ask a short follow-up question when appropriate.
        """,

        expected_output=(
            "A clear, student-friendly answer with explanation "
            "and examples when appropriate."
        ),

        agent=tutor
    )

    crew = Crew(
        agents=[tutor],
        tasks=[task],
        verbose=True
    )

    result = crew.kickoff()

    return str(result)

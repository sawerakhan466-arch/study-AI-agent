from crewai.tools import tool


@tool("calculator")
def calculator(expression: str) -> str:
    """
    Calculate a simple mathematical expression.
    Example: 25 * 4
    """

    try:
        # Only allow basic mathematical characters
        allowed = "0123456789+-*/(). "

        if not all(char in allowed for char in expression):
            return "Please provide a simple mathematical expression."

        result = eval(expression, {"__builtins__": {}}, {})

        return f"The answer is {result}"

    except Exception:
        return "I could not calculate that expression."


@tool("study_planner")
def study_planner(topic: str, days: int) -> str:
    """
    Create a simple study plan for a topic.
    """

    if days <= 0:
        return "Number of days must be greater than 0."

    plan = []

    for day in range(1, days + 1):

        if day == 1:
            activity = "Learn the basic concepts"
        elif day == 2:
            activity = "Study examples and important points"
        elif day == 3:
            activity = "Practice questions"
        else:
            activity = "Review and test your understanding"

        plan.append(f"Day {day}: {activity}")

    return f"Study plan for {topic}:\n" + "\n".join(plan)

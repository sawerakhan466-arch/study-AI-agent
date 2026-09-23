def build_context(history):

    if not history:
        return "No previous conversation."

    context = []

    for message in history[-6:]:

        role = message["role"]
        content = message["content"]

        context.append(
            f"{role}: {content}"
        )

    return "\n".join(context)

BLOCKED = [

"ignore previous instructions",

"ignore all previous instructions",

"forget your prompt",

"show prompt",

"developer message",

"system prompt",

"jailbreak",

"act as",

"pretend",

"disable safety",

"bypass"

]


def detect_prompt_injection(text):

    text=text.lower()

    for word in BLOCKED:

        if word in text:

            return True

    return False

"""
Quiz question bank for cybersecurity awareness training.
All questions are educational — answers validated server-side.
"""

QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "You receive a Telegram message claiming you won a luxury car. What should you do first?",
        "options": [
            "Click the link and enter your details to claim the prize",
            "Verify the sender and never trust unbelievable prizes",
            "Forward the message to friends so they can win too",
            "Reply with your phone number immediately",
        ],
        "correct": 1,
        "explanation": "Unbelievable prizes are a classic scam tactic. Always verify sources and never trust unsolicited win notifications.",
    },
    {
        "id": 2,
        "question": "What does HTTPS in a website URL primarily indicate?",
        "options": [
            "The website is definitely legitimate and safe",
            "Encrypted connection between your browser and the server",
            "The website cannot be a phishing site",
            "Your payment card is automatically protected",
        ],
        "correct": 1,
        "explanation": "HTTPS encrypts data in transit, but scammers can also obtain HTTPS certificates. Always verify the domain name carefully.",
    },
    {
        "id": 3,
        "question": "A website asks for your SMS verification code to 'confirm your prize.' What do you do?",
        "options": [
            "Enter the code — they need it to verify you",
            "Never share SMS codes — this is OTP theft",
            "Share only the last 3 digits",
            "Ask them to send a new code first",
        ],
        "correct": 1,
        "explanation": "SMS verification codes are for YOUR authentication only. Sharing them lets criminals access your accounts.",
    },
    {
        "id": 4,
        "question": "Which is a common sign of a phishing website?",
        "options": [
            "Professional design and branding",
            "Urgency messages like 'Claim in 5 minutes or lose prize!'",
            "Clear contact information",
            "Proper spelling and grammar",
        ],
        "correct": 1,
        "explanation": "Scammers create urgency to bypass your critical thinking. Legitimate organizations rarely pressure immediate action.",
    },
    {
        "id": 5,
        "question": "What is social engineering in cybersecurity?",
        "options": [
            "Building secure software systems",
            "Manipulating people into revealing information or taking unsafe actions",
            "Encrypting social media messages",
            "Engineering social network algorithms",
        ],
        "correct": 1,
        "explanation": "Social engineering exploits human psychology — trust, fear, greed, and urgency — rather than technical vulnerabilities.",
    },
    {
        "id": 6,
        "question": "You scan a QR code from a poster offering free prizes. What risk does this pose?",
        "options": [
            "No risk — QR codes are always safe",
            "QR codes can redirect to malicious phishing websites",
            "QR codes only open legitimate apps",
            "QR codes cannot steal information",
        ],
        "correct": 1,
        "explanation": "QR-code attacks (quishing) hide malicious URLs. Always preview the destination before proceeding.",
    },
    {
        "id": 7,
        "question": "A countdown timer on a lottery website pressures you to act fast. This is an example of:",
        "options": [
            "Good user experience design",
            "Urgency tactic used in scams",
            "Legal requirement for online lotteries",
            "Standard e-commerce practice",
        ],
        "correct": 1,
        "explanation": "Artificial urgency prevents you from researching the site or consulting others — a hallmark of fraud.",
    },
    {
        "id": 8,
        "question": "Which information should you NEVER enter on an unknown website?",
        "options": [
            "Your favorite color",
            "Payment card number, CVV, and SMS verification codes",
            "A made-up username for a game",
            "Your city name",
        ],
        "correct": 1,
        "explanation": "Financial credentials and OTP codes on untrusted sites lead directly to card fraud and account takeover.",
    },
    {
        "id": 9,
        "question": "How can you verify if a website address is suspicious?",
        "options": [
            "Check if it has many images",
            "Look for misspellings, unusual domains, or extra subdomains",
            "See if the page loads quickly",
            "Count the number of buttons on the page",
        ],
        "correct": 1,
        "explanation": "Phishing domains often mimic real sites with subtle changes like 'paypa1.com' instead of 'paypal.com'.",
    },
    {
        "id": 10,
        "question": "What is the safest action after recognizing a phishing attempt?",
        "options": [
            "Enter fake information to trick the scammers",
            "Close the page, do not interact, and report it",
            "Complete the form to see what happens",
            "Share it on social media without context",
        ],
        "correct": 1,
        "explanation": "Do not engage with phishing sites. Close immediately, report to relevant authorities, and warn others responsibly.",
    },
]


def get_questions_for_client():
    """Return questions without correct answers for the client."""
    return [
        {
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
        }
        for q in QUIZ_QUESTIONS
    ]


def grade_quiz(answers: dict) -> tuple:
    """Grade quiz answers and return score with explanations."""
    results = []
    score = 0
    for q in QUIZ_QUESTIONS:
        qid = str(q["id"])
        selected = answers.get(qid)
        correct = q["correct"]
        is_correct = selected == correct
        if is_correct:
            score += 1
        results.append(
            {
                "question_id": q["id"],
                "question": q["question"],
                "your_answer": q["options"][selected] if selected is not None and 0 <= selected < len(q["options"]) else "No answer",
                "correct_answer": q["options"][correct],
                "is_correct": is_correct,
                "explanation": q["explanation"],
            }
        )
    return score, len(QUIZ_QUESTIONS), results

def generate_reply(customer_email, knowledge_context):
    """
    Temporary mock LLM for development.
    """

    return f"""
Hi,

Thank you for contacting our support team.

We received your request regarding:

"{customer_email}"

Based on our company knowledge:

{knowledge_context}

Our support team will be happy to assist you further.

Best regards,
Customer Support Team
"""
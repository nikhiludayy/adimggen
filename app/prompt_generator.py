# app/prompt_generator.py

def create_ad_prompt(product: str, audience: str) -> str:
    return (
        f"Create a high-quality digital advertisement image. "
        f"Product: '{product}'. Target audience: '{audience}'. "
        f"Use modern and engaging visuals suitable for Instagram/Facebook ads."
    )

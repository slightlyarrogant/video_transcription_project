from openai import OpenAI
from anthropic import Anthropic
import os
from dotenv import load_dotenv, find_dotenv

openai_client = None
anthropic_client = None

def init_clients():
    global openai_client, anthropic_client
    dotenv_path = find_dotenv(usecwd=True)
    if dotenv_path:
        print(f"Training Material: Found .env file at: {dotenv_path}")
        load_dotenv(dotenv_path, override=True)
    else:
        print("Training Material: No .env file found!")

    openai_api_key = os.getenv("OPENAI_API_KEY", "Not found")
    anthropic_api_key = os.getenv("ANTHROPIC_API_KEY", "Not found")
    
    print(f"Training Material: Using OpenAI API key (first 5 chars): {openai_api_key[:5]}...")
    print(f"Training Material: Using Anthropic API key (first 5 chars): {anthropic_api_key[:5]}...")
    
    openai_client = OpenAI(api_key=openai_api_key)
    anthropic_client = Anthropic(api_key=anthropic_api_key)

def generate_section(prompt, model, max_tokens, language):
    full_prompt = f"Generuj odpowiedź w języku polskim. {prompt}"
    system_message = f"Jesteś ekspertem w tworzeniu kompleksowych materiałów szkoleniowych w języku {language}."
    
    if model.startswith("gpt"):
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": full_prompt}
        ]
        response = openai_client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    elif model.startswith("claude"):
        response = anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_message,
            messages=[
                {"role": "user", "content": full_prompt}
            ]
        )
        return response.content[0].text
    
    else:
        raise ValueError(f"Unsupported model: {model}")
def generate_training_material(transcript, config, title=None):
    if openai_client is None or anthropic_client is None:
        init_clients()

    model = config['training_material']['model']
    max_tokens = config['training_material']['max_tokens']
    language = config['training_material']['language']

    sections = [
        ("Wprowadzenie", config['training_material']['prompts']['introduction']),
        ("Podsumowanie menedżerskie", config['training_material']['prompts']['executive_summary']),
        ("Kluczowe koncepcje i szczegółowe wyjaśnienia", config['training_material']['prompts']['key_concepts']),
        ("Praktyczne zastosowania", config['training_material']['prompts']['practical_applications']),
        ("Studia przypadków lub przykłady", config['training_material']['prompts']['case_studies']),
        ("Pytania kontrolne", config['training_material']['prompts']['review_questions']),
        ("Ćwiczenia praktyczne", config['training_material']['prompts']['practical_exercises']),
        ("Dalsza lektura", config['training_material']['prompts']['further_reading']),
        ("Zakończenie", config['training_material']['prompts']['conclusion'])
    ]

    generated_sections = {}
    for section_title, prompt in sections:
        section_content = generate_section(prompt.format(transcript=transcript, title=title), model, max_tokens, language)
        generated_sections[section_title] = section_content

    # Combine sections
    combined_material = "\n\n".join([f"# {section_title}\n\n{content}" for section_title, content in generated_sections.items()])

    # Final pass for coherence and completeness
    final_prompt = config['training_material']['prompts']['final_pass'].format(material=combined_material, title=title)
    final_material = generate_section(final_prompt, model, max_tokens * 3, language)

    return final_material

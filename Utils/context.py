# Utils/context.py
import config
import json, os, logging

def load_context():
    """Load context keywords from JSON file, return empty dict on failure."""
    try:
        with open(config.resource_path(os.path.join(config.data_dir, 'context.json'))) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading context.json: {e}")
        return {}

def detect_context(user_input, prompts_dict, context_keywords, current_prompt=None, is_new_conversation=False):
    """Score prompts based on keyword matches in user input."""
    scores = {name: 0 for name in prompts_dict}
    user_input = user_input.lower()

    # Count keyword matches for each prompt
    for prompt_name, keywords in context_keywords.items():
        for keyword in keywords:
            if keyword in user_input:
                scores[prompt_name] += 1
                logging.info(f"Added 1 point to {prompt_name} for keyword '{keyword}'")

    # Log non-zero scores for debugging
    non_zero_scores = [f"{name}: {score}" for name, score in scores.items() if score > 0]
    if non_zero_scores:
        logging.info("Current points: " + ", ".join(non_zero_scores))

    # Set threshold based on conversation state
    threshold = 1 if is_new_conversation else 2
    max_score = max(scores.values())

    # Return top-scoring prompt if threshold met
    if max_score >= threshold:
        top_prompts = [name for name, score in scores.items() if score == max_score]
        if len(top_prompts) > 1:
            logging.info(f"Tie detected: {', '.join(top_prompts)} with score {max_score}")
            # Prefer current prompt if tied, else non-Assistant prompt, else first
            best_prompt = current_prompt if current_prompt in top_prompts else next(
                (p for p in top_prompts if p != "Assistant"), top_prompts[0])
        else:
            best_prompt = top_prompts[0]
        return best_prompt, prompts_dict[best_prompt]

    return None, None

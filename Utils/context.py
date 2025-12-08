# Utils/context.py
import logging

def detect_context(globals, user_text):
    """
    Score prompts based on keyword matches in user input.
    
    Parameters:
        globals: Global variables containing all_prompts and all_context
        user_text: The user's input text
    """
    prompts_dict = globals.all_prompts
    context_keywords = globals.all_context
    
    scores = {name: 0 for name in prompts_dict}
    user_text = user_text.lower()

    # Count keyword matches for each prompt
    for prompt_name, keywords in context_keywords.items():
        if prompt_name not in scores:
            continue  # Skip if not in prompts
        for keyword in keywords:
            if keyword.lower() in user_text:
                scores[prompt_name] += 1
                logging.debug(f"Added 1 point to {prompt_name} for keyword '{keyword}'")

    # Log non-zero scores for debugging
    non_zero_scores = [f"{name}: {score}" for name, score in scores.items() if score > 0]
    if non_zero_scores:
        logging.debug("Current points: " + ", ".join(non_zero_scores))

    # Simplify: fixed threshold
    threshold = 1
    max_score = max(scores.values()) if scores else 0

    # Return top-scoring prompt if threshold met
    if max_score >= threshold:
        top_prompts = [name for name, score in scores.items() if score == max_score]
        if len(top_prompts) > 1:
            logging.info(f"Tie detected: {', '.join(top_prompts)} with score {max_score}")
            # Simplify: just pick the first in tie
            best_prompt = top_prompts[0]
        else:
            best_prompt = top_prompts[0]
        
        logging.info(f"Detected context: {best_prompt}")
        return best_prompt, prompts_dict.get(best_prompt, {})
    
    logging.info("No context detected.")
    return None, None
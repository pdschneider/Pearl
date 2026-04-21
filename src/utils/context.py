# Utils/context.py
import logging
from src.connections.ollama import context_query, get_all_models
from src.utils.toast import show_toast


def detect_context(globals, user_text):
    """
    Score prompts based on keyword matches in user input.

    Parameters:
        globals: Global variables containing all_prompts and all_context
        user_text: The user's input text
    
    Variables:
        user_text: Text sent via the input box
        (turned into a list of strings separated by spaces)
    """
    prompts_dict = globals.all_prompts
    context_keywords = globals.all_context

    # Exit early if no message was sent
    if not user_text:
        return

    scores = {name: 0 for name in prompts_dict}

    # Separate words into a list for processing
    user_text = user_text.lower().split()

    # Count keyword matches for each prompt
    for prompt_name, keywords in context_keywords.items():
        if prompt_name not in scores:
            continue  # Skip if not in prompts
        for keyword in keywords:
            if keyword.lower() in user_text:
                scores[prompt_name] += 1
                logging.debug(
                    f"Added 1 point to {prompt_name} for keyword '{keyword}'")

    # Log non-zero scores for debugging
    non_zero_scores = [f"{name}: {score}" for name, score in scores.items()
                       if score > 0]
    if non_zero_scores:
        logging.debug("Current points: " + ", ".join(non_zero_scores))

    # Simplify: fixed threshold
    threshold = 1
    max_score = max(scores.values()) if scores else 0

    # Return top-scoring prompt if threshold met
    if max_score >= threshold:
        top_prompts = [name for name, score in scores.items()
                       if score == max_score]
        if len(top_prompts) > 1:
            logging.info(
                f"Tie detected: {', '.join(top_prompts)} with score {max_score}")
            # Simplify: just pick the first in tie
            best_prompt = top_prompts[0]
        else:
            best_prompt = top_prompts[0]
        logging.debug(f"Detected context: {best_prompt}")

        # Get models list, return if empty
        all_models = get_all_models(globals, endpoint=globals.ollama_chat_path)
        if not all_models:
            logging.warning(f"No models detected. Exiting context query...")
            return

        # Ensure the model being used is present
        if not globals.context_model or globals.context_model not in all_models:
            if "llama3.2:latest" in all_models:
                globals.context_model = "llama3.2:latest"
                logging.warning(f"Context model not found in models list. Defaulting to llama3.2:latest...")
            else:
                globals.context_model = all_models[0]
                logging.warning(f"Context model not found in models list. Defaulting to {all_models[0]}...")

        # Set prompt to highest scoring for now, then query context model for long-term change
        logging.info(f"Switching to {best_prompt} for next message!")
        with globals.prompt_lock:
            globals.active_prompt = best_prompt
            globals.system_prompt = globals.all_prompts[f"{globals.active_prompt}"]["prompt"]

        # Query context model
        try:
            logging.debug(f"Querying context model...")
            context_response = context_query(globals, model=globals.context_model, message=user_text)
            if context_response:
                llm_prompt = str(context_response).strip().lower()
                best_prompt = str(best_prompt).strip().lower()
                logging.debug(f"Context model's response: {llm_prompt}")

                # If context models response aligns with the determined prompt
                if llm_prompt.startswith(best_prompt):
                    with globals.prompt_lock:
                        globals.active_prompt = best_prompt
                        globals.system_prompt = globals.all_prompts[f"{globals.active_prompt}"]["prompt"]
                    logging.info(f"Context switched to {best_prompt}")
                else:
                    logging.debug(f"Model choice and keywords not aligned: {best_prompt} vs {context_response}")
                    logging.info(f"Switching back to Assistant prompt...")
                    with globals.prompt_lock:
                        globals.active_prompt = "Assistant"
                        globals.system_prompt = globals.all_prompts[f"{globals.active_prompt}"]["prompt"]
        
        # Show error on exception
        except Exception as e:
            logging.error(f"Unable to query context model or switch prompt due to: {e}")
            show_toast(globals,
                       message="Unable to reach context model - is Ollama up on that network?",
                       _type="error")
            with globals.prompt_lock:
                globals.active_prompt = "Assistant"
                globals.system_prompt = globals.all_prompts[f"{globals.active_prompt}"]["prompt"]

        return best_prompt, prompts_dict.get(best_prompt, {})

    logging.debug("No context detected.")
    return None, None

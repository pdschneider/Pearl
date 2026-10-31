# src/utils/tts_scrub.py
import re


# Emoji & symbol ranges (pictographs, dingbats, regional flags, etc.)
_EMOJI = re.compile(
    "["
    "\U0001F000-\U0001FAFF"   # emoji, symbols, pictographs
    "\U00002600-\U000027BF"   # misc symbols & dingbats (☀ ✅ ☕)
    "\U00002B00-\U00002BFF"   # arrows & stars (⭐ ➤)
    "\U0001F1E6-\U0001F1FF"   # regional indicators (flags)
    "\U0000FE0F"               # variation selector
    "\U0000200D"               # zero-width joiner
    "\U000020E3"               # enclosing keycap
    "\U0000FE0E\U0000FE0F"     # text/emoji variation selectors
    "]+"
)


def scrub_for_tts(text):
    """Strips markdown to plain speech-friendly text."""
    # Code blocks -> spoken placeholder
    text = re.sub(r"```[\s\S]*?```", " Code block omitted. ", text)
    # Inline code -> keep contents, drop backticks
    text = re.sub(r"`([^`]*)`", r"\1", text)
    # Images -> drop entirely
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", "", text)
    # Links -> keep the label, drop the URL
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    # Heading hashes
    text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)
    # Blockquotes
    text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
    # Emphasis markers
    text = re.sub(r"\*{1,3}|_{1,3}|~~", "", text)
    # Bullet dashes
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    # Tables -> drop rows entirely
    text = re.sub(r"^\s*\|.*\|\s*$", "", text, flags=re.MULTILINE)
    # Horizontal rules
    text = re.sub(r"^\s*[-=_]{3,}\s*$", "", text, flags=re.MULTILINE)
    # Collapse leftover gaps
    # Emojis and their combining marks
    text = _EMOJI.sub(" ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

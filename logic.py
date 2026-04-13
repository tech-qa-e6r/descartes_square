import re

def calculate_points(text: str) -> int:
    """ Считает сумму баллов из текста (цифры 1-5 в конце строк) """
    score = 0
    if not text:
        return 0
    for line in text.split('\n'):
        line = line.strip()
        match = re.search(r'(?:^|\s)([1-5])$', line)
        if match: 
            score += int(match.group(1))
    return score

def get_verdict(total_action: int, total_status_quo: int, t_dict: dict) -> str:
    """ Определяет текстовый вердикт на основе весов """
    if total_action > total_status_quo:
        return t_dict["verdict_do"]
    elif total_status_quo > total_action:
        return t_dict["verdict_stay"]
    else:
        return t_dict["verdict_draw"]
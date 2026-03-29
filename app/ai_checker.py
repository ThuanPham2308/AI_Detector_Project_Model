from app.predictor import predict_ai_score
from app.sentence_splitter import split_sentences

RED_THRESHOLD = 0.6
YELLOW_THRESHOLD = 0.3

PARA_WEIGHT = 0.3
SENT_WEIGHT = 0.7

PARA_BOOST_THRESHOLD = 0.6
PARA_BOOST_VALUE = 0.05


def get_color(score):
    if score >= RED_THRESHOLD:
        return "red"
    elif score >= YELLOW_THRESHOLD:
        return "yellow"
    else:
        return "black"


def hybrid_score(para_score, sent_score, word_count):
    if word_count < 5:
        combined = para_score
    elif word_count < 10:
        combined = 0.6 * para_score + 0.4 * sent_score
    else:
        combined = PARA_WEIGHT * para_score + SENT_WEIGHT * sent_score

    if para_score >= PARA_BOOST_THRESHOLD:
        combined = min(1.0, combined + PARA_BOOST_VALUE)

    return combined


def check_paragraph(paragraph_text):
    para_score = predict_ai_score(paragraph_text)
    sentences = split_sentences(paragraph_text)

    results = []

    total_words = 0
    weighted_score = 0

    for s in sentences:
        word_count = len(s.split())
        sent_score = predict_ai_score(s)

        final_score = hybrid_score(para_score, sent_score, word_count)

        weighted_score += final_score * word_count
        total_words += word_count

        results.append({
            "text": s,
            "score": final_score,  # giữ dạng 0-1
            "color": get_color(final_score)
        })

    ai_percent = (weighted_score / total_words * 100) if total_words > 0 else 0

    return {
        "sentences": results,
        "ai_percent": ai_percent
    }
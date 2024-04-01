import nltk
from nltk.tokenize import sent_tokenize
from flask import request, render_template, Flask

app = Flask(__name__)

def get_overall_score(positive_count, total_count):
    percentage = (positive_count / total_count) * 100
    if percentage <= 50:
        return round(percentage), "Hmmm there's room for improvement. Let's refine it!"
    elif 50 < percentage <= 60:
        return round(percentage), "Not bad! Let's tweak a few things to make it even stronger."
    elif 60 < percentage <= 80:
        return round(percentage), "You're on the right track! Keep going!"
    else:
        return round(percentage), "Now that is a good email. Fantastic work!"

@app.route('/')
def my_form():
    return render_template('index.html', sentence_scores=[], overall_score=None, overall_comment=None)

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/tips')
def tips_page():
    return render_template('tips.html')

@app.route('/email', methods=['POST'])
def email_form_post():
    text = request.form['email_content']
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    
    sentences = sent_tokenize(text)
    positive_count = 0
    
    sentence_scores = []
    
    for sentence in sentences:
        score = sid.polarity_scores(sentence)['compound']
        sentence_scores.append((sentence, score))
        if score > 0:
            positive_count += 1
    
    overall_score, overall_comment = get_overall_score(positive_count, len(sentences))
    
    return render_template('index.html', sentence_scores=sentence_scores, overall_score=overall_score, overall_comment=overall_comment)

if __name__ == "__main__":
    app.run(port='8088', threaded=False, debug=True)

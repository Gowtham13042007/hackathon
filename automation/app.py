from flask import Flask, render_template, flash
from forms import Ambition
from openai import OpenAI
from searching import get_top3_youtube_links
from my_email import email_sending
from bot1 import botwork
from bot2 import googleforms
import requests
from dotenv import load_dotenv
import os

load_dotenv()

url=os.environ.get("url")

app = Flask(__name__)
app.secret_key = os.environ.get("secret_key")
api_key=os.environ.get("open_ai")

client = OpenAI(api_key=api_key)
all_links_list=[]
summaries=[]

def yesorno(ambition):
        prompt = f"""
        You are an AI classifier.
        Your task is to determine whether the user input describes an ambitious profession.
        If it does, reply only with "Yes".
        If it does not, reply only with "No".
        Do not include any explanation or extra words.

        Input: "{ambition}"
        """
        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a helpful classifier."},
        {"role": "user", "content": prompt}])

        prediction=response.choices[0].message.content.strip()

        return prediction


def oneliner(ambition):
     if len(ambition.strip().split()) == 1:
        return ambition.strip().capitalize()
      
     prompt=f'''Given the following career title, summarize it into 1–2 words that capture the core profession or field as a “dream career” label. Just return the label text without any extra explanation.
                Career Title: {ambition}'''
     response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": '''You are an expert career classifier.You take any career-related description and output a clean, short label of the general field or profession in 1–2 words, without any extra text.'''},
        {"role": "user", "content": prompt}]) 
     
     topics=response.choices[0].message.content.strip()
     return topics


def selectthree(ambition,fields):
    prompt = f'''
    Given the following career description, select the 3 most relevant fields from the provided list that best match the description. Return only the chosen fields as a clean numbered list without any extra explanation.

    Career Description:
    "{ambition}"

    Available Fields:
    {chr(10).join(fields)}
    '''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an expert career advisor who accurately maps ambitions to relevant fields."
            },
            {
                "role": "user",
                "content": prompt.strip()
            }
        ]
    )


    output = response.choices[0].message.content.strip()
    lines = output.strip().split("\n")
    result = [line.split(". ", 1)[1].strip() for line in lines if ". " in line]
    return result


def summary(topic):
     prompt=f'''Given the following topic:         {topic}
                Write a short paragraph (1–2 sentences) describing what someone will learn by studying this topic. Keep it clear and under 40 words.'''
     response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": "You are a learning outcome analyser"},
        {"role": "user", "content": prompt}]) 
     
     topicsummary=response.choices[0].message.content.strip()
     return topicsummary



def studytopics(profession):
    prompt=f'''I want to learn to achieve this ambition: {profession}

Please list only the main topics or areas I need to study, arranged in the perfect step-by-step order for a complete beginner to learn them progressively.

Each topic should build on the previous one, and the user should complete them in sequence to fully master the ambition.

Format the output as a numbered list of headings only, without any explanations or descriptions.(topics must be atmost 7)'''
    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)


    result = response.choices[0].message.content.strip()
    lines = result.strip().split("\n")
    topics = [line.split(". ", 1)[1].strip() for line in lines if ". " in line]
    return topics

@app.route("/", methods=["GET", "POST"])
def index():
    form = Ambition()
    if form.validate_on_submit():
        email_address = form.email.data
        ambition = form.ambition.data
        all_links_list.clear()
        summaries.clear()

        prediction = yesorno(ambition)
        if prediction.lower() == "yes":
            inshort=oneliner(ambition)
            all_fields=botwork(inshort)
            three_fields=selectthree(ambition,all_fields)
            googleforms(email_address,three_fields)

            get_data = requests.get(url)
            full_data = get_data.json()
            responses = full_data["formResponses1"]
            last_response = responses[-1]
    
            career_list=[last_response['giveYour1StChoice'],last_response['giveYour2NdChoice'],last_response['giveYour3RdChoice']]
            for career in career_list:
                full_topics=studytopics(career)
                for topic in full_topics:
                    title_and_links = get_top3_youtube_links(topic)
                    topic_summary = summary(topic)
                    summaries.append(topic_summary)
                    all_links_list.append(title_and_links)

                indexed_topics = list(zip(range(len(full_topics)), full_topics))
                roadmap_html = render_template(
                    "email.html",
                    career=career,
                    topics=indexed_topics,
                    links=all_links_list,
                    summaries=summaries
                )

                email_sending(
                    to_email=email_address,
                    subject="🎯 Your Personalized Learning Plan",
                    html_content=roadmap_html
                )
                
                
                flash(f"✅ Your learning plan of {topic} has been sent to your email.", "success")

        else:
            flash(
                "The ambition you mentioned doesn’t seem like a clear goal. Please be more detailed.",
                "danger"
            )

    return render_template("ambition.html", form=form)


if __name__ == "__main__":
    app.run(debug=False)
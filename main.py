import praw #Reddit API
import os
import dotenv #reads key-value pairs from a .env file
import openai
import time
from icecream import ic #print debugging

dotenv.load_dotenv()
openai.api_key=os.environ.get("OPENAI_API_KEY")

def reddit_search(praw_obj,subreddits):
    all_text=[]
    for subreddit in subreddits:
        ic(subreddit)

    # Let's pull the first post of the week from Reddit

    for post in praw_obj.subreddit(subreddit).top(limit=1,time_filter="week"):
        title=post.title
        all_text.append(title)

        # Upload comments
        post.comments.replace_more(limit=3)
        comments_array=post.comments[:2]
        for comment in comments_array:
            body=comment.body
            ic(subreddit,title)
            ic(body)
            all_text.append(body)
    return ' '.join(all_text)

def engage_ai(reddit_data):
    system_message=f"""Reddit posts and the topic of Cryptocurrency"""
    user_message=f"""Analyze Reddit threads. Identify the most mentioned cryptocurrency
    Reddit Threads:
    {reddit_data}
    """
    messages=[
        {"role":"system","content":f"{system_message}"},
        {"role":"system","content":f"{user_message}"},
    ]
    ic(f"Prompts we send to the language model: {user_message}")
    ans=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        max_tokens=2048,
        message=messages,
    )
    res=ans["choices"][0]["message"]["content"]
    ic(res)
    return res

if __name__=="__main__":
    # Reddit user info
    client_id=os.environ.get("CLIENT_ID")
    client_secret=os.environ.get("CLIENT_SECRET")
    user_agent=os.environ.get("APP_NAME")

    praw_obj=praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )

    subreddits=[
        'cryptocurrency',
        'bitcoin',
        'ethereum',
    ]
    ic(f"Searching: {subreddits}")
    
    # Pulling data from Reddit
    response=reddit_search(praw_obj,subreddits)
    ic(len(response))

    # Send to ai model
    chatgpt_res=engage_ai(response)
    ic(chatgpt_res)
    
import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_product_info():
    return {
        "title": "This Week’s Best Amazon Deal!",
        "description": "Discover a top-rated product on Amazon that's trending now. Great price, excellent reviews, and perfect for your needs!",
        "link": "https://amzn.to/3TH9LnW"
    }

def generate_blog_post(product):
    prompt = f"""
    Write an engaging blog post about {product['title']} found here: {product['link']}.
    Highlight its features and why it's worth buying. End with a strong call to action.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    content = response.choices[0].message.content
    return {
        "title": product["title"],
        "content": f"{content}\n\nBuy now: {product['link']}"
    }

def post_to_wordpress(post):
    wp_url = os.getenv("WP_URL")
    wp_user = os.getenv("WP_USER")
    wp_password = os.getenv("WP_APP_PASSWORD")

    headers = {
        "Content-Type": "application/json"
    }

    auth = (wp_user, wp_password)

    data = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish"
    }

    response = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, auth=auth, json=data)
    
    if response.status_code == 201:
        print("✅ Blog post published successfully!")
        print("Post URL:", response.json()["link"])
    else:
        print("❌ Failed to post:", response.status_code, response.text)

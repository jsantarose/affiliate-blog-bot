import openai
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_product_info(link):
    return {
        "title": "Top-Rated Amazon Find",
        "description": "This product is trending and highly rated. Find out why it’s a must-have!",
        "image": "https://via.placeholder.com/600x400",  # You can replace this later
        "link": link
    }

def generate_blog_post(product):
    prompt = f"""
Write an SEO-optimized blog post about this Amazon product:
Title: {product['title']}
Description: {product['description']}
Affiliate Link: {product['link']}

Include:
- A catchy title
- Introduction
- Key benefits or features
- Why it’s trending
- Final call to action with the link
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['choices'][0]['message']['content']
    return {
        "title": product["title"],
        "content": content
    }

def post_to_wordpress(post):
    wp_url = os.getenv("WORDPRESS_URL")  # Should be your site like: https://www.josephsantarose.com
    username = os.getenv("WORDPRESS_USERNAME")
    app_password = os.getenv("WORDPRESS_PASSWORD")

    credentials = f"{username}:{app_password}"
    token = base64.b64encode(credentials.encode())
    headers = {
        "Authorization": f"Basic {token.decode('utf-8')}",
        "Content-Type": "application/json"
    }

    payload = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish"
    }

    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/posts",
        headers=headers,
        json=payload
    )

    if response.status_code == 201:
        print("✅ Blog post published successfully.")
    else:
        print("❌ Failed to publish post:", response.status_code, response.text)


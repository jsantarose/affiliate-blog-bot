import openai
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_product_info(link):
    return {
        "title": "Top-Rated Amazon Find",
        "description": "This product is trending and highly rated. Find out why it’s a must-have!",
        "image": "https://via.placeholder.com/600x400",  # Placeholder for now
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
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['choices'][0]['message']['content']
    return {
        "title": product["title"],
        "content": content
    }

def post_to_wordpress(post):
    wp = Client(
        os.getenv("WORDPRESS_URL"),
        os.getenv("WORDPRESS_USERNAME"),
        os.getenv("WORDPRESS_PASSWORD")
    )

    wp_post = WordPressPost()
    wp_post.title = post["title"]
    wp_post.content = post["content"]
    wp_post.post_status = "publish"

    wp.call(NewPost(wp_post))


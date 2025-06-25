import requests
from bs4 import BeautifulSoup
import json
import html
import random

def get_product_info(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    try:
        title = soup.find(id="productTitle").get_text(strip=True)
    except:
        title = "Great Amazon Find"

    try:
        img = soup.find("img", {"id": "landingImage"})["src"]
    except:
        img = "https://via.placeholder.com/600x400.png?text=Product+Image"

    try:
        description = soup.find("meta", {"name": "description"})
        description = description["content"] if description else "No description available."
    except:
        description = "No description available."

    return {
        "title": html.unescape(title),
        "image": img,
        "description": html.unescape(description),
        "link": url
    }

def generate_blog_post(product):
    title = product["title"]
    image = product["image"]
    description = product["description"]
    link = product["link"]

    content = f"""
<h2>{title}</h2>
<img src=\"{image}\" alt=\"{title}\" style=\"max-width:100%; height:auto;\" />
<p>{description}</p>
<p><a href=\"{link}\" target=\"_blank\">\ud83d\udc49 Check it out on Amazon</a></p>
"""

    return {
        "title": title,
        "content": content
    }

def post_to_wordpress(post):
    import os
    from requests.auth import HTTPBasicAuth

    wp_url = os.getenv("WP_URL")
    wp_user = os.getenv("WP_USER")
    wp_pass = os.getenv("WP_APP_PASS")

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "title": post["title"],
        "content": post["content"],
        "status": "publish"
    }

    response = requests.post(
        f"{wp_url}/wp-json/wp/v2/posts",
        headers=headers,
        auth=HTTPBasicAuth(wp_user, wp_pass),
        json=data
    )

    if response.status_code == 201:
        print("\u2705 Blog post published successfully!")
        print("Post URL:", response.json().get("link"))
    else:
        print("\u274c Failed to publish blog post.", response.status_code)
        print(response.text)

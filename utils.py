import requests
from datetime import datetime

# ✅ Your WordPress credentials (already filled in)
WORDPRESS_SITE = "https://www.josephsantarose.com"
USERNAME = "jsantarose"
APPLICATION_PASSWORD = "DEQW MHJ2 Jmkw vKZB PzJR 0Sxy"

def get_product_info():
    # Sample product info (you can customize or upgrade this later)
    return {
        "name": "Top-Selling Amazon Find",
        "price": "$19.99",
        "features": ["Durable", "Affordable", "Highly Rated"],
        "affiliate_link": "https://amzn.to/3TH9LnW"
    }

def generate_blog_post(product):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    slug = f"{product['name'].lower().replace(' ', '-')}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    title = f"{product['name']} Review – {timestamp}"
    content = f"""
    <h2>{product['name']}</h2>
    <p>Price: {product['price']}</p>
    <ul>
        {''.join(f'<li>{feature}</li>' for feature in product['features'])}
    </ul>
    <p><a href="{product['affiliate_link']}" target="_blank">Buy now on Amazon</a></p>
    <p><em>Automatically posted on {timestamp}</em></p>
    """

    return {
        "title": title,
        "slug": slug,
        "status": "publish",
        "content": content
    }

def post_to_wordpress(post):
    url = f"{WORDPRESS_SITE}/wp-json/wp/v2/posts"
    headers = {
        "Content-Type": "application/json"
    }
    auth = (USERNAME, APPLICATION_PASSWORD)

    response = requests.post(url, json=post, headers=headers, auth=auth)

    if response.status_code in [200, 201]:
        print("✅ Blog post published successfully!")
        print("Post URL:", response.json().get("link"))
    else:
        print("❌ Failed to publish post:", response.status_code, response.text)


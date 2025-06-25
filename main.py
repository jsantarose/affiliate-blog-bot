import os
import random
from utils import get_product_info, generate_blog_post, post_to_wordpress
from dotenv import load_dotenv

load_dotenv()

# Use your SiteStripe affiliate links
AFFILIATE_LINKS = [
    "https://amzn.to/3TH9LnW",
    "https://amzn.to/45FvP9Q",
    "https://amzn.to/4476YJu",
    "https://amzn.to/45yv6au",
    "https://amzn.to/4k3C9eL"
]

def run_blog_bot():
    print("🔥 Starting blog automation...")

    for _ in range(3):  # Create 3 blog posts
        link = random.choice(AFFILIATE_LINKS)
        product = get_product_info(link)
        post = generate_blog_post(product)
        post_to_wordpress(post)

    print("✅ Blog posts created and published!")

if __name__ == "__main__":
    run_blog_bot()

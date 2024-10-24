import os
from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import requests
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow all origins for simplicity (you can adjust as needed)

# Hugging Face API URL and token
HF_API_URL = "https://dzym1rm5tj.execute-api.eu-north-1.amazonaws.com/staging"
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}

# Load your CSVs (pros and cons, reviews, etc.)
pros_cons_df = pd.read_csv('data/product_pros_and_cons_spacy.csv')
pros_cons_list = pros_cons_df.to_dict('records')
df = pd.read_csv('data/df_reviews_with_summaries_and_clusters_sentiment.csv')

# Sort the df by 'final_cluster' (ascending) and 'sentiment_score' (descending)
df = df.sort_values(
    ['final_cluster', 'sentiment_score'], ascending=[True, False])

# Define categories mapping
categories = {
    0: 'Power and Connectivity Accessories',
    1: 'Amazon Devices and Media Equipment',
    2: 'Computing and Mobile Devices',
    3: 'Home and Office Products',
    4: 'Carrying and Storage Accessories',
    5: 'Audio Equipment and Accessories'
}

# Calculate average sentiment and review count


def query_huggingface(prompt):
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={
            "inputs": prompt,
            "parameters": {
                "max_length": 100,
                "temperature": 0.6,
                "top_p": 0.85,
                "no_repeat_ngram_size": 3,
                "early_stopping": True
            }
        }
    )
    if response.status_code == 200:
        try:
            return response.json()[0]["generated_text"]
        except (KeyError, IndexError):
            return "Error: Could not retrieve text from API response."
    else:
        return f"Error: Could not generate text. Status code: {response.status_code}"


# API route to generate blog posts
@app.route('/api/generate_blog_post', methods=['POST'])
def generate_blog_post_by_category():
    data = request.get_json()  # Get the selected category from the frontend
    selected_category = data.get('category')

    if selected_category not in categories.values():
        return jsonify({"error": "Invalid category"}), 400

    category_id = next((k for k, v in categories.items()
                       if v == selected_category), None)

    # Filter the products by category and get the top product
    top_product = df[df['final_cluster'] == category_id].iloc[0]
    product_name = top_product['name']
    product_category = categories[category_id]

    # Get pros and cons for the product
    entry = next(
        (item for item in pros_cons_list if item['product_name'] == product_name), None)
    if entry:
        pros = entry['pros'].split(',')
        cons = entry['cons'].split(',')

        # Generate the product summary using GPT-2 via Hugging Face
        summary_prompt = (
            f"The {product_name} from the "
            f"{product_category} category is built to offer excellent performance. "
            f"It stands out for its reliability, durability, and value for money. Here's a short overview of this product."
        )
        summary = query_huggingface(summary_prompt)

        # Generate the product features using GPT-2 via Hugging Face
        features_prompt = (
            f"The key features of the "
            f"{product_name} include its high performance, durable design, and superior functionality. "
            "This product is ideal for consumers who need reliable technology. It offers great value compared to competitors."
        )
        features = query_huggingface(features_prompt)

        # Clean up the pros and cons by removing brackets and single quotes
        pros = [pro.strip().replace("'", "").replace(
            "[", "").replace("]", "") for pro in pros]
        cons = [con.strip().replace("'", "").replace(
            "[", "").replace("]", "") for con in cons]
        # Remove any empty pros and cons
        pros = [pro.strip()
                for pro in pros if pro.strip()]  # Remove empty strings
        cons = [con.strip()
                for con in cons if con.strip()]  # Remove empty strings

        # Combine the generated sections into a blog post
        blog_post = (
            f"## Product Overview\n\n{summary}\n\n"
            f"## Key Features\n\n{features}\n\n"
            f"## Pros\n\n- " + '\n- '.join(pros) + "\n\n"
            f"## Cons\n\n- " + '\n- '.join(cons) + "\n\n"
            f"## Conclusion\n\n"
            f"In conclusion, the {product_name} offers excellent "
            f"{pros[0]} and {pros[1]}, "
            f"but keep in mind that it has some drawbacks such as {cons[0]}."
        )

        return jsonify({
            'product_name': product_name,
            'blog_post': blog_post
        })

    return jsonify({"error": "Product not found for this category"}), 404


if __name__ == '__main__':
    app.run(debug=True)

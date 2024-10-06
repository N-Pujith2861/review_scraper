from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from playwright.async_api import async_playwright
import openai
import traceback
import os

app = FastAPI()

# Set your OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

async def fetch_reviews(url, page_number):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f"{url}?page={page_number}")

        # Use LLM to identify CSS selectors dynamically
        html_content = await page.content()
        
        # Send the HTML to the LLM for CSS selector suggestions
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use other models if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant that provides CSS selectors."},
                {"role": "user", "content": f"Given the following HTML, suggest CSS selectors for extracting reviews:\n\n{html_content}"}
            ]
        )

        # Extract the CSS selectors from the response
        css_selectors = response['choices'][0]['message']['content'].strip().split("\n")

        # Assuming the LLM provides selectors in the format:
        # review_selector, title_selector, body_selector, rating_selector, reviewer_selector
        review_selector = css_selectors[0]
        title_selector = css_selectors[1]
        body_selector = css_selectors[2]
        rating_selector = css_selectors[3]
        reviewer_selector = css_selectors[4]

        reviews = await page.query_selector_all(review_selector)  # Dynamic review selector

        reviews_data = []
        for review in reviews:
            title = await review.query_selector(title_selector)  # Dynamic title selector
            body = await review.query_selector(body_selector)    # Dynamic body selector
            rating = await review.query_selector(rating_selector)  # Dynamic rating selector
            reviewer = await review.query_selector(reviewer_selector)  # Dynamic reviewer selector
            
            # Collect the review data if the elements are found
            if title and body and rating and reviewer:
                reviews_data.append({
                    "title": await title.inner_text(),
                    "body": await body.inner_text(),
                    "rating": int(await rating.inner_text()),  # Make sure to convert to int
                    "reviewer": await reviewer.inner_text(),
                })

        await browser.close()
        return reviews_data

@app.get("/api/reviews")
async def get_reviews(url: str, page_number: int = 1):
    try:
        reviews_data = await fetch_reviews(url, page_number)
        return JSONResponse(content={"reviews_count": len(reviews_data), "reviews": reviews_data})

    except HTTPException as http_err:
        return JSONResponse(content={"error": str(http_err.detail)}, status_code=http_err.status_code)

    except Exception as e:
        # Log the error for debugging
        traceback.print_exc()
        return JSONResponse(content={"error": "An unexpected error occurred. Please try again later."}, status_code=500)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)

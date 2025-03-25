from pydantic import BaseModel, Field
import httpx
import asyncio
import os
from typing import List, Optional, Dict, Any
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("API_KEY", "")


# Define example models
class Person(BaseModel):
    name: str = Field(..., description="Name")
    age: int = Field(..., description="Age")
    height: float = Field(..., description="Height in cm")
    occupation: Optional[str] = Field(None, description="Occupation")


class BookInfo(BaseModel):
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author")
    publish_year: int = Field(..., description="Year published")
    price: float = Field(..., description="Price")
    categories: List[str] = Field(default_factory=list, description="Category tags")


class NewsArticle(BaseModel):
    headline: str = Field(..., description="News headline")
    content: str = Field(..., description="News content")
    date: str = Field(..., description="Publication date")
    source: str = Field(..., description="News source")
    tags: List[str] = Field(default_factory=list, description="Tags")


async def structure_data(
    content: str, model: BaseModel, system_prompt: str = None, model_name: str = None
) -> Dict[str, Any]:
    """
    Send a structuring request using a predefined Pydantic model

    Args:
        content: The text content to structure
        model: The Pydantic model defining the structure
        system_prompt: Optional system prompt to guide the LLM
        model_name: Optional model name (e.g., 'openai:gpt-4o', 'anthropic:claude-3-opus-latest')
    """
    schema_json = model.model_json_schema()

    request_data = {
        "content": content,
        "schema_description": json.dumps(schema_json),
        "system_prompt": system_prompt,
        "is_need_schema_description": False,
    }

    if model_name:
        request_data["model_name"] = model_name

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/api/structure",
            json=request_data,
            headers={"X-API-Key": API_KEY},
        )
        return response.json()


async def model_comparison_example():
    """Compare the results of different models on the same task"""
    news_text = """
    OpenAI Releases Major GPT-4 Update
    On March 20, 2024, OpenAI announced a significant upgrade to GPT-4. This update brings several important improvements, including enhanced multimodal capabilities and better reasoning abilities.
    Source: Tech Daily
    Tags: AI, GPT-4, Technology Update
    """

    # Select a few models for comparison
    model_names = [
        "openai:gpt-4o",  # OpenAI's GPT-4o
        "anthropic:claude-3-5-sonnet-latest",  # Anthropic's Claude
    ]

    print("\nModel Comparison for News Article Structuring:")
    print("=" * 60)

    for model_name in model_names:
        try:
            result = await structure_data(
                content=news_text, model=NewsArticle, model_name=model_name
            )
            print(f"\nResults from {model_name}:")
            if result.get("success"):
                print(f"Data: {result['data']}")
            else:
                print(f"Error: {result.get('error')}")
        except Exception as e:
            print(f"Error using {model_name}: {str(e)}")


async def main():
    # Check if API_KEY is set
    if not API_KEY:
        print(
            "WARNING: API_KEY environment variable is not set. API requests may fail."
        )
        print("Please set the API_KEY in your .env file and try again.")
        return

    # Example 1: Structuring person information
    person_text = "John is a 32-year-old software engineer, with a height of the 182.5 centimeters."
    person_system_prompt = "You are a personal information extraction expert. Please extract the person's name, age, height, and occupation from the text."

    person_result = await structure_data(person_text, Person, person_system_prompt)
    print("\nPerson Information Structuring Result:")
    print(person_result)

    # Example 2: Structuring book information
    book_text = "The Three-Body Problem is a science fiction novel by Liu Cixin, published in 2008, priced at $15.99, in the science fiction and fantasy categories."
    book_result = await structure_data(book_text, BookInfo)
    print("\nBook Information Structuring Result:")
    print(book_result)

    # Example 3: Structuring news article
    news_text = """
    OpenAI Releases Major GPT-4 Update
    On March 20, 2024, OpenAI announced a significant upgrade to GPT-4. This update brings several important improvements, including enhanced multimodal capabilities and better reasoning abilities.
    Source: Tech Daily
    Tags: AI, GPT-4, Technology Update
    """
    news_result = await structure_data(news_text, NewsArticle)
    print("\nNews Article Structuring Result:")
    print(news_result)

    # Example 4: Model comparison
    try:
        print("\nRunning model comparison example...")
        await model_comparison_example()
    except Exception as e:
        print(f"Error in model comparison: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

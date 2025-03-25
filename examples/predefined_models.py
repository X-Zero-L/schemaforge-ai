"""
Predefined Model Usage Examples

This script demonstrates how to use predefined Pydantic models to structure data
using the AI structuring API with support for multiple AI models.
"""

import httpx
import asyncio
import os
import json
from typing import List, Optional, Dict, Any, Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
API_KEY = os.getenv("API_KEY", "")
# Default API base URL
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


# Define example models
class Person(BaseModel):
    """Model representing a person's basic information"""
    name: str = Field(..., description="Person's full name")
    age: int = Field(..., description="Age in years")
    height: float = Field(..., description="Height in centimeters")
    occupation: Optional[str] = Field(None, description="Current occupation or profession")


class BookInfo(BaseModel):
    """Model representing book information"""
    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Author's name")
    publish_year: int = Field(..., description="Year when the book was published")
    price: float = Field(..., description="Book price in the local currency")
    categories: List[str] = Field(default_factory=list, description="List of book categories/genres")


class NewsArticle(BaseModel):
    """Model representing a news article"""
    headline: str = Field(..., description="Article headline or title")
    content: str = Field(..., description="Main article content")
    date: str = Field(..., description="Publication date (YYYY-MM-DD format)")
    source: str = Field(..., description="News source or publisher")
    tags: List[str] = Field(default_factory=list, description="Article tags or keywords")


async def structure_data(
    content: str, 
    model: Type[BaseModel], 
    system_prompt: str = None, 
    model_name: str = None
) -> Dict[str, Any]:
    """
    Send a structuring request using a predefined Pydantic model

    Args:
        content: The text content to structure
        model: The Pydantic model class defining the structure
        system_prompt: Optional system prompt to guide the AI model
        model_name: Optional model name (e.g., 'openai:gpt-4o', 'anthropic:claude-3-opus-latest')

    Returns:
        Dictionary containing the structured data and metadata
    """
    schema_json = model.model_json_schema()

    request_data = {
        "content": content,
        "schema_description": json.dumps(schema_json),
        "is_need_schema_description": False,
    }

    if system_prompt:
        request_data["system_prompt"] = system_prompt
        
    if model_name:
        request_data["model_name"] = model_name

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{API_BASE_URL}/api/v1/structure",
            json=request_data,
            headers={"X-API-Key": API_KEY},
            timeout=60
        )
        return response.json()


async def person_info_example():
    """Example 1: Structuring person information"""
    person_text = "John is a 32-year-old software engineer, with a height of 182.5 centimeters."
    person_system_prompt = "You are a personal information extraction expert. Extract the person's name, age, height, and occupation from the text."

    print("\n=== Example 1: Person Information Structuring ===")
    result = await structure_data(
        content=person_text, 
        model=Person, 
        system_prompt=person_system_prompt
    )
    
    if result.get("success"):
        print("✅ Success!")
        print(f"Structured Data: {json.dumps(result['data'], indent=2)}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print(f"Model Used: {result.get('model_used', 'default')}")


async def book_info_example():
    """Example 2: Structuring book information"""
    book_text = "The Three-Body Problem is a science fiction novel by Liu Cixin, published in 2008, priced at $15.99, in the science fiction and fantasy categories."
    
    print("\n=== Example 2: Book Information Structuring ===")
    result = await structure_data(
        content=book_text, 
        model=BookInfo,
        model_name="openai:gpt-4o"
    )
    
    if result.get("success"):
        print("✅ Success!")
        print(f"Structured Data: {json.dumps(result['data'], indent=2)}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print(f"Model Used: {result.get('model_used', 'default')}")


async def news_article_example():
    """Example 3: Structuring news article"""
    news_text = """
    OpenAI Releases Major GPT-4 Update
    
    On March 20, 2024, OpenAI announced a significant upgrade to GPT-4. This update brings several 
    important improvements, including enhanced multimodal capabilities and better reasoning abilities.
    The company claims this new version shows a 30% reduction in hallucinations compared to previous models.
    
    Source: Tech Daily
    Tags: AI, GPT-4, Technology Update
    """
    
    print("\n=== Example 3: News Article Structuring ===")
    result = await structure_data(
        content=news_text, 
        model=NewsArticle
    )
    
    if result.get("success"):
        print("✅ Success!")
        print(f"Structured Data: {json.dumps(result['data'], indent=2)}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print(f"Model Used: {result.get('model_used', 'default')}")


async def model_comparison_example():
    """Example 4: Compare different AI models on the same task"""
    news_text = """
    OpenAI Releases Major GPT-4 Update
    On March 20, 2024, OpenAI announced a significant upgrade to GPT-4. This update brings several 
    important improvements, including enhanced multimodal capabilities and better reasoning abilities.
    Source: Tech Daily
    Tags: AI, GPT-4, Technology Update
    """

    # Models to compare
    model_names = [
        "openai:gpt-4o",  # OpenAI's GPT-4o
        "anthropic:claude-3-7-sonnet-latest",  # Anthropic's Claude
    ]

    print("\n=== Example 4: Model Comparison ===")
    print("Comparing different AI models on the same news article structuring task")
    
    for model_name in model_names:
        print(f"\n📋 Testing model: {model_name}")
        try:
            result = await structure_data(
                content=news_text, 
                model=NewsArticle, 
                model_name=model_name
            )
            
            if result.get("success"):
                print("✅ Success!")
                print(f"Structured Data: {json.dumps(result['data'], indent=2)}")
            else:
                print(f"❌ Error: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error using {model_name}: {str(e)}")


async def custom_model_example():
    """Example 5: Using a custom model for specific use case"""
    
    # Define a custom model for recipe information
    class Recipe(BaseModel):
        """Model representing cooking recipe information"""
        name: str = Field(..., description="Recipe name")
        prep_time: int = Field(..., description="Preparation time in minutes")
        cooking_time: int = Field(..., description="Cooking time in minutes")
        ingredients: List[str] = Field(..., description="List of ingredients")
        instructions: List[str] = Field(..., description="List of cooking instructions/steps")
        cuisine: Optional[str] = Field(None, description="Cuisine type (e.g., Italian, Chinese)")
        difficulty: Optional[str] = Field(None, description="Recipe difficulty level")
        
    recipe_text = """
    Classic Chocolate Chip Cookies
    
    Prep Time: 15 minutes
    Cooking Time: 12 minutes
    
    Ingredients:
    - 2 1/4 cups all-purpose flour
    - 1 teaspoon baking soda
    - 1 teaspoon salt
    - 1 cup unsalted butter, softened
    - 3/4 cup granulated sugar
    - 3/4 cup packed brown sugar
    - 2 large eggs
    - 2 teaspoons vanilla extract
    - 2 cups chocolate chips
    
    Instructions:
    1. Preheat oven to 375°F (190°C).
    2. Combine flour, baking soda, and salt in a small bowl.
    3. Beat butter, granulated sugar, and brown sugar in a large bowl until creamy.
    4. Add eggs one at a time, beating well after each addition.
    5. Stir in vanilla extract.
    6. Gradually beat in flour mixture.
    7. Stir in chocolate chips.
    8. Drop by rounded tablespoons onto ungreased baking sheets.
    9. Bake for 9 to 11 minutes or until golden brown.
    10. Let stand for 2 minutes; remove to wire racks to cool completely.
    
    Cuisine: American
    Difficulty: Easy
    """
    
    print("\n=== Example 5: Custom Recipe Model ===")
    result = await structure_data(
        content=recipe_text, 
        model=Recipe,
        model_name="openai:gpt-4o"
    )
    
    if result.get("success"):
        print("✅ Success!")
        print(f"Structured Data: {json.dumps(result['data'], indent=2)}")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    print(f"Model Used: {result.get('model_used', 'default')}")


async def main():
    # Check if API_KEY is set
    if not API_KEY:
        print("⚠️ WARNING: API_KEY environment variable is not set. API requests may fail.")
        print("Please set the API_KEY in your .env file and try again.")
        return

    try:
        # Example 1: Structuring person information
        await person_info_example()
        
        # Example 2: Structuring book information
        await book_info_example()
        
        # Example 3: Structuring news article
        await news_article_example()
        
        # Example 4: Model comparison
        await model_comparison_example()
        
        # Example 5: Using a custom model
        await custom_model_example()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please ensure the API service is running and your API key is valid.")


if __name__ == "__main__":
    asyncio.run(main())

# Gemini AI Agent - Research Assistant

This project is an AI-powered research assistant that uses Google’s Gemini large language model (LLM) to generate structured research summaries based on user queries. It integrates web search and Wikipedia tools to enhance responses and allows users to save generated research papers locally with timestamps.

---

## Features

- Interactive prompt to ask any research question
- Uses Gemini LLM (`gemini-1.5-flash`) via Google Generative AI API
- Integrated web search (DuckDuckGo) and Wikipedia lookup tools
- Structured JSON output parsed with Pydantic for consistent results
- Option to save generated research papers to a timestamped `.txt` file in the project directory

---

## Prerequisites

- Python 3.8 or higher
- Install dependencies with:
  ```bash
  pip install -r requirements.txt

## How to Get Gemini API Key

Google’s Gemini API is part of their **Generative AI services** and requires an API key for access.

1. Visit the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Generative AI API** for your project.
3. Create or locate your API key under **APIs & Services > Credentials**.
4. Add your API key to your `.env` file as shown below:

    ```
    GEMINI_API_KEY=your_actual_api_key_here
    ```

> **Note:** Access to Gemini API might be limited or require joining a waitlist in beta.  
> For improved and more stable access, you can **purchase or subscribe to a paid plan** through Google Cloud’s pricing and billing options.  
> Having a valid Gemini API key in your `.env` will enable your AI agent to perform better and access more features.

---


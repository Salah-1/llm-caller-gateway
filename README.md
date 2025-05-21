````markdown
# LLM Caller Gateway
Uses Firewall and other ACLs to guard against unauthorized use.

Acts as LLM caller gateway
A FastAPI-based service that receives external call requests, validates them using a secure hash, processes user input, interacts with a large language model (OpenAI or Gemini), and returns a structured response.

## Features

- ✅ Secure endpoint validation via hash
- 🧠 Supports user input processing (e.g., summarize text, answer questions)
- 🔁 Integrates with LLMs like OpenAI or Google Gemini
- 📦 Returns output in a consistent JSON format

## How It Works

1. **Receive Call**  
   A request hits the FastAPI endpoint with an input payload and a hash.

2. **Validate**  
   The server checks the hash to ensure the request is trusted.

3. **Process Input**  
   Parses user instructions (e.g., summarize this text, answer this question).

4. **Query LLM**  
   Forwards the processed prompt to an LLM (OpenAI or Gemini).

5. **Return Response**  
   Sends back a JSON response with the LLM’s output in a predefined format.

## Example Request

```http
POST /process
Content-Type: application/json

{
  "input": "Summarize the following: The quick brown fox jumps over the lazy dog.",
   
}
````

## Example Response

```json
{
  "status": "success",
  "result": "A quick fox jumps over a lazy dog."
}
```

## Setup

⚠️ **Do not commit your `.env` file or API keys to version control.** Add `.env` to your `.gitignore`.


```bash
git clone https://github.com/yourusername/llm-caller-gateway.git
cd llm-caller-gateway
pip install -r requirements.txt
uvicorn main:app --reload
```

## Environment Variables

Create a `.env` file for secrets and API keys:

```env
OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
SHARED_SECRET=your_hash_secret
```
END
```

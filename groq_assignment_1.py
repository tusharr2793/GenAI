
import os
import requests

# Task 2: Keep the model separate from the request code.
MODEL = "openai/gpt-oss-20b"

# Groq Chat Completions API endpoint.
API_URL = "https://api.groq.com/openai/v1/chat/completions"


def ask_groq(prompt):
    """Send one prompt to Groq and return the generated answer."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        print("Error: GROQ_API_KEY is not set.")
        print("Set your API key in the terminal and try again.")
        return

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Task 3: Include all required request parameters.
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "top_p": 1
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        # Handle HTTP errors, such as an invalid API key.
        response.raise_for_status()

        result = response.json()

        # Check that the expected answer exists.
        choices = result.get("choices", [])
        if not choices:
            print("Error: The API response did not contain any choices.")
            return

        message = choices[0].get("message", {})
        answer = message.get("content")

        if not isinstance(answer, str) or not answer.strip():
            print("Error: No answer text was found in the response.")
            return

        print("\nResponse:")
        print(answer)

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again.")

    except requests.exceptions.HTTPError as error:
        print(f"HTTP Error: {error}")
        try:
            print("Details:", response.text)
        except UnboundLocalError:
            pass

    except requests.exceptions.RequestException as error:
        print(f"Network or request error: {error}")

    except ValueError:
        print("Error: The API returned invalid JSON.")

    except (KeyError, IndexError, TypeError):
        print("Error: The response had an unexpected format.")


# Task 1 and Task 5: Accept multiple prompts until the user exits.
def main():
    print("Welcome to the Groq AI Chat Program!")
    print("Type 'exit' to quit.")

    while True:
        prompt = input("\nEnter your prompt: ").strip()

        if prompt.lower() == "exit":
            print("Goodbye!")
            break

        if not prompt:
            print("Please enter a question. Empty prompts are not allowed.")
            continue

        ask_groq(prompt)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""CLI tool to send words of affirmation to the Fickle Ferrets API."""

import sys
import httpx
from typing import NoReturn

# Configure stdout to handle Unicode on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main() -> None:
    """Send words of affirmation to the ferrets."""
    # Check if affirmation text was provided
    if len(sys.argv) < 2:
        print("❌ Error: Please provide words of affirmation!")
        print("\nUsage:")
        print('  uv run post_affirm "Your affirmation here"')
        print('  post_affirm "You are amazing ferrets!"')
        sys.exit(1)
    
    # Get the affirmation from command line arguments
    # Join all arguments in case the user didn't use quotes
    affirmation: str = " ".join(sys.argv[1:])
    
    if not affirmation.strip():
        print("❌ Error: Affirmation cannot be empty!")
        sys.exit(1)
    
    # API endpoint
    api_url: str = "http://localhost:8000/affirmation"
    
    print(f"🦦 Sharing with the ferrets: \"{affirmation}\"")
    print("⏳ Sending...")
    
    try:
        # Send the affirmation
        response: httpx.Response = httpx.post(
            api_url,
            json={"words_of_affirmation": affirmation},
            timeout=10.0
        )
        response.raise_for_status()
        
        # Parse response
        data: dict[str, str] = response.json()
        affirmation_id: str = data.get("affirmation_id", "unknown")
        message: str = data.get("message", "")
        
        print("\n✅ Success!")
        print(f"📝 Affirmation ID: {affirmation_id}")
        print(f"💬 {message}")
        print("\n👀 Check the server logs to see the ferrets' reaction!")
        
    except httpx.ConnectError:
        print("\n❌ Error: Could not connect to the API!")
        print("Make sure the server is running at http://localhost:8000")
        print("\nStart the server with:")
        print("  uv run python -m app.main")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"\n❌ HTTP Error: {e.response.status_code}")
        print(f"Response: {e.response.text}")
        sys.exit(1)
    except httpx.TimeoutException:
        print("\n❌ Error: Request timed out!")
        print("The server might be overloaded or not responding.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


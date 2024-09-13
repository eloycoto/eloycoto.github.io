
Google Gemini Workshop: Function Calling and AI Insights
===========================================================

:date: 2024-09-13 12:00
:language: en-GB
:author: eloycoto
:head: Google Gemini Workshop: Function Calling and AI Insights
:index_title: Reflections on a Google Gemini Workshop
:metatitle: Google Gemini Workshop: Exploring Function Calling and AI Capabilities
:tags: python, ai
:metatags: artificial intelligence, Google Gemini, function calling, AI workshop, LLaMA model
:description: Reflections on an insightful workshop about Google Gemini and function calling, comparing its performance with LLaMA 3.1:8b in handling multiple product queries.
:keywords: Google Gemini, function calling, AI workshop, hackspace, LLaMA model, AI comparison, product stock query, AI programming

I went to an awesome workshop at our local hackspace about Google Gemini and
function calling. I can only say thanks to `Merchi <https://x.com/mgarod3>`_
for giving it; I learned a ton of things regarding Gemini models and AI in
general.

During the workshop, we tried to see how to chain functions when multiple items
need to pass through the function. We used a prompt like:

**"Do you have stock of iPhone 8 or Google Pixel 9?"**

The function defines the way to get the stock for a given product.


.. code-block:: python

    tools = [
      {
            "type": "function",
            "function": {
                "name": "retrieve_stock_for_item",
                "description": "Get the stock information for the given product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The product name to check the stock."
                        }
                    },
                    "required": ["product_name"]
                }
            }
        }
    ]


A normal user, who reasons logically, will check the function for two items.
However, Gemini only returned one function call for one product. I tried with
LLaMA 3.1:8b, and it detected both products and returned both function calls
without much issue (See the tool_calls field).

.. code-block:: json

    {
        "id": "chatcmpl-514",
        "object": "chat.completion",
        "created": 1726234612,
        "model": "llama3.1:8b",
        "system_fingerprint": "fp_ollama",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_e0f4geqf",
                            "type": "function",
                            "function": {
                                "name": "retrieve_stock_for_item",
                                "arguments": "{\"product_name\":\"Iphone 8\"}"
                            }
                        },
                        {
                            "id": "call_cbnhz6qu",
                            "type": "function",
                            "function": {
                                "name": "retrieve_stock_for_item",
                                "arguments": "{\"product_name\":\"Google Pixel 9\"}"
                            }
                        }
                    ]
                },
                "finish_reason": "tool_calls"
            }
        ],
        "usage": {
            "prompt_tokens": 172,
            "completion_tokens": 46,
            "total_tokens": 218
        }
    }


And the full code if you want to try it:


.. code-block:: python

    import requests
    import json

    model="llama3.1:8b"

    tools = [
      {
            "type": "function",
            "function": {
                "name": "retrieve_stock_for_item",
                "description": "Get the stock information for the given product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "product_name": {
                            "type": "string",
                            "description": "The product name to check the stock."
                        }
                    },
                    "required": ["product_name"]
                }
            }
        }
    ]

    messages = [
        {
            "content": "Do you have stock of Iphone 8 or Google Pixel 9?",
            "role": "user"
        }
    ]

    data={
        "messages": messages,
        "tools": tools,
        "model": model,
        "temperature": 0
    }

    response = requests.post('http://ollama.acalustra.local:11434/v1/chat/completions',
        headers={"Content-Type": "application/json"},
        json=data)
    print(json.dumps(response.json(), indent=4))


It's fascinating that this can be achieved with just 40 lines of code. Truly fascinating!

Thanks Merchi for the workshop!

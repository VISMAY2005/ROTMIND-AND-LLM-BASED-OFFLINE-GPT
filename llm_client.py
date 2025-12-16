# llm_client.py
import time
import os
import json

# Example LLM client abstraction.
# It exposes stream_chat(prompt, memory) which yields string tokens (for streaming display)

class LLMClient:
    def __init__(self, model_name="mock", **kwargs):
        """
        model_name: "mock" (default), "openai", "mistral", etc.
        If using a real provider, add API-key configuration here.
        """
        self.model_name = model_name
        self.kwargs = kwargs

    def stream_chat(self, prompt, memory=None):
        """
        Generator that yields tokens (strings). The main app will insert each token
        into the chat UI as they arrive.

        If you want to integrate a real provider:
         - For OpenAI: use the streaming completions (Server-Sent Events) and yield chunks.
         - For other local models: stream tokens as they're generated.
        """
        # If user selected a real model name (e.g., 'openai') you can branch here.
        if self.model_name == "openai":
            # Example stub: you would call OpenAI streaming API here and yield tokens
            # require openai package and API key
            raise NotImplementedError("OpenAI streaming not implemented in this stub. See README to configure.")
        elif self.model_name == "mistral":
            # Stub for other provider
            raise NotImplementedError("Mistral streaming not implemented in this stub.")
        else:
            # Mock streamer: slowly yields a fake reply
            reply = self._mock_reply(prompt, memory)
            # yield token-by-token (simulate)
            for ch in reply:
                yield ch
                time.sleep(0.01)  # small delay to give streaming feeling
            # done

    def _mock_reply(self, prompt, memory):
        # Quick heuristic "smart-ish" mock using memory retrieval if provided
        mem_snippet = ""
        try:
            if memory is not None:
                # memory.search() should return combined text of top results or empty string
                mem_snippet = memory.search(prompt, top_k=2)
        except Exception:
            mem_snippet = ""
        base = f"Hi — this is ROT-MIND (mock response).\nYou asked: {prompt}\n"
        if mem_snippet:
            base += f"\nRelevant memory:\n{mem_snippet}\n"
        base += "\n(End of mock response.)"
        return base

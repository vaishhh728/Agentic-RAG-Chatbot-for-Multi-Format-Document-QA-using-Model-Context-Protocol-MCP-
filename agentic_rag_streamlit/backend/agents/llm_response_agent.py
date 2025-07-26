class LLMResponseAgent:
    def generate_answer(self, query, chunks):
        prompt = f"Answer this: '{query}' using only:\n" + "\n".join(chunks)
        return f"[Simulated LLM Answer] Based on: {prompt[:100]}..."
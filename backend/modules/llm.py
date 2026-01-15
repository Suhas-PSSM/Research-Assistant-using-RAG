import os
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_llm_chain(retriever):
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant"
    )

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are an AI-powered research assistant trained to help users understand documents and related questions.

Your job is to provide clear, accurate, and helpful responses based **only on the provided context**.

---

🔍 **Context**:
{context}

🙋‍♂️ **User Question**:
{question}

---

💬 **Answer**:
- Respond in a calm, factual, and respectful tone.
- Use simple explanations when needed.
- If the context does not contain the answer, say: "I'm sorry, but I couldn't find relevant information in the provided documents."
- Do NOT make up facts.
"""
    )

    def run_chain(inputs):
        question = inputs["question"]

        docs = retriever._get_relevant_documents(question)
        context = "\n\n".join(d.page_content for d in docs)

        formatted_prompt = prompt.format(context=context, question=question)
        answer = llm.invoke(formatted_prompt)

        return {
            "result": answer.content if hasattr(answer, "content") else str(answer),
            "source_documents": docs
        }

    return RunnableLambda(run_chain)
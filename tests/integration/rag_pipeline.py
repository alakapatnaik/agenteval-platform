from langchain_ollama import OllamaLLM, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


def build_rag_chain():
    """
    Build RAG pipeline using modern LangChain LCEL syntax
    """
    docs = [
        Document(
            page_content=(
                "Red Hat OpenShift AI is a platform for "
                "running AI and ML workloads on Kubernetes. "
                "It supports model serving using KServe and "
                "integrates with Jupyter notebooks for data "
                "science workflows."
            ),
            metadata={"source": "openshift-ai-overview"}
        ),
        Document(
            page_content=(
                "KServe is a Kubernetes-native model inference "
                "platform used in OpenShift AI. It supports "
                "TensorFlow, PyTorch, and scikit-learn models. "
                "KServe handles autoscaling and canary rollouts "
                "for ML model deployments."
            ),
            metadata={"source": "kserve-docs"}
        ),
        Document(
            page_content=(
                "OpenShift AI model serving supports both "
                "single-model serving and multi-model serving. "
                "Single-model serving dedicates resources to "
                "one model. Multi-model serving shares resources "
                "across multiple models for efficiency."
            ),
            metadata={"source": "model-serving-docs"}
        ),
        Document(
            page_content=(
                "Data science pipelines in OpenShift AI are "
                "built on Kubeflow Pipelines. They enable "
                "automated ML workflows from data preparation "
                "to model training and deployment."
            ),
            metadata={"source": "pipelines-docs"}
        ),
        Document(
            page_content=(
                "OpenShift AI includes a model registry for "
                "storing and versioning ML models. Models can "
                "be promoted from development to production "
                "through approval workflows."
            ),
            metadata={"source": "model-registry-docs"}
        ),
    ]

    # Step 1 — embeddings + vector store
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="openshift_ai_docs"
    )
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 2}
    )

    # Step 2 — prompt template
    prompt = ChatPromptTemplate.from_template("""
You are an assistant for Red Hat OpenShift AI questions.
Answer based ONLY on the context provided below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {question}

Answer:""")

    # Step 3 — LLM
    llm = OllamaLLM(model="llama3.2", temperature=0)

    # Step 4 — LCEL chain: retriever → prompt → llm
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain, retriever
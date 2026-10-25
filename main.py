from core.logger import get_logger


logger = get_logger(__name__)


def main():
    logger.info("Starting RAG Supreme Court Judgements application")
    print("Hello from rag-sc-judgements!")


if __name__ == "__main__":
    main()

# Decisions Log

A concise record of why specific tools and approaches are chosen in this project.

---

## 1. Vector Database: Why Qdrant over ChromaDB

* **Status:** Accepted
* **Choice:** **Qdrant** (via Docker)

### Why not ChromaDB?
* **Not built for scale:** Chroma is great for quick prototypes, but struggles with large-scale datasets like 75 years of Supreme Court judgments.
* **Deployment issues:** More difficult to manage, configure, and reliably run in a reproducible deployment setup.

### Why Qdrant?
* **Easy to deploy:** Runs effortlessly as a lightweight single container via Docker Compose (`docker-compose.yml`).
* **Runs locally & in production:** Can be run locally on `localhost:6333` / `6334` for development and seamlessly transitioned to production without changing code or logic.
* **Built for scale & speed:** Handles large vector collections with high performance and low latency.

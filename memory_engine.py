# memory_engine.py
import os
import json
import numpy as np

try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except Exception:
    ST_AVAILABLE = False

class MemoryEngine:
    """
    Simple memory engine supporting:
    - add_document(text, metadata)
    - search(query, top_k=3) -> returns concatenated top text results
    """
    def __init__(self, dim=384, model_name="all-MiniLM-L6-v2"):
        self.dim = dim
        self.model_name = model_name
        self.docs = []  # list of dicts: {"text":..., "meta":..., "vec": np.array}
        # load embedder if available
        self.embedder = None
        if ST_AVAILABLE:
            try:
                self.embedder = SentenceTransformer(model_name)
                # update dim on success
                self.dim = self.embedder.get_sentence_embedding_dimension()
            except Exception:
                self.embedder = None

        if FAISS_AVAILABLE and self.embedder is not None:
            try:
                self.index = faiss.IndexFlatIP(self.dim)
                self.recreate_index()
            except Exception:
                self.index = None
        else:
            self.index = None

    def recreate_index(self):
        # reset index using current vectors
        if self.index is None:
            return
        vecs = [d["vec"] for d in self.docs] if self.docs else []
        if vecs:
            mat = np.vstack(vecs).astype('float32')
            # normalize for cosine-sim using inner product after normalization
            faiss.normalize_L2(mat)
            self.index.reset()
            self.index.add(mat)

    def _embed(self, texts):
        if self.embedder:
            emb = self.embedder.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            # normalize for cosine-sim
            try:
                import numpy as np
                faiss.normalize_L2(emb)
            except Exception:
                pass
            return emb
        else:
            # dummy embed: hash-based small vector
            import numpy as np
            out = []
            for t in texts:
                h = abs(hash(t)) % (10**8)
                rng = np.random.RandomState(h)
                v = rng.rand(self.dim).astype('float32')
                out.append(v)
            return np.vstack(out)

    def add_document(self, text, metadata=None):
        vec = self._embed([text])[0]
        self.docs.append({"text": text, "meta": metadata or {}, "vec": vec})
        if self.index is not None:
            faiss.normalize_L2(vec.reshape(1, -1))
            self.index.add(vec.reshape(1, -1))

    def search(self, query, top_k=3):
        if not self.docs:
            return ""
        qvec = self._embed([query])[0].astype('float32')
        if self.index is not None:
            faiss.normalize_L2(qvec.reshape(1, -1))
            D, I = self.index.search(qvec.reshape(1, -1), top_k)
            results = []
            for idx in I[0]:
                if idx < len(self.docs):
                    results.append(self.docs[idx]["text"])
            return "\n---\n".join(results)
        else:
            # brute-force cosine similarity on self.docs
            import numpy as np
            def cos(a,b):
                num = np.dot(a,b)
                den = (np.linalg.norm(a)*np.linalg.norm(b)+1e-9)
                return float(num/den)
            sims = [(cos(qvec, d["vec"]), d["text"]) for d in self.docs]
            sims.sort(key=lambda x: x[0], reverse=True)
            top = [t for s,t in sims[:top_k]]
            return "\n---\n".join(top)

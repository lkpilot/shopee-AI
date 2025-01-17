from sentence_transformers import SentenceTransformer

def load_model(model_name: str):
    model = SentenceTransformer(model_name)
    return model
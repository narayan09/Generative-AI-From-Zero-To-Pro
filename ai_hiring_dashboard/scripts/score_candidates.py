from sentence_transformers import SentenceTransformer, util # type: ignore

model = SentenceTransformer('all-MiniLM-L6-v2')

role_requirements = "Python, Machine Learning, NLP, AI, Data Analysis"

def score_candidate(candidate_text):
    embedding1 = model.encode(role_requirements, convert_to_tensor=True)
    embedding2 = model.encode(candidate_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return float(similarity[0][0])

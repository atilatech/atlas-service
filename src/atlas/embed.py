from sentence_transformers import SentenceTransformer
import pinecone
from tqdm import tqdm

from atlas.utils import parse_video_id
from config import PINECONE_API_KEY
from functools import lru_cache

sentence_transformer_model_model_id = "multi-qa-mpnet-base-dot-v1"
pinecone_index_id = "youtube-search"
batch_size = 64

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment="us-west1-gcp"
)

pinecone_index = pinecone.Index(pinecone_index_id)


@lru_cache
def get_sentence_transformer_model(model_id: str = sentence_transformer_model_model_id) -> SentenceTransformer:
    return SentenceTransformer(model_id)


def initialize_pinecone_index():
    dimensions = get_sentence_transformer_model().get_sentence_embedding_dimension()
    if pinecone_index_id not in pinecone.list_indexes():
        pinecone.create_index(
            pinecone_index_id,
            dimensions,
            metric="dotproduct"
        )


def does_video_exist(video_url):
    # create a placeholder vector of zeros to see if any vectors with the
    # given video_id match.
    video_id = parse_video_id(video_url)
    dimension = pinecone_index.describe_index_stats()['dimension']
    query_response = pinecone_index.query(
        top_k=1,
        vector=[0] * dimension,
        filter={
            "video_id": {"$eq": video_id}
        }
    )
    return len(query_response['matches']) > 0


def upload_transcripts_to_vector_db(transcripts_for_upload):
    # loop through in batches of 64
    for i in tqdm(range(0, len(transcripts_for_upload), batch_size)):
        # find end position of batch (for when we hit end of data)
        i_end = min(len(transcripts_for_upload) - 1, i + batch_size)
        # extract the metadata like text, start/end positions, etc
        batch_meta = [{
            **transcripts_for_upload[x]
        } for x in range(i, i_end)]
        # extract only text to be encoded by embedding model
        batch_text = [
            row['text'] for row in transcripts_for_upload[i:i_end]
        ]
        # create the embedding vectors
        batch_embeds = get_sentence_transformer_model().encode(batch_text).tolist()
        # extract IDs to be attached to each embedding and metadata
        batch_ids = [
            row['id'] for row in transcripts_for_upload[i:i_end]
        ]
        # 'upsert' (insert) IDs, embeddings, and metadata to index
        to_upsert = list(zip(
            batch_ids, batch_embeds, batch_meta
        ))
        pinecone_index.upsert(to_upsert)
        print(f'Uploaded Batches: {i} to {i_end}')


def query_model(query, video_id=""):
    encoded_query = get_sentence_transformer_model().encode(query).tolist()
    metadata_filter = {"video_id": {"$eq": video_id}} if video_id else None
    return pinecone_index.query(encoded_query, top_k=5,
                                include_metadata=True,
                                filter=metadata_filter)

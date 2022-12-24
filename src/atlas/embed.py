from sentence_transformers import SentenceTransformer
import pinecone
from tqdm import tqdm

from atlas.utils import parse_video_id
from config import PINECONE_API_KEY

model_id = "multi-qa-mpnet-base-dot-v1"

sentence_transformer_model = SentenceTransformer(model_id)
dimensions = sentence_transformer_model.get_sentence_embedding_dimension()

index_id = "youtube-search"

pinecone.init(
    api_key=PINECONE_API_KEY,
    environment="us-west1-gcp"
)

if index_id not in pinecone.list_indexes():
    pinecone.create_index(
        index_id,
        dimensions,
        metric="dotproduct"
    )

pinecone_index = pinecone.Index(index_id)
pinecone_index.describe_index_stats()

batch_size = 64


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
        batch_embeds = sentence_transformer_model.encode(batch_text).tolist()
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
    encoded_query = sentence_transformer_model.encode(query).tolist()
    metadata_filter = {"video_id": {"$eq": video_id}} if video_id else None
    return pinecone_index.query(encoded_query, top_k=5,
                                include_metadata=True,
                                filter=metadata_filter)

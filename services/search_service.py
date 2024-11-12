from concurrent.futures import ThreadPoolExecutor, as_completed
import constants
from google.cloud import aiplatform
from vertexai.language_models import TextEmbeddingModel
from constants import AssetTypes

from services.metadata_service import MetadataService

class SearchService:

    
    def __init__(self, search_deployed_index_id:str = constants.SEARCH_DEPLOYED_INDEX_ID, 
                 search_endpoint_id:str = constants.SEARCH_ENDPOINT_ID,
                 embedding_model: str = constants.EMBEDDING_MODEL):
        """Initializes Search Service

        Args:
            search_index_id: (optional) The id of the search index in vector search
            search_endpoint_id: (optional) The id of the search endpoint in vector search
        """
        # get index
        self.search_deployed_index_id = search_deployed_index_id
        
        #init vertex
        aiplatform.init(project=constants.PROJECT_ID, location=constants.LOCATION)
        
        # get the endpoint from vector search
        self.index_endpoint = aiplatform.MatchingEngineIndexEndpoint(search_endpoint_id)
        #init the embedding model 
        self.model = TextEmbeddingModel.from_pretrained(embedding_model)

         


    def generate_embedding(self):
        docs = self.db.collection(self.collection_name).stream()
        #convert objects 
        docs = [doc.to_dict() for doc in docs]
        return list(docs)
    
    def get_document_by_key(self, key: str):
        doc = self.db.collection(self.collection_name).document(key).get()
        return doc
    
    def get_metadata_with_index(self, idx, neighbor):
        # This is a helper function to keep the index with the metadata
        metadata = self.get_metadata(neighbor.id)
        return idx, neighbor, metadata

    def search(self, query):
        query_embeddings = self.generate_embedding(query)

        response = self.index_endpoint.find_neighbors(
            deployed_index_id=self.search_deployed_index_id,
            queries=[query_embeddings],
            num_neighbors=15
        )

        search_results = []

        with ThreadPoolExecutor() as executor:
            futures = []
            for idx, neighbor in enumerate(response[0]):
                futures.append(executor.submit(self.get_metadata_with_index, idx, neighbor))

            for future in as_completed(futures):
                try:
                    idx, neighbor, metadata = future.result() 
                    search_results.append({
                        'id': idx,
                        'similarity': f"{neighbor.distance:.2f}",
                        'media_id': neighbor.id,
                        'asset_type' :f"{self.get_asset_type_from_id(neighbor.id)}",
                        'metadata': metadata
                    })
                except Exception as e:
                    print(f"Error getting metadata for {neighbor.id}: {e}")

        return {
            'count': len(search_results),
            'search_results': search_results
        }
  
    def get_document_by_id(self, asset_type, id):
        metadata_service = None
        if asset_type == AssetTypes.AUDIO.value:
            metadata_service = MetadataService(collection_name = constants.AUDIO_FIRESTORE_DATABASE)
        elif asset_type == AssetTypes.IMAGE.value:
            metadata_service =  MetadataService(collection_name = constants.IMAGE_FIRESTORE_DATABASE)
        elif asset_type == AssetTypes.ARTICLE.value:
            metadata_service =  MetadataService(collection_name = constants.ARTICLE_FIRESTORE_DATABASE)
        elif asset_type == AssetTypes.VIDEO.value:
            metadata_service =  MetadataService(collection_name = constants.VIDEO_FIRESTORE_DATABASE)
        
        result = metadata_service.get_document_by_key(id)
        
        return result
    
    def get_asset_type_from_id(self, id):
        tokens = id.split(':')
        return tokens[0] if len(tokens) <= 2 else AssetTypes.SEGMENT.value
    
    def get_metadata(self, id):
        tokens = id.split(':')
        asset_type = tokens[0]
        asset_id = tokens[1] if len(tokens) <= 2 else tokens[2]    
        document = self.get_document_by_id(asset_type=asset_type, id=asset_id)
        return document if document != None else None
        
    def generate_embedding(self, text):
        return self.model.get_embeddings([text])[0].values


import constants
from google.cloud import firestore

class MetadataService:
    def __init__(self, collection_name: str = constants.VIDEO_FIRESTORE_DATABASE):
        """Initializes MetadataService with a Firestore collection.

        Args:
            collection_name: (optional) The name of the Firestore collection to use. 
                             If None, defaults to the value of FIRESTORE_DATABASE.
        """
        self.db = firestore.Client(project=constants.PROJECT_ID)

        self.collection_name = collection_name


    def list_all_documents(self):
        docs = self.db.collection(self.collection_name).stream()
        #convert objects 
        docs = [doc.to_dict() for doc in docs]
        return list(docs)
    
    def get_document_by_key(self, key: str):
        doc = self.db.collection(self.collection_name).document(key).get()
        return doc

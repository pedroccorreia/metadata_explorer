from google.cloud import storage
import datetime

class StorageService(): 

    def __init__(self, buckets, service_account_key_file, session_duration_minutes=5):
        """
        Initializes StorageService with a list of bucket names, service account key file, 
        and session duration. Generates signed URLs for all objects within the specified 
        GCS buckets upon initialization.
        """

        self.storage_client = storage.Client.from_service_account_json(service_account_key_file)
        self.buckets = [self.storage_client.bucket(bucket_name) for bucket_name in buckets]
        self.session_duration_minutes = session_duration_minutes
        self.signed_urls = {}
        self.generate_signed_urls_for_buckets()

    def generate_signed_urls_for_buckets(self):
        """
        Generates signed URLs for all objects within the specified GCS buckets.
        """

        for bucket in self.buckets:
            blobs = bucket.list_blobs()
            for blob in blobs:
                try:
                    expiration_time = datetime.timedelta(minutes=self.session_duration_minutes)
                    signed_url = blob.generate_signed_url(
                        version="v4",
                        expiration=expiration_time,
                        method="GET"
                    )
                    self.signed_urls[blob.name] = signed_url
                except Exception as e:
                    print(f"Error generating signed URL for {blob.name}: {e}")

        return self.signed_urls

    @property
    def signed_urls(self):
        """Getter for signed_urls."""
        return self._signed_urls

    @signed_urls.setter
    def signed_urls(self, value):
        """Setter for signed_urls."""
        self._signed_urls = value

    def get_signed_url(self, object_name):
        return self.signed_urls[object_name]
    

#TODO: Move additional methods here as statics ones instead of the utils file

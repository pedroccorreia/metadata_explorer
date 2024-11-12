
import threading
import json
import time
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import vertexai.preview.generative_models as generative_models

import constants


class ContentAssistanceService():

    def __init__(self,project_id:str = constants.PROJECT_ID, location:str = constants.LOCATION, generation_model:str = constants.CREATION_MODEL):
        self.vertexai = vertexai.init(project=project_id, location=location) 
        self.model =  GenerativeModel(generation_model)


    def sleep_thread(self):
        time.sleep(5)  # Sleep for X seconds
        

    def get_article_summary (self, article):
        # Generate content
        responses = self.model.generate_content(
            f"""You are a content creation assistant. 
        You provide information for journalists to get the information they need from articles. 

        Summary the following [news_content] into three bullet points.

        [news_content]:
        {article}""",

            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread

        return responses.candidates[0].text
    

    def get_keyword_summary(self,article):
        responses = self.model.generate_content(
            f"""
            You are a content creation assistant. 
            You provide information for journalists to get the information they need from articles. 

            generate the most relevant keywords to classify the [news_content].
            
            output the result in the following  format: keyword1,keyword2, keyword3
                
            

            [news_content]:{article}""",
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False
            ,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread
        response = responses.candidates[0].text
        keywords = response.split(",")
        
        print(keywords)
        
        return keywords
    

    def create_podcast_content(self, podcast_info, sources):
        responses = self.model.generate_content(
            f"""
            You are a content creation assistant. 
            You are creating an article. 
            
            Generate an [article] for a the following [news_sources].
            [article] should be weaving all stories together. 

            The script should follow the description of the podcast as per this [podcast_info].
            The tone and the writing style follow [podcast_info]. 
            The script uses the tagline from [podcast_info].
            The script introduces the podcast hosts from [podcast_info].

            [podcast_info]:{podcast_info}

            [news_sources]:{sources}""",
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False
            ,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread

        return responses.candidates[0].text
    
    def create_newsletter_content(self, reader_profile, sources):
        responses = self.model.generate_content(
            f"""
            You are a content creation assistant. 
            You are creating a newsletter that summarizes the content that you are given. 
            
            Generate an [newsletter] for a the following [news_sources].

            Tailor the tone and writing style to cater for the reader's profile as stated in [reader_profile]

            Output is an HTML file. The newspaper is called Editorial Solaris. The journalist that is reponsible for the newsletter is called Stevie Nicks.

            [newsletter] follows the following structure: 
            - Greeting
            - two paragraph summary of the newsletter
            - The summary of stories weaved into a narrative, pointing out the things that matter to the [reader_profile]. Each summary has a link at a keyword to point the reader
            - asking users to subscribe and providing url to it.

            -Apply no styling to the html.
            
            [reader_profile]:{reader_profile}

            [news_sources]:{sources}""",
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False
            ,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread

        return responses.candidates[0].text
    
    def translate(self, content):
        responses = self.model.generate_content(
            f"""
            Translate  an [article] into brazilian portuguese.
            

            [article]:{content}""",
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False
            ,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread

        return responses.candidates[0].text
    

    def contextualize(self, content):
        responses = self.model.generate_content(
            f"""
            Transform an [article] so that it's understood by school aged kids. 
            Where possible provide context to what are the entities or concepts involved. 

            [article]:{content}""",
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1
            },
            safety_settings={
                generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
                generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            },
            stream=False
            ,
        )

        thread = threading.Thread(target=self.sleep_thread)
        thread.start()  # Start the thread

        return responses.candidates[0].text
        
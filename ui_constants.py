# Flag for the page type being used in the video page
MEDIA_VIEW_TYPE = "media_view"
# Types that are used for the MEDIA_VIEW_TYPE property
MEDIA_VIEW_LIST = "media_view_list"
MEDIA_VIEW_ITEM_SEGMENT = "media_item_segment"
MEDIA_VIEW_ITEM = "media_view_item"

#Session Constants
# contains the media item that is currently being explored in detail (i,e: looking at a key moment of a video)
MEDIA_ITEM_CHOSEN = "media_item_chosen"
# Boolean flag to inform if a there is an item being explored in detail
MEDIA_ITEM_SEGMENT_CHOSEN = "media_item_segment_chosen"
# Index of the Item Chosen
MEDIA_ITEM_INDEX_CHOSEN = "media_item_index_chosen"
# Number of section on item chosen
MEDIA_ITEM_SECTIONS_LENGTH = "media_item_sections_length"


#Launchpad Control
LAUNCHPAD_ITEMS = "launchpad_items"

# Experience Options
CREATE_PODCAST_OPTION = "Podcast"
CREATE_NEWSLETTER_OPTION = "Newsletter"
# Array with options
CREATE_OPTIONS= [CREATE_PODCAST_OPTION, CREATE_NEWSLETTER_OPTION]
# Key for chosen option
CREATE_CHOSEN_OPTION = "create_chosen_option"
# KEy for the status of experience creation
CREATE_STATUS_KEY = "create_status"



# Search Status
SEARCH_STATUS_KEY = "search_status"
SEARCH_TERM = "search_term"
SEARCH_RESULTS = "search_results"


class SearchStatus():
    INIT = 0
    RESULTS = 1


class CreateContentStatus():
    INIT = 0, 
    PODCAST_OPTIONS = 1,
    PODCAST_CREATE = 2,
    NEWSLETTER_OPTIONS = 3,
    NEWSLETTER_CREATE = 4

#Service definitions
SERVICE_STORAGE = "service_storage"


PODCAST_CHOSEN = "podcast_chosen"
PERSONA_CHOSEN = "persona_chosen"


# Class to hold all static information used throughout the demo


class DemoService():

    def __init__(self):
        self.podcasts =[
            {
                'podcast_name' : 'The Spin 🐨',
                'podcast_tagline' : """
                To empower readers with clear, unbiased information about budgets and politics, to foster a more informed, engaged citizenry that holds politicians accountable for the impacts of their decisions.
                """,
                'hosts' : [
                     {'host_name' : 'Ed Mutiah', 'role':'host'},
                     {'host_name' : 'Pedro Correia', 'role':'Analyst'}
                ],
                'writing_style' : 'Straight to the point, data focused. They often like to use quotes from the different people in the story',
                'podcast_logo' : 'media/podcast/beyond_the_spin.png'
           },{
                'podcast_name' : 'Solaris Daily 🚀',
                'podcast_tagline' : """Changing the way you get your daily news.""",
                'hosts' : [
                     {'host_name' : 'Julie Hensen', 'role':'News Reporter'},
                ],
                'writing_style' : 'Typical news reporter style. Wrapping up the daily news in a summarized way, briding stories together into a cohesive deliver. Always finishes with the weather and ask for people to follow the podcast',
                'podcast_logo' : 'media/logo.jpeg'
           },{
                'podcast_name' : 'N4Y 🧑🏽‍🏫',
                'podcast_tagline' : """News 4 you. All the news for you. whenever you can be bothered.""",
                'hosts' : [
                     {'host_name' : 'Jay Jay', 'role':'host'},
                ],
                'writing_style' : 'Focus in school age kids. Simple language that uses analogies to breakdown complex topics into understandable digestable items. Jay Jay likes to start with the tagline of the show.',
                'podcast_logo' : 'media/podcast/n4y_logo.png'
           }
        ]

        self.personas = [
            {
                'name' : 'Persona A',
                'values' : [
                        {'value' : 'Woman representation' },
                        {'value' :'Attribution in the workplace'},
                        {'value' :'Inspiring stories of overcoming challenges'},
                        {'value' :'Technology adoption'}
                ],
                'concerns' : [
                        {'concern' : 'Negative impact on tech'},
                        {'concern' : 'Economic downturns'}
                ]
            },            {
                'name' : 'Persona B',
                'values' : [
                        {'value' : 'Economic growth' },
                        {'value' :'Tech Adoption'},
                        {'value' :'Tech progress'},
                        {'value' :'Sports'}

                ],
                'concerns' : [
                        {'concern' : 'Hardships'},
                        {'concern' : 'Wars'}
                ]
            }
        ]

    def get_podcasts(self): 
        return self.podcasts
    
    def get_podcasts_names(self):
        names = []
        for podcast in self.podcasts:
            names.append(podcast['podcast_name'])
        return names
    
    def get_podcast_by_name(self, name):
        for podcast in self.podcasts:
            if podcast['podcast_name'] == name:
                return podcast
        return None
    
    def get_personas(self):
        return self.personas
    
    def get_persona_by_name(self, name):
        for persona in self.personas:
            if persona['name'] == name:
                return persona
        return None
    
    def get_personas_names(self):
        names = []
        for persona in self.personas:
            names.append(persona['name'])
        return names
    

#Lauren Murphy

#Final Project for SI 106.

#import statements
import requests
import json
import requests_oauthlib
import test106 as test

#Instagram information necessary to run API
access_token = "1834570599.1fb234f.ae127d266d114277b8340c3a26eac2b5"
client_id = 'a84c4e894993489f8d7edcf30fd6e52a'
client_secret = 'a58e94df9347ec19945a4c03cd5d020'
 
#flickr information necessary to run API  
flickr_key = "01fab8a5716b2b52e211eee28314cbb6"

#class Game_play is now made here
class Game_play():
    """Objects representing the things needed to play game"""
    def __init__(self, category = 'nature', health = 1, max_health = 5, user_len = 1, flickr_dict = {}, flickr_list = [], instagram_list = []):
        self.health = health
        self.max_h = max_health
        self.category = category
        self.length = user_len
        self.length_full = user_len + 1 
        self.f_dict = flickr_dict
        self.f_list = flickr_list
        self.i_list = instagram_list
        
    def game_progress(self):
        if self.health > 0:
            return False
        else:
            return True
        
    def tries_left(self):
        return (self.max_h - self.health)
        
    def playing(self):
        print "Here is an example of the Instagram results.  Keep in mind that the users of Flicker are different from users of Instagram."
        print "The first few examples of Instagram tags are:"
        for item in self.i_list[1:self.length_full]:
            print item
        self.health = self.max_h
        print "your max health is", self.max_h
        guesses_so_far = []
        correct_guesses = 0
        self.game_progress()

        while self.game_progress() != True:
            next_guess = str(raw_input("What is your guess? "))
            if next_guess in guesses_so_far:
                print "You've already guessed that, try again"
            else:
                guesses_so_far.append(next_guess)
                if next_guess in self.f_list[1:self.length_full]:
                    print "It's on there!", self.f_dict[next_guess], "other people tagged", next_guess
                    correct_guesses = correct_guesses + 1
                    if (correct_guesses == self.length):
                        feedback = "You've guessed them all!"
                        self.health = 0
                else:
                    print "Sorry, that's not one of them, try again."
                    self.health = self.health - 1
                    print "X"*(self.tries_left())
                    if self.game_progress() == True:
                        feedback = "Sorry, game over."
                        game_over = True
                    
        print(feedback)
        print "Top", self.length, "tags in that category for Flickr were:"
        for item in self.f_list[1:self.length_full]:
            print item

#Start of definitions for retrieving API information
def flickr_API(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.search',
    api_key = flickr_key,
    format = 'json',
    extra_params={}):
    d = {}
    d['method'] = method
    d['api_key'] = api_key
    d['format'] = format
    for k in extra_params:
        d[k] = extra_params[k]
    return requests.get(baseurl, params = d)
    
def flickr_photo_Info(baseurl = 'https://api.flickr.com/services/rest/',
    method = 'flickr.photos.getInfo',
    api_key = flickr_key,
    format = 'json',
    id = 0):
    d = {}
    d['method'] = method
    d['format'] = format
    d['api_key'] = api_key
    d['photo_id'] = id
    return requests.get(baseurl, params = d)
    
def fix_resp(flickr_string):
	return flickr_string[len("jsonFlickrApi("):-1]
	
test.testEqual(type(fix_resp("")), type(""))
	
def tags_2_dicts(list_of_tags):
    dict_tags = {}
    for tag in list_of_tags:
        if tag not in dict_tags:
            dict_tags[tag] = 0
        dict_tags[tag] = dict_tags[tag] + 1
    if len(dict_tags) > 0:
        return dict_tags

test.testEqual(tags_2_dicts(['nature', 'travel', 'nature', 'nature', 'architecture', 'vacations', 'travel']), {'nature': 3, 'travel': 2, 'architecture': 1, 'vacations': 1})

def tag_sort(dict_of_tags):
    return sorted(dict_of_tags, key = lambda x: dict_of_tags[x], reverse = True)
    
test.testEqual(tag_sort({'beautiful': 9, 'houses': 3, 'mushrooms': 5}), ['beautiful', 'mushrooms', 'houses'])
test.testEqual(type(tag_sort({})), type([]))

#end of definitions
#ask the user to get a tag	
user_tags = str(raw_input("What tag would you like to play family feud with? "))

print "In Flickr and Instagram, users are able to tag content with multiple tags. For this family feud, you will be using the tag you have chosen as a category, and will be provided with a list of the top tags from Instagram that are associated with your chosen tag. You will be asked to guess the most common tags in Flicker that are associated with the same tag you chose."

user_len_results = int(raw_input("How many tags in this category would you like to guess? (ex. 5) "))
print "This may take a moment."

#beginning of instagram retrieval section
oauth = requests_oauthlib.OAuth1Session(client_id, client_secret=client_secret)
d = {"access_token": access_token, "min_id": 0}
results = oauth.get("https://api.instagram.com/v1/tags/%s/media/recent/?" % (user_tags), params=d )
insta_results = results.json()

#an if statement that checks if the results equal 400, which is an error. If it is an error, the user is informed and asked to provide another 
if insta_results['meta']['code'] == 400:
    print "Sorry, there was an error with your tag request, please try another tag."
    user_tags = str(raw_input("What tag would you like to play family feud with? "))
    oauth = requests_oauthlib.OAuth1Session(client_id, client_secret=client_secret)
    d = {"access_token": access_token, "max_id": 20, "min_id": 0} #may need to take out the max_id key value pair if run before June 2016, otherwise you're stuck in sandbox mode, and you're not able to use this anymore lol sandbox mode
    results = oauth.get("https://api.instagram.com/v1/tags/%s/media/recent/?" % (user_tags), params=d )
    insta_results = results.json()

#retrieve tags and sort them for the most common
insta_tags = []
print insta_results
for pic in insta_results['data']:
    for tag in pic['tags']:
        insta_tags.append(tag)

insta_dict = tags_2_dicts(insta_tags)
insta_sort = tag_sort(insta_dict)

#Beginning of the Flickr section
#change the response from Flickr so that it is usable by python with json.loads()
user_requ = flickr_API(extra_params = {'tags':user_tags, 'per_page':100})
flickr_info = json.loads(fix_resp(user_requ.text))

#retrieve the flickr ids from the photos
photo_ids = []
for pos in flickr_info['photos']['photo']:
    photo_ids.append(pos['id'])

#call to each photo id and retrieve the information from each, putting it in Info_of_pics
Info_of_pics = map(lambda photo_id: json.loads(fix_resp(flickr_photo_Info(id = photo_id).text)), photo_ids)

#create the dictionaries and sort the results so that you have the most common tags
flickr_tags = []

for itera in Info_of_pics:
    for tag in itera['photo']['tags']['tag']:
        flickr_tags.append(tag['raw'])

flickr_dict = tags_2_dicts(flickr_tags)     
flickr_sort = tag_sort(flickr_dict)
#end of Flickr Retrieval Section

# Now for the game play
a = Game_play(category = user_tags, user_len = user_len_results, flickr_dict = flickr_dict, flickr_list = flickr_sort, instagram_list = insta_sort)
a.playing()
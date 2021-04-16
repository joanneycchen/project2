#################################
##### Name: Joanne
##### Uniqname: joanneyc
#################################

from bs4 import BeautifulSoup
import requests
import json
import time
import secrets  # file that contains your API key

BASE_URL = 'https://www.nps.gov'
CACHE_FILE_NAME = 'national_park.json'
CACHE_DICT = {}
headers = {'User-Agent': 'python-requests/2.25.0', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'}
API_KEY = secrets.API_KEY







class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        '''
        intialize the intance variables

        Parameters
        ----------        
        Instance variables: category, name, address, zipcode, phone

        Returns
        -------
        None
        '''
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone

 
    def info(self):
        '''
        print out informatin about national site 

        Parameters
        ----------        
        self

        Returns
        -------
        a string of the format  <name>(<category>):<address><zip>.
        '''
   
        return f"{self.name} ({self.category}): {self.address} {self.zipcode}"


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''


    BASE_URL = 'https://www.nps.gov'
    COURSES_PATH = '/index.htm'
    courses_page_url = BASE_URL + COURSES_PATH
    response = requests.get(courses_page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    state_listing_parent = soup.find('div', class_='col-sm-12 col-md-10 col-md-push-1')
    state_listing_divs = state_listing_parent.find('div', recursive=False)

    all_state = state_listing_divs.find_all('li')

    state_dic = {}
    for every_state in all_state:
   
        every_state_name = every_state.find('a')

        every_state_name_url = every_state_name['href']
        state_details_url = BASE_URL + every_state_name_url


        state_dic[every_state_name.text.strip().lower()] = state_details_url

    return state_dic
def load_cache():
    ''' opens the cache file if it exists and loads the JSON into the FIB_CACHE dictionary.    
    if the cache file doesn't exist, creates a new cache dictionary    
    Parameters    
    ----------    
    None    
    Returns   
     -------    
     The opened cache
   
    '''
    try:
        cache_file = open(CACHE_FILE_NAME, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache: dict
    The dictionary to save
    Returns
    -------
    None
    '''
    cache_file = open(CACHE_FILE_NAME, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()


def make_url_request_using_cache(url, cache):
    ''' 
    check if the url is in the cache, if there is cache, use cache
    if there is no cache,  fetch the data

    Parameters
    ----------
    url
    cache: dict

    Returns
    -------
    cache dic
    '''
    if (url in cache.keys()): # the url is our unique key
        print("Using cache")
        return cache[url] # return the dic key
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(url, headers=headers)
        cache[url] = response.text
        save_cache(cache)
        return cache[url]

def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''
    np_page_url = site_url
    CACHE_DICT = load_cache()
    responseDetail = make_url_request_using_cache(np_page_url, CACHE_DICT)
    soup = BeautifulSoup(responseDetail, 'html.parser')
  
    # np_page_url = site_url
    # response = requests.get(np_page_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # For each course listed

    np_listing_parent = soup.find('div', class_='Hero-titleContainer clearfix')
    
    np_footer = soup.find('div', class_='ParkFooter-contact')
    try: 
        category = np_listing_parent.find(class_='Hero-designationContainer').find('span').text.strip()
    except:
        category = "no category"
    try:
        name = np_listing_parent.find('a').text.strip()
    except:
        name = "no name"
    try:
        city_name = np_footer.find('span', itemprop='addressLocality').text.strip()
    except:
        city_name = "no city"
    try:
        state_name = np_footer.find('span', class_='region').text.strip()
    except:
        state_name = "no state"
    try:
        zipcode = np_footer.find('span', class_='postal-code').text.strip()
    except:
        zipcode = "no zipcode"
    try:
        phone = np_footer.find('span', class_='tel').text.strip()
    except:
        phone = "no phone"
    try:
        address = f"{city_name}, {state_name}"
    except:
        address = "no address"

    return NationalSite(category, name, address, zipcode, phone)






def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances

    '''
    CACHE_DICT = load_cache()
    responseDetail = make_url_request_using_cache(state_url, CACHE_DICT)
    soup = BeautifulSoup(responseDetail, 'html.parser')

    each_np_divs = soup.find_all('div', class_='col-md-9 col-sm-9 col-xs-12 table-cell list_left')
  
    list_national_site =[]
    for each_np_div in each_np_divs:
        np_link_tag = each_np_div.find('a')
        course_details_path = np_link_tag['href']
        individual_path_page_url = BASE_URL+course_details_path+"index.htm"
     
        national_site = get_site_instance(individual_path_page_url)
      
        list_national_site.append(national_site)
    return list_national_site




def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''


    key = API_KEY
    origin = site_object.zipcode
    radius = 10
    maxMatches = 10
    ambiguities = 'ignore'
    outFormat = 'json'
    baseurl = 'http://www.mapquestapi.com/search/v2/radius'
    suburl = f'?key={key}&maxMatches={maxMatches}&origin={origin}&radius={radius}&ambiguities={ambiguities}&outFormat={outFormat}'
    whole_url = baseurl + suburl
    if (whole_url in CACHE_DICT.keys()): # the url is our unique key
        print("Using cache")
        return CACHE_DICT[whole_url] # return the dic key
    else:
        print("Fetching")
        time.sleep(1)
        response = requests.get(whole_url, headers=headers)
        CACHE_DICT[whole_url] = response.json()
        save_cache(CACHE_DICT)

      
        return CACHE_DICT[whole_url]


   
def print_map(result):
    '''print MapQuest result
    
    Parameters
    ----------
    result: json
        the json file from MapQuest API.

    Returns
    -------
    Ｎone
    '''
 
    
    all_the_results = result['searchResults']
    number = 0
    for result in all_the_results:
        number+=1
        name = result['name']
        category = result['fields']['group_sic_code_name']
        address = result['fields']['address']
        city = result['fields']['city']
        if name == None or name =="":
            name = 'no name'
        if category == None or category == "":
            category = 'no category'
        if city == None or city == "":
            city = 'no city'
        if address == None or address == "":
            address = 'no address'

        value_of_dic = f"-{name} ({category}): {address}, {city}"
        print(value_of_dic)

if __name__ == "__main__":
    all_the_states = build_state_url_dict()
    while True:
        state_name = input('Enter a state name (e.g. Michigan, michigan) or "exit" ')
     
        if state_name.lower()=='exit':
            quit()
        elif state_name.lower() not in all_the_states.keys():
            print('[Error] Enter proper state name ')
            pass
     
        else:
            answer = ""
            number = 0
            print('---------------------------------')
            print(f"List of national sites in {state_name.lower()}")
            print('---------------------------------')
            state = state_name.lower()
            state_url = all_the_states[state]
            sites = get_sites_for_state(state_url)
            len_sites = len(sites)
            for site in sites:
                number+=1
                each_site =  f"[{number}] {site.info()}"
                print(each_site)
                national_site = site.name
            while answer != 'exit' or answer != 'back':
                answer = input('Choose a number for detail search or "exit" or "back" ')
                if answer.isnumeric() and 1 <= int(answer) <= len(sites):
                    i = int(answer)-1
                    info = get_nearby_places(sites[i])
                    national_site = sites[i].name
                    print('---------------------------------')
                    print(f'Places near {national_site}')
                    print('---------------------------------')
                    print_map(info)
                elif answer == 'exit':
                    exit()
                elif answer.isnumeric() and 1 > int(answer):
                    print('[Error] Invalid input')
                elif answer.lower()!='back':
                    print('[Error] Invalid input')
                else:
                    answer = 'back'
                    print(answer)
                    break
        
                
         
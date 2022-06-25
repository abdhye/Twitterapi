from django.shortcuts import render
import base64
import requests


# twitter key
client_key = 'IvuHTgI2LbEqjlgyXAmlDIaCa'

# twitter secret key
client_secret = 'sQWxx4bfauH9lLnbGvccTfp2qy7n8wSxnlmnrD8iXZHg0rUCKk'

# twitter token
bearer_token = 'Bearer AAAAAAAAAAAAAAAAAAAAAAHQUQEAAAAATWYwAfmn%2FyM%2BtCJ5NAwvYkM3srU%3DOA6IYc1ELaa5kO9bJPYUh0njEhmSPIRIf5eld21Cdd5qXvB3H2'

base_url = 'https://api.twitter.com/'
search_url = base_url+'1.1/search/tweets.json'
status_code = 'status_code'

# encode your keys
key_secret = '{}:{}'.format(client_key, client_secret).encode('ascii')

# use base64 to encode the keys to binary
b64_encoded_key = base64.b64encode(key_secret)

# convert to ascii
b64_encoded_key = b64_encoded_key.decode('ascii')

auth_endpoint = base_url+'oauth2/token'
auth_headers = {'Authorization': 'Basic {}'.format(b64_encoded_key),
                'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
auth_data = {'grant_type': 'client_credentials'}

# Post Request
response = requests.post(
    auth_endpoint, headers=auth_headers, data=auth_data)
json_data = response.json()
'''
    {'token_type': 'bearer',
    'access_token': 'your token will be here'}
    '''
access_token = json_data['access_token']
search_headers = {'Authorization': bearer_token.format(access_token)
                  }


# marvel key
public_key = 'cda256b8123954a75977b71bcfab69af'
md5 = 'd3736871d46d778a01b289b7efe6fad9'

# marvel api url
marvel_char_url = f'https://gateway.marvel.com/v1/public/characters?ts=1&apikey={public_key}&hash={md5}'
marvel_comics_url = f'https://gateway.marvel.com/v1/public/comics?ts=1&apikey={public_key}&hash={md5}'


def home(request):
    return render(request, 'home.html')


def twitter(request):
    parameters = {'q': 'football',
                  'result_type': 'popular',
                  'count': 20}

    response = requests.get(
        search_url, headers=search_headers, params=parameters)

    tweet = response.json()

    return render(request, 'twitter_cover.html', {'stat_data': tweet['statuses']})


def search_twt(request):
    if request.method == "POST":
        searched = request.POST['searched']
        if searched == '':
            return render(request, 'ifnot_searched.html')

        twtcount = request.POST.get('twtcount', False)

        filter = request.POST['filter']

        parameters = {'q': searched,
                      'result_type': filter,
                      'count': twtcount}

        response = requests.get(
            search_url, headers=search_headers, params=parameters)
        tweet = response.json()

        return render(request, 'twitter_searched.html', {'searched': searched, 'data': tweet['statuses']})

    else:
        return render(request, 'twitter_cover.html')


def marvel(request):
    return render(request, 'marvel_cover.html')


def mar_chars(request):
    response = requests.get(marvel_char_url)
    data = []
    char_name = []
    marvel = response.json()
    for item in marvel['data']['results']:
        mar = item
        mar['names'] = []
        for series in item['series']['items']:
            mar['names'].append(series)
            if len(mar['names']) > 4:
                break
        data.append(mar)

    return render(request, 'marvel_chars.html', {'data': data})


def mar_comics(request):
    response = requests.get(marvel_comics_url)
    marvel = response.json()
    return render(request, 'marvel_comics.html', {'data': marvel['data']['results']})

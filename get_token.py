
import requests

def get_token(base_url, clientID, clientSecret):
    print(f"get_token(): base_url={base_url},  clientID={clientID},  clientSecret={clientSecret}")

    # headers = {'clientID': clientID , 'clientSecret': str(clientSecret)}
    headers = {'client_id': clientID , 'client_secret': clientSecret}
    print(f"get_token(): headers={headers}")
    url = base_url+"/auth/token"
    try:
        # search_all_events
        response = requests.get(url, headers=headers)
        print(f"get_token(): response.json={response.json()}")
    except requests.exceptions.RequestException as e:
        print("Exception when calling get_token(): %s\n" % e)
        return None

    return response
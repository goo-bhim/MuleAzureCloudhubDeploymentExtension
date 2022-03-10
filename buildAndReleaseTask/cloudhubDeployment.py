import requests # To send HTTP requests
import requests.exceptions
import json # To handle deployment metadata
import os # To handle file operations
import sys # To read additional properties from command line
import ast # To parse and format additional properties
from distutils.version import StrictVersion # To compare Mule Runtime versions


print(os.getcwd())

# Set up input variables
artifact_drop_path = os.environ['artifact_drop_path']
cloudhub_user = os.environ['cloudhub_user']
cloudhub_pass = os.environ['cloudhub_pass']
org_id = os.environ['org_id']
env_id = os.environ['env_id']
domain_name = os.environ['domain_name']
mule_version = os.environ['mule_version']
region = os.environ['region']
monitoring_enabled = os.environ['monitoring_enabled']
monitoring_auto_restart = os.environ['monitoring_auto_restart']
workers_amount = os.environ['workers_amount']
workers_type_name = os.environ['workers_type_name']
anypoint_platform_client_id = os.environ['anypoint_platform_client_id']
anypoint_platform_client_secret = os.environ['anypoint_platform_client_secret']
cloudhub_environment = os.environ['cloudhub_environment']
security_key = os.environ['security_key']
logging_enabled = os.environ['logging_enabled']
persistent_queues = os.environ['persistent_queues']
object_store_v1 = os.environ['object_store_v1']
domain_name = os.environ['domain_name']

# Retrieve access token in order to use Cloudhub REST API
def oauth_get_token(username, password):

    oauth_url = "https://anypoint.mulesoft.com/accounts/login" 
    response = requests.post(oauth_url,  
            json={'username': username, 'password': password})
    json_obj = json.loads(response.content)
    return json_obj["access_token"] 

# Get the Mule build artifact file extension corresponding to the Runtime version
def get_mule_artifact_extension(mule_version):
    return ".jar" if (StrictVersion(mule_version) >= "4.0.0") else ".zip"

# Find the .jar file in the build directory (to deploy)
def get_file_extension():
    os.chdir(artifact_drop_path)
    for file in os.listdir("."):
        if file.endswith(get_mule_artifact_extension(mule_version)):
            return file



# Deploy an existing application using PUT
def deploy_existing(app_name, multipart_data, headers):
    try:
        response = requests.put(f"https://anypoint.mulesoft.com/cloudhub/api/v2/applications/{app_name}", headers=headers, files=multipart_data) 
        print(f"Status Code: {response.status_code}")
        print(f"Status Message: {response.text}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
        sys.exit(1)
    print("Finished re-deploying existing application!")

# Deploy a new application using POST
def deploy_new(app_name, multipart_data, headers):
    try:
        response = requests.post("https://anypoint.mulesoft.com/cloudhub/api/v2/applications", headers=headers, files=multipart_data)
        print(f"Status Code: {response.status_code}")
        print(f"Status Message: {response.text}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
        sys.exit(1)
    print("Finished deploying new application!")

# Checks to see if the application already exists.  If so, simply update / redeploy the application
def check_for_existing_apps(access_token, env_id, app_name):
    already_deployed = False
    headers = {'Authorization': f'Bearer {access_token}', 'X-ANYPNT-ENV-ID': env_id}

    try:
        response = requests.get("https://anypoint.mulesoft.com/cloudhub/api/v2/applications", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Status Message: {response.text}")
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
        sys.exit(1)

    json_obj = json.loads(response.content)
    
    for apps in json_obj:
        if (app_name == apps['domain']):
            already_deployed = True

    return already_deployed


if __name__ == '__main__':
    # First, get the oauth access token for the Cloudhub REST API
    access_token = oauth_get_token(cloudhub_user, cloudhub_pass)

    raw_properties = sys.argv[1]
    ast_literal = ast.literal_eval(raw_properties)

    # Set headers and multipart data for the deployment PUT / POST request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-ANYPNT-ORG-ID': org_id,
        'X-ANYPNT-ENV-ID': env_id,
        'Cache-Control': 'no-cache',
    }

    # Prepare properties object for OPTIONAL inputs
    properties_dict = {}

    if anypoint_platform_client_id != 'undefined':
        properties_dict['anypoint.platform.client_id'] = anypoint_platform_client_id

    if anypoint_platform_client_secret != 'undefined':
        properties_dict['anypoint.platform.client_secret'] = anypoint_platform_client_secret

    if cloudhub_environment != 'undefined':
        properties_dict['mule.env'] = cloudhub_environment

    if security_key != 'undefined':
        properties_dict['security.key'] = security_key

    app_info_json = {
        'domain': domain_name,
        'muleVersion': {
            'version': mule_version
        },
        'region': region,
        'monitoringEnabled': monitoring_enabled,
        'monitoringAutoRestart': monitoring_auto_restart,
        'workers': {
            'amount': workers_amount,
            'type': {
                'name': workers_type_name
            }
        },
        'properties': properties_dict,
        'loggingNgEnabled': logging_enabled,
        'persistentQueues': persistent_queues,
        'objectStoreV1': object_store_v1
    }

    app_info_json['properties'].update(ast_literal)

    multipart_data = {
        'file': open(f'{get_file_extension()}','rb'),
        'appInfoJson': json.dumps(app_info_json),
        'autoStart': 'true'
    }

    # If the application already exists, update with a PUT request
    # Else, deploy new application with a POST request
    if (check_for_existing_apps(access_token, env_id, domain_name)):
        deploy_existing(domain_name, multipart_data, headers)
    else:
        deploy_new(domain_name, multipart_data, headers)
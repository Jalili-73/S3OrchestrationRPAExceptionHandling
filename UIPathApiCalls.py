import requests
import datetime

class ApiHandler:
  def __init__(self):
    self.GetProcessLIstUrl = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/odata/Processes"
    self.SendMessageToOrchestrationURL = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/odata/Queues/UiPathODataSvc.AddQueueItem"
    self.payload = {}
    self.OrganizationUnitId=4061831
    self.current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    self.tocken = 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlJUTkVOMEl5T1RWQk1UZEVRVEEzUlRZNE16UkJPVU00UVRRM016TXlSalUzUmpnMk4wSTBPQSJ9.eyJodHRwczovL3VpcGF0aC9lbWFpbCI6ImphbGlsaS5oNzNAZ21haWwuY29tIiwiaHR0cHM6Ly91aXBhdGgvZW1haWxfdmVyaWZpZWQiOnRydWUsImlzcyI6Imh0dHBzOi8vYWNjb3VudC51aXBhdGguY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA4NzQ5MjIyMzMzODExNzE0MTkxIiwiYXVkIjpbImh0dHBzOi8vb3JjaGVzdHJhdG9yLmNsb3VkLnVpcGF0aC5jb20iLCJodHRwczovL3VpcGF0aC5ldS5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNjgwNTQ5ODc1LCJleHAiOjE2ODA2MzYyNzUsImF6cCI6IjhERXYxQU1OWGN6VzN5NFUxNUxMM2pZZjYyaks5M241Iiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCBvZmZsaW5lX2FjY2VzcyJ9.VxyPm3shZkuy6wOFDhw-GQqb75ohCFaYlDH1afqIvA0KCjMHgrrj9xmkxlFVUtmnhtCDCd0ta0kYRuuoCmVhgtg4f_FQcJO-ODgCwgXsLoGnp5nXDKwL1NHrnl9ve5MgMNTkGbEJi6Ttw9BnONcgDywBASry4Kj1aN8Y501SVdvhwT7tfb6LkDXEpdI21xX3OslyE2Knypkl8HsOVY369Lf-p7rjCM4mgXU-EZPEwaSlLDmJ2LMt7pOM9mg792wT3B6U4a1Up3mODZa0_kqD3Lx8Nj-5C5w7ckFyToXtjzhFU-VhfFb2weOGOOEo5ONNlCX3XOvD14NGnBJWshBoNQ'
    self.headers = {
      'accept': 'application/json',
      'authorization': self.tocken }
    self.GetfolderLIst = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/tenant/odata"
    self.GetItemsFromUipathQueue = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/QueueItems?$filter=QueueDefinitionId"

  def ProcessLIst(self):
    try:
      print("i am in get process list")
      response = requests.request("GET", self.GetProcessLIstUrl, headers=self.headers, data=self.payload ).text
      return response
    except requests.exceptions.HTTPError as err:
      print("ProcessLIst Request failed with status code: ", response.status_code)
      print("ProcessLIst Error message: ", err)
    except requests.exceptions.RequestException as e:
      print("ProcessLIst Request failed: ", e)

  def SendLogToOrchestration(self,LogMessage):
    LogMessage = LogMessage.replace("\n", "")
    payload = "{\"itemData\": {\"Name\": \"received exception\",\"Priority\": \"High\",\"SpecificContent\": {\"message\" : \"" + LogMessage + "\"},\"DeferDate\": \"" + self.current_time + "\",\"DueDate\": \"" + self.current_time + "\",\"RiskSlaDate\": \"" + self.current_time + "\"}}"
    headers = {
      'accept': 'application/json',
      'X-UIPATH-OrganizationUnitId': '4061831',
      'authorization': self.tocken,
      'Content-Type': 'application/json;odata.metadata=minimal;odata.streaming=true'
    }
    try:
      print (payload)
      response = requests.request("POST", self.SendMessageToOrchestrationURL, headers=headers, data=payload)
      print("i am in get send to orchestrator")
      return response
    except requests.exceptions.HTTPError as err:
      print("SendLogToOrchestration Request failed with status code: ", response.status_code)
      print("SendLogToOrchestration Error message: ", err)
    except requests.exceptions.RequestException as e:
      print("Request failed: ", e)

  def get_folders(self):
    url = f"{self.base_url}/Folders"
    response = requests.get(url, headers=self.headers)
    if response.status_code == 200:
      data = response.json()
      folders = data.get('value', [])
      return folders

    else:
      print(f"Error: {response.status_code} - {response.text}")
      return []

  def get_queue_items(self, queue_name):
      queue_def_id = self.get_queue_definition_id(queue_name)
      if not queue_def_id:
        return []

      queue_item_url = f"{self.base_url}/QueueItems?$filter=QueueDefinitionId eq {queue_def_id}"
      response = requests.get(queue_item_url, headers=self.headers)
      if response.status_code == 200:
        queue_items = response.json().get('value', [])
        return queue_items
      else:
        print(f"Error: {response.status_code} - {response.text}")
        return []

  def get_queue_definition_id(self, queue_name):
    queue_url = f"{self.base_url}/QueueDefinitions?$filter=Name eq '{queue_name}'"
    response = requests.get(queue_url, headers=self.headers)

    if response.status_code == 200:
      queue_data = response.json()
      if 'value' in queue_data and len(queue_data['value']) > 0:
        queue_def_id = queue_data['value'][0]['Id']
        return queue_def_id
      else:
        print(f"Error: Queue '{queue_name}' not found.")
        return None
    else:
      print(f"Error: {response.status_code} - {response.text}")
      return None
import requests
import datetime

class ApiHandler:
  def __init__(self):
    self.GetProcessLIstUrl = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/odata/Processes"
    self.SendMessageToOrchestrationURL = "https://cloud.uipath.com/personlebfom/MasterEA/orchestrator_/odata/Queues/UiPathODataSvc.AddQueueItem"
    self.payload = {}
    self.OrganizationUnitId=4061831
    self.current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    self.tocken = 'Bearer '
    self.headers = {
      'accept': 'application/json',
      'authorization': self.tocken }

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
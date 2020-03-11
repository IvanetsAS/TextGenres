import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class Exporter:
    def __init__(self):
        self.CREDENTIALS_FILE = '/home/ivanetsas/PycharmProjects/Readability/text-220509-7934bb4ea547.json'     # имя файла с закрытым ключом

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.CREDENTIALS_FILE,
            ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        )

        httpAuth = credentials.authorize(httplib2.Http())
        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

        self.dataToAdd = []

    def addData(self, metric, file_name):
        self.addData([
            file_name,
            metric.wordCount,
            metric.sentencesCount,
            metric.charactersCount,
            metric.vowelsCount,
            metric.FRE,
            metric.FKRA,
            metric.ARI
        ])

    def addData(self, data_arr):
        self.dataToAdd.append(data_arr)

    def rewriteTable(self, table_id):
        results = self.service.spreadsheets().values().batchUpdate(spreadsheetId=table_id, body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {
                    "range": "A1:N" + str(self.dataToAdd.__len__()),
                    "majorDimension": "ROWS",
                    "values": self.dataToAdd
                }
            ]
        }).execute()
        self.dataToAdd.clear()

    # def rewriteTable(self):
    #     SAMPLE_SPREADSHEET_ID = "1WL1LeGvYMCcwy8Vca3x6FhQ0BRSt9A1pRw1E21TLvAo"
    #     self.rewriteTable(SAMPLE_SPREADSHEET_ID)


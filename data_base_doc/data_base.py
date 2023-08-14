import httplib2
from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'data_base_doc/creds.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
service = discovery.build('sheets', 'v4', http=httpAuth)


def send_data(spreadsheets_id: str, data: list, num: int) -> None:
    """
    Функция отправляет данные в гугл таблицу
    :param spreadsheets_id : str id таблицы из функции creating_sheet (можно подставить данные своей таблицы)
    :param data : list список данных, которые запишутся в одну строку
    :param num: номер строки куда будет вестись запись
    :return: None
    """
    body = {'value_input_option': 'USER_ENTERED',
            'data': [{
                "range": f"A{num}",
                "majorDimension": "ROWS",
                "values": [data]}]
            }
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheets_id, body=body).execute()


def send_data_to_sheep(data, status, spreadsheet_id, message):

    data_for_send = [data[0][0], *data[0][2:5], data[0][-3], data[0][-2], status, data[0][-1], data[0][-4],
                     message.from_user.first_name]
    send_data(spreadsheets_id=spreadsheet_id, num=data[0][0] + 1, data=data_for_send)





if __name__ == "__main__":
    pass

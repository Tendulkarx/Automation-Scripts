import os
import requests
import datetime
import unicodedata
from bs4 import BeautifulSoup
from sendEmail import send_email
from googleapiclient.discovery import build
# from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'sheetkeys.json'


def send_to_sheets(data_as_list):
  creds = None
  creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

  # If modifying these scopes, delete the file token.json.
  # SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

  # The ID and range of a sample spreadsheet.
  SAMPLE_SPREADSHEET_ID = '1kcjkBJRcJU4nf_vNntTtbmt1W1bVU9_6cfJ3S-MK1PY'
  # SAMPLE_RANGE_NAME = 'Class Data!A2:E'

  service = build('sheets', 'v4', credentials=creds)

  # Call the Sheets API
  sheet = service.spreadsheets()
  result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                              range="Amazon!A1:B1").execute()
  values = result.get('values', [])

  data = data_as_list
  # request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
  #                                 range="Amazon!A2",
  #                                 valueInputOption="USER_ENTERED",
  #                                 body={"values": data}).execute()

  request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                   range="Amazon!A2",
                                   valueInputOption="USER_ENTERED",
                                   insertDataOption="INSERT_ROWS",
                                   body={"values": data}).execute()
  # print(request)


HEADERS = ({'User-Agent':
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Accept-Language': 'en-GB,en-US, en;q=0.5'})


def get_product_info(url):
  page = requests.get(url, headers=HEADERS)
  soup = BeautifulSoup(page.content, features="lxml")
  time_stamp = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
  try:
    title = soup.find(id='productTitle').get_text().strip()
    price_str = soup.find(id='priceblock_ourprice').get_text().strip()
    # price_str = soup.find(id='priceblock_pospromoprice').get_text().strip()
  except:
    return None, None, None, None

  try:
    soup.select('#availability .a-color-success')[0].get_text().strip()
    available = True
  except:
    available = False

  try:
    price = unicodedata.normalize("NFKD", price_str)
    price = price.replace(',', '.').replace('£', '')
    price = float(price)
  except:
    return None, None, None, None

  return title, price, available, time_stamp


if __name__ == '__main__':
  username = os.environ.get('email_user')
  product_1 = "https://www.amazon.co.uk/Neewer-AC-PW20-Adapter-Compatible-DSC-RX10/dp/B08PJVZJJ1/ref=sr_1_6?dchild=1&keywords=canon+750+battery+adapter&qid=1618605654&sr=8-6"
  product_2 = "https://www.amazon.co.uk/Elgato-Cam-Link-Broadcast-camcorder/dp/B07K3FN5MR/?_encoding=UTF8&pd_rd_w=mSLLJ&pf_rd_p=3d6f73e3-59a0-49fa-adae-5548adbb7b98&pf_rd_r=QK3RP99YNYNSP12DEGMH&pd_rd_r=8b4350f6-e54d-4709-8606-7e496bf09b5a&pd_rd_wg=cL2IC&ref_=pd_gw_ci_mcx_mr_hp_d"
  product_3 = "https://www.amazon.co.uk/dp/B07JGSPQV2/?coliid=I2SYPWQK4KYMNY&colid=1IMZNQ3MU13KC&psc=1&ref_=lv_ov_lig_dp_it"
  product_4 = "https://www.amazon.co.uk/iFixit-precision-screwdriver-compatible-smartphone/dp/B0189YWOIO/ref=sr_1_5?crid=1K3X503IFJ99Q&dchild=1&keywords=ifixit&qid=1619461147&sprefix=ifi%2Caps%2C191&sr=8-5"
  product_5 = "https://www.amazon.co.uk/iFixit-Aluminum-Precision-MacBook-Smartphone/dp/B07BMM74FD/ref=sr_1_8?crid=1K3X503IFJ99Q&dchild=1&keywords=ifixit&qid=1619461147&sprefix=ifi%2Caps%2C191&sr=8-8"

  # List of products and price limits
  products = [(product_1, 26), (product_2, 115), (product_3, 325),
              (product_4, 30), (product_5, 55)]

  products_below_limit = []
  for product_url, limit in products:
    title, price, available, time_stamp = get_product_info(product_url)
    if title is not None and price < limit and available:
      products_below_limit.append((' '.join(title.split()[:15]), price,
                                   '=HYPERLINK("{}","{}")'.format(product_url,
                                                                  'Link'), time_stamp))

  if products_below_limit:
    send_to_sheets(products_below_limit)
    # print(products_below_limit)

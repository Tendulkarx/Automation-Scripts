import os
import requests
import unicodedata
from bs4 import BeautifulSoup
from sendEmail import send_email

HEADERS = ({'User-Agent':
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Accept-Language': 'en-GB,en-US, en;q=0.5'})


def get_product_info(url):
  page = requests.get(url, headers=HEADERS)
  soup = BeautifulSoup(page.content, features="lxml")
  try:
    title = soup.find(id='productTitle').get_text().strip()
    price_str = soup.find(id='priceblock_ourprice').get_text().strip()
    # price_str = soup.find(id='priceblock_pospromoprice').get_text().strip()
  except:
    return None, None, None

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
    return None, None, None

  return title, price, available


if __name__ == '__main__':
  username = os.environ.get('email_user')
  product_1 = "https://www.amazon.co.uk/Neewer-AC-PW20-Adapter-Compatible-DSC-RX10/dp/B08PJVZJJ1/ref=sr_1_6?dchild=1&keywords=canon+750+battery+adapter&qid=1618605654&sr=8-6"
  product_2 = "https://www.amazon.co.uk/Elgato-Cam-Link-Broadcast-camcorder/dp/B07K3FN5MR/?_encoding=UTF8&pd_rd_w=mSLLJ&pf_rd_p=3d6f73e3-59a0-49fa-adae-5548adbb7b98&pf_rd_r=QK3RP99YNYNSP12DEGMH&pd_rd_r=8b4350f6-e54d-4709-8606-7e496bf09b5a&pd_rd_wg=cL2IC&ref_=pd_gw_ci_mcx_mr_hp_d"
  product_3 = "https://www.amazon.co.uk/dp/B07JGSPQV2/?coliid=I2SYPWQK4KYMNY&colid=1IMZNQ3MU13KC&psc=1&ref_=lv_ov_lig_dp_it"
  product_4 = "https://www.amazon.co.uk/iFixit-precision-screwdriver-compatible-smartphone/dp/B0189YWOIO/ref=sr_1_5?crid=1K3X503IFJ99Q&dchild=1&keywords=ifixit&qid=1619461147&sprefix=ifi%2Caps%2C191&sr=8-5"
  product_5 = "https://www.amazon.co.uk/iFixit-Aluminum-Precision-MacBook-Smartphone/dp/B07BMM74FD/ref=sr_1_8?crid=1K3X503IFJ99Q&dchild=1&keywords=ifixit&qid=1619461147&sprefix=ifi%2Caps%2C191&sr=8-8"



  # List of products and price limits
  products = [(product_1, 26), (product_2, 115), (product_3, 325), (product_4, 30), (product_5, 55)]

  products_below_limit = []
  for product_url, limit in products:
    title, price, available = get_product_info(product_url)
    if title is not None and price < limit and available:
      products_below_limit.append((title, price, product_url))

  if products_below_limit:
    message = "Reference: Your tracked products are below the given limit!"
    for title, price, url in products_below_limit:
      # message += f"{title}\n"
      # message += f"Price: {price}\n"
      # message += f"{url}\n\n"
      message += """\
              <!DOCTYPE html>
              <head>
              <style>
              table {{
                  width: 100%;
                  text-align:left;
              }}
              table, th, td {{
                border: 1px solid black;
                border-collapse: collapse;
                padding: 3px 10px 3px 10px;
              }}
              th.Url, th.Price {{ width: 10% }}
              th.Product {{ width: 80%; }}
            
              </style>
              </head>
              <html>
                <body>
                <br>
                  <table class="mytable">
                    <tr>
                      <th class="Product">Product</th>
                      <th class="Price">Price</th>
                      <th class="Url">Url</th>
                    </tr>
                    <tbody>
                    <tr>
                    <td>{title}</td>
                    <td>£{price}</td>
                    <td><a href={url}>link</a></td>
                    </tr>
                    </tbody>
                  </table>
                </body>
              </html>
              """.format(title=' '.join(title.split()[:15]), price=price, url=url)
    send_email(username, [username], 'Notified', message)

import requests
import os
import argparse

token = os.getenv('TOKEN')

def cut_link_for_api(link):
  '''Обрезает (http:// или https://) + www. для подстановки в API.'''
  if link.startswith('http://'):      
    link = link[len('http://'):]
  
  if link.startswith('https://'):
    link = link[len('https://'):]

  if link.startswith('www.'):
    return link[len('www.'):]

  return link

def get_link_info(token, link):
  '''Получить информацию о типе ссылки.
  На выходе словарь с двумя параметрами:
    is_bitlink -- [bool] флаг укороченной ссылки если True
    link -- [str] сама ссылка, обрезанная для API, если укороченная.
  '''

  headers = {'Authorization': 'Bearer {}'.format(token)}
  cut_link = cut_link_for_api(link)
  url = 'https://api-ssl.bitly.com/v4/bitlinks/{link}'.format(link=cut_link)
  response = requests.get(url, headers=headers)

  result_of_check = dict()
  result_of_check['is_bitlink'] = False
  result_of_check['link'] = link

  if response.ok:
    result_of_check['is_bitlink'] = True
    result_of_check['link'] = response.json()['id']

  return result_of_check



def shorten_link(token, link):
  '''По длинной ссылке получить короткую.'''

  headers = {'Authorization': 'Bearer {}'.format(token)}

  # без http:// не работает, даже с www.
  if not link.startswith('http'):
    link = 'http://' + link

  params = {'long_url': link}
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  response = requests.post(url, headers=headers, json=params)

  if not response.ok:
    return None

  return response.json()['link']

def count_clicks(token, link):
  '''По короткой ссылке получить количество кликов.'''

  headers = {'Authorization': 'Bearer {}'.format(token)}
  params = {'units': -1}
  url = 'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'.format(link=link)
  response = requests.get(url, headers=headers, params=params)

  if not response.ok:
    return None

  return response.json()['total_clicks']


if __name__ == '__main__':

  doc = '''
  Программа дает короткую ссылку при вводе обычной ссылки.
  При вводе короткой ссылки дает количество кликов на ссылку.
  При некорректном ответе bit.ly API вызывается исключение.
  '''

  # ссылка - обязательный параметр
  parser = argparse.ArgumentParser(description=doc)
  parser.add_argument('link', help='Короткая или длинная ссылка')
  args = parser.parse_args()


  link_info = get_link_info(token, args.link)

  if link_info['is_bitlink']:
    clicks = count_clicks(token, link_info['link'])

    if clicks is None:
      raise requests.exceptions.HTTPError('invalid bitlink: {link}'.format(link=link_info['link']))

    print(clicks)
  else:
    bitlink = shorten_link(token, link_info['link'])

    if bitlink is None:
      raise requests.exceptions.HTTPError('invalid longlink: {link}'.format(link=link_info['link']))

    print(bitlink)

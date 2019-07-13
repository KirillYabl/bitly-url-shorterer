import requests
import os
import argparse
import dotenv

dotenv.load_dotenv()
token = os.getenv('TOKEN')

def cut_link_for_api(link):
  '''Cut (http:// or https://) + www. for transfer to bit.ly API.'''
  if link.startswith('http://'):      
    link = link[len('http://'):]
  
  if link.startswith('https://'):
    link = link[len('https://'):]

  if link.startswith('www.'):
    return link[len('www.'):]

  return link

def get_link_info(token, link):
  '''Get link info.
  The output is dict with 2 parameters:
    is_bitlink -- [bool] True if link is bitlink
    link -- [str] link which will cut for bit.ly API if is_bitlink == True
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
  '''Get shorten link from long link.'''

  headers = {'Authorization': 'Bearer {}'.format(token)}

  # without http:// don't work, even with www.
  if not link.startswith('http'):
    link = 'http://' + link

  params = {'long_url': link}
  url = 'https://api-ssl.bitly.com/v4/bitlinks'
  response = requests.post(url, headers=headers, json=params)

  if not response.ok:
    return None

  return response.json()['link']

def count_clicks(token, link):
  '''Get number of clicks on a short link for all time.'''

  headers = {'Authorization': 'Bearer {}'.format(token)}
  # for all time
  params = {'units': -1}
  url = 'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary'.format(link=link)
  response = requests.get(url, headers=headers, params=params)

  if not response.ok:
    return None

  return response.json()['total_clicks']


if __name__ == '__main__':

  doc = '''
  The programm give you short link when you enter long link.
  If you enter a short link you will get the number of clicks on a short link for all time.
  If you enter incorrect link or short link and HTTP answer will not equal 2xx
  the programm raise exception
  '''

  # link is required parameter
  parser = argparse.ArgumentParser(description=doc)
  parser.add_argument('link', help='Short or long link')
  args = parser.parse_args()


  link_info = get_link_info(token, args.link)

  if link_info['is_bitlink']:
    clicks = count_clicks(token, link_info['link'])

    if clicks is None:
      raise requests.exceptions.HTTPError('invalid bitlink: {link}'.format(link=link_info['link']))

    print('The number of clicks:', clicks)
  else:
    bitlink = shorten_link(token, link_info['link'])

    if bitlink is None:
      raise requests.exceptions.HTTPError('invalid longlink: {link}'.format(link=link_info['link']))

    print('Your bitlink:', bitlink)

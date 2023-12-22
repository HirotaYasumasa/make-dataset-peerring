import re
import pandas as pd

def remove_hashtag(text:str):
    remove_hash_text = re.sub(r'(#[^\s\\]+)','',text.replace('＃','#').replace('♯','#'))
    return remove_hash_text

def get_hashtag(text:str):
    hashtags = ';'.join(re.findall(r'(#[^\s\\]+)', text.replace('＃','#').replace('♯','#')))
    return str(hashtags)

def main():
  df = pd.read_csv('./data/peerring_post_all.csv')
  print(df['content'][0])

  hash = get_hashtag(df['content'][0])

  text = remove_hashtag(df['content'][0])

  print(hash.split(';'))

  print(text)


if __name__ == '__main__':
  main()

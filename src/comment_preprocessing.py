import re
import pandas as pd

def custom_split(text):
  #content内のシングルコーテーションを一時的に置き換える
  temp_text = text.replace("\\'", '<<QUOTATION>>')
  #content内のカンマを一時的に置き換える
  temp_text = re.sub(r"'(.*?)'", lambda x: x.group(0).replace(',', '<<COMMA>>'), temp_text)

  split_text = temp_text.split(',')

  split_text = [part.replace('<<COMMA>>', ',') for part in split_text]
  split_text = [part.replace('<<QUOTATION>>', "\\'") for part in split_text]

  return split_text

def main():
  text_file = open('./data/comments_lists.txt', 'r', encoding='UTF-8')
  texts = []
  previous_text = ""

  #謎の改行を削除する
  for text in text_file:
    if text.startswith('('):
      if previous_text:
        texts.append(previous_text.rstrip('\n').rstrip(',').rstrip(';').rstrip(')').lstrip('('))
      previous_text = text
    else:
      previous_text = previous_text.rstrip('\n') + text
  if previous_text:
    texts.append(previous_text.rstrip('\n').rstrip(',').rstrip(';').rstrip(')').lstrip('('))

  # #データ(列数)に不備がないかの確認
  # comment_columns = 7
  # count = 0
  # for text_data in texts:
  #   split_data = custom_split(text_data)
  #   count += 1
  #   if len(split_data) != comment_columns:
  #     print("==========Error==========")
  #     print(count)
  #     print(len(split_data))
  #     print(split_data)
  #     break

  dataframes = []
  comment_column_names = ['id', 'user_id', 'type', 'post_id', 'content', 'created_at', 'updated_at']

  for text_data in texts:
    split_text = custom_split(text_data)
    df = pd.DataFrame([split_text], columns=comment_column_names)
    dataframes.append(df)

  result_df = pd.concat(dataframes, ignore_index=True)

  result_df['type'] = result_df['type'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['content'] = result_df['content'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['created_at'] = result_df['created_at'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['updated_at'] = result_df['updated_at'].map(lambda x: x.lstrip('\'').rstrip('\''))

  result_df['id'] = result_df['id'].astype('int')
  result_df['user_id'] = result_df['user_id'].astype('int')
  result_df['post_id'] = result_df['post_id'].astype('int')

  result_df.sort_values(by=["post_id","id"]).to_csv('./output/peerring_comment_all.csv', index=False, encoding='utf_8_sig')

if __name__ == '__main__':
  main()

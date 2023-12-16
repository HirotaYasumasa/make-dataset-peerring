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
  text_file = open('./data/posts_list.txt', 'r', encoding='UTF-8')
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
  # count = 0
  # for text_data in texts:
  #   split_data = custom_split(text_data)
  #   count += 1
  #   if len(split_data) != 11:
  #     print("==========Error==========")
  #     print(count)
  #     print(len(split_data))
  #     print(split_data)
  #     break

  dataframes = []
  column_names = ['id', 'user_id', 'type', 'content', 'category', 'commented_at', 'audience', 'is_pinned', 'device_info', 'created_at', 'updated_at']

  for text_data in texts:
    split_text = custom_split(text_data)
    df = pd.DataFrame([split_text], columns=column_names)
    dataframes.append(df)

  result_df = pd.concat(dataframes, ignore_index=True)

  result_df['type'] = result_df['type'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['content'] = result_df['content'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['category'] = result_df['category'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['commented_at'] = result_df['commented_at'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['device_info'] = result_df['device_info'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['created_at'] = result_df['created_at'].map(lambda x: x.lstrip('\'').rstrip('\''))
  result_df['updated_at'] = result_df['updated_at'].map(lambda x: x.lstrip('\'').rstrip('\''))

  result_df['category'] = result_df['category'].map(lambda x: 'NULL' if x == '' else x)

  result_df['id'] = result_df['id'].astype('int')
  result_df['user_id'] = result_df['user_id'].astype('int')

  chunk_size = 5000
  number_of_chunks = len(result_df) // chunk_size + (1 if len(result_df) % chunk_size else 0)

  result_df.sort_values(by=["user_id","id"]).to_csv('./output/peerring_post_all.csv', index=False, encoding='utf_8_sig')

  for i in range(number_of_chunks):
    start_row = i * chunk_size
    end_row = start_row + chunk_size
    df_subset = result_df.sort_values('user_id').iloc[start_row:end_row]
    #df_subset.to_csv(f'./output/peerring_post_id_{i+1}.csv', index=False, encoding='utf_8_sig')

if __name__ == '__main__':
  main()

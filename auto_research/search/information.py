import datetime
import json
import os
import re


def extract_exact_date(result):
    if 'abstract' in result['bib']:
        abstract = result['bib']['abstract']

        # Extract the number of days ago from the abstract
        match = re.search(r'(\d+)\s+day[s]?\s+ago', abstract)
        if match:
            days_ago = int(match.group(1))
            result_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
            result_date = result_date.date()
            print("Found a paper on", result_date)
        return result_date
    else:
        return None

def save_meta_data(meta_data_path,papers_info):

  if os.path.exists(meta_data_path):
      with open(meta_data_path, 'r') as json_file:
          existing_data = json.load(json_file)
      if isinstance(existing_data, list) and isinstance(papers_info, list):
          combined_data = existing_data + papers_info
      else:
          raise ValueError("Existing data and new data must be lists.")
  else:
      combined_data = papers_info

  seen_titles = set()
  unique_data = []
  for item in combined_data:
      title = item.get("title")
      if title:
          if title not in seen_titles:
              unique_data.append(item)
              seen_titles.add(title)
      else:
          unique_data.append(item)

  with open(meta_data_path, 'w') as json_file:
      json.dump(unique_data, json_file, indent=4)

  print()
  print(f"Metadata saved to "+meta_data_path)


def read_meta_data(meta_data_path):
  if os.path.exists(meta_data_path):
    with open(meta_data_path, 'r') as json_file:
      meta_data = json.load(json_file)
    return meta_data
  else:
    return []
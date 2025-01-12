from auto_research.search.files_management import is_pdf_corrupted
import requests
from requests.exceptions import Timeout, RequestException
import os
import arxiv

def download_pdf(url, filename, folder=None, timeout=30):
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()  # Check if the request was successful
        if folder != None:
          os.makedirs(folder, exist_ok=True)
          file_path=folder+"/"+filename
        else:
          file_path=filename
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {filename}")

        # Check if the downloaded PDF file is corrupted
        if not is_pdf_corrupted(file_path):
            print(f"The downloaded PDF file '{filename}' is corrupted.")
            os.remove(file_path)  # Delete the local file
            return False
    except Timeout:
        print(f"Timeout occurred while downloading {filename} from {url}")
        return False
    except RequestException as e:
        print(f"Failed to download {filename} from {url}: {e}")
        return False
    return True


def get_paper_details_from_semantic_scholar(title,verbose=False):
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": title,
        "fields": "title,abstract,venue"
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data.get('data'):
            paper = data['data'][0]
            abstract = paper.get('abstract', 'Abstract not available')
            venue = paper.get('venue', 'Venue not available')
            return abstract, venue
    elif verbose:
        print(f"Error: {response.status_code}")
    return None

def get_arxiv_paper_details(title):
    client = arxiv.Client()
    search = arxiv.Search(
        query=title,
        max_results=1,
        sort_by=arxiv.SortCriterion.Relevance
    )
    results = client.results(search)
    for result in results:
        paper_title = result.title
        abstract = result.summary
        pdf_link = result.pdf_url
        venue = result.journal_ref if result.journal_ref else "arXiv"
        return paper_title, abstract, pdf_link, venue
    return None

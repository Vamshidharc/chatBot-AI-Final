import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from nltk.corpus.reader import documents

visited_urls = set()  # To keep track of visited URLs

def get_html_content(url):
    response = requests.get(url)
    return response.content

def get_plain_text(html_content):
    soup = BeautifulSoup(html_content,'html.parser')
    for script in soup(["script"]):
        script.extract()
    plain_text = '\n'.join(line.strip() for line in soup.get_text().splitlines() if line.strip())
    return plain_text

def split_text_into_chunks(plain_text, max_chars=2000):
    text_chunks=[]
    current_chunk =""
    for line in plain_text.split("\n"):
        if len(current_chunk) + len(line) + 1 <= max_chars:
            current_chunk += line+ ""
        else:
            text_chunks.append(current_chunk.strip())
            current_chunk = line + ""
        if current_chunk:
            text_chunks.append(current_chunk.strip())
        return text_chunks

directory = '/Data'

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents
#
# def split_docs(documents,chunk_size=1000, chunk_overlap=20):
#   text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#   docs=text_splitter.split_documents(documents)
#   return docs
#
# docs = split_docs(documents)
# print(len(docs))

# def scrape_text_from_url (filepath, max_chars=10000):
   # html_content = get_html_content(url)
   #  plain_text1 = get_plain_text(html_content)
  #  plain_text1 = website_scraping(url)
  #  plain_text = get_plain_text(plain_text1)
  #  print("Plain = ", plain_text1)

  #  text_chunks = get_csv_splits(plain_text, max_chars)
  # text_chunks = website_scraping(url,max_chars)
   # print(plain_text1)
   #  char_count = len(plain_text)
   #  print("Number of characters:", char_count)
   #  print(text_chunks)
   #  return text_chunks

def load_docs(directory):
  loader = DirectoryLoader(directory)
  documents = loader.load()
  return documents

def split_docs(documents,chunk_size=1000, chunk_overlap=20):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
  docs=text_splitter.split_documents(documents)
  print('len docs -',len(docs))
  print('docs -',docs[0].page_content)
  return docs

#docs = split_docs(documents)
#print(len(docs))

def website_scraping(url,max_chars=10000):

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the question and answer elements on the page
    #question_elements = soup.find_all('h2', class_='coop-c-text coop-u-margin-bh')
    #answer_elements = soup.find_all('div', class_='coop-c-text coop-u-margin-bh')
    answer_elements = soup.find_all('div', class_=('flex-hero__text-inner', 'coop-c-page'))
    answers = [answer.text.strip() for answer in answer_elements]
    #print('Answers - ', answers)

    # Save the questions and answers to the output.txt file
    with open('Data/WebScraped5.txt', 'w', encoding='utf-8') as file:

        for answer in answers:
         #   cleaned_answer = answer.replace('\n', ' ').strip()
         #   if cleaned_answer:
         #       file.write(cleaned_answer + '\n')
                file.write(answer + '/n')
            #mystring =answers[x]

          # for answer in zip(answers):
          #  file.write("Question: " + question + "\n")
          #  file.write(mystring)
          #  file.write(answer + '\n')



    # Confirmation message
    print("Data saved to text file.")


    print("Website scraping completed. Results are saved in .txt file")
    return answer


def website_crawling(url):
    global visited_urls

    # Parse the base URL
    base_url = urlparse(url).netloc

    # Get the HTML content of the current page
    html_content = get_html_content(url)
    plain_text = get_plain_text(html_content)

    # Write plain_text to a text document
    with open('output.txt', 'a', encoding='utf-8') as file:
        file.write(plain_text + '\n')

    # Add the current URL to visited_urls
    visited_urls.add(url)

    # Parse all anchor tags and recursively scrape internal links
    soup = BeautifulSoup(html_content, 'html.parser')
    for link in soup.find_all('a'):
        href = link.get('href')

        # Build the absolute URL for internal links
        if href and not href.startswith(('http://', 'https://', 'mailto:')):
            absolute_url = urljoin(url, href)

            # Visit the internal link if it belongs to the same domain and hasn't been visited yet
            if urlparse(absolute_url).netloc == base_url and absolute_url not in visited_urls:
                website_crawling(absolute_url)

                # Visit the internal link if it belongs to the same domain and hasn't been visited yet
             #   if urlparse(absolute_url).netloc == base_url and absolute_url not in visited_urls:
             #       plain_text += "\n" + website_crawling(absolute_url)

      #  return plain_text

# Example usage
#main_url = "https://example.com"  # Replace with the main/home page URL of the website
#website_crawling(main_url)



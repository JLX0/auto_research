from PyPDF2 import PdfReader
import tiktoken
import fitz

class paper():

    end_markers=["references","acknowledgement","bibliography"]

    def __init__(self, paper_path, model='gpt-4o-mini'):
        self.paper_path = paper_path
        self.whole_paper=[]
        self.paper_length=0
        self.model = model
        self.extracted_information= {"abstract":"","introduction":"","discussion":"","conclusion":"","algorithm":""}

    def read_pypdf2(self):
        pdf_obj = PdfReader(self.paper_path)
        self.whole_paper = []
        for page in pdf_obj.pages:
            text = page.extract_text()
            self.whole_paper.append(text)

    def read_pymupdf(self):
        pdf_document = fitz.open(self.paper_path)
        self.whole_paper = []
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            text = page.get_text()
            self.whole_paper.append(text)

    def first_n_pages(self, n):
        return ''.join(self.whole_paper[:n])

    def print_whole_paper(self):
        for idx,text in enumerate(self.whole_paper):
            print(f"-----Page {idx+1} beginning marker-----")
            print(text)
            print(f"-----Page {idx+1} ending marker-----")

    @staticmethod
    def extract_up_to_first_match_exclude_list(a , b_list) :
        """
        Concatenate the list of strings A and extract the part up to the first occurrence of any substring in B_list, excluding the substring.
        The returned result should be a list of strings.
        Ignore the first 3 pages of the concatenated string.
        Case insensitive.

        :param a: A list of strings to concatenate and search within.
        :param b_list: A list of substrings to search for.
        :return: A list of strings from A up to but not including the first occurrence of any substring in B_list.
        """
        # Concatenate the list of strings into a single string
        concatenated_a = ''.join(a)

        # skip the first 3 pages
        first_three_pages = a[:3]
        first_three_pages = ''.join(first_three_pages)

        # Convert the concatenated string to lowercase for case insensitive search
        lower_concatenated_a = concatenated_a.lower()

        # Initialize the index to None
        first_index = None

        # Iterate over each substring in the list
        for b in b_list :
            # Convert the substring to lowercase
            lower_b = b.lower()
            # Find the first occurrence of the substring in the concatenated string
            index = lower_concatenated_a.find(lower_b)
            # Update the first_index if this substring occurs earlier than previous matches
            if index != -1 and (index > len(first_three_pages)) and (first_index is None or index < first_index) :
                first_index = index

        if first_index is not None :
            # Extract up to the first match, excluding the match
            extracted_string = concatenated_a[:first_index]
        else :
            extracted_string = concatenated_a

        # Convert the extracted string back to a list of strings
        result = []
        current_string = ""
        for char in extracted_string :
            current_string += char
            # Check if the current string matches any of the original strings in `a`
            if current_string in a :
                result.append(current_string)
                current_string = ""

        if current_string :  # Append any remaining part
            result.append(current_string)

        return result

    def extract_ending_pages(self,page_number=3):
        ending_pages=paper.extract_up_to_first_match_exclude_list(self.whole_paper,paper.end_markers)
        ending_pages=ending_pages[-page_number:]
        ending_pages=''.join(ending_pages)
        return ending_pages



    def calculate_token_length(self):
        encoder = tiktoken.encoding_for_model(self.model)
        self.paper_length = 0
        for text in self.whole_paper:
            length = len(encoder.encode(text))
            self.paper_length += length
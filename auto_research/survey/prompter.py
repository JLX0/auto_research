class prompt():


    general_text_cleaning = ["Your answer should not include any references marks, author information, page number, publisher information, figure captions, or table captions."]
    general_text_cleaning += ["Your answer should not paraphrase or summarize the text, but should be a direct extraction of text."]

    def __init__(self):
        self.prompt = ""


    def prompt_formatting_GPT(self , prompt) :
        for idx , n in enumerate(prompt) :
            if idx > 0 :
                n = "\n" + n
            prompt[idx] = { "role" : "system" , "content" : n }
        return prompt

    def print_prompt(self):
        for prompt_segment in self.prompt:
            print(prompt_segment["content"])

    def extract_abstract(self,raw_text):
        prompt_string = ["Given some raw text extracted from a PDF file, your task is to extract the abstract from the raw text."]
        prompt_string += ["The raw text up to the first 2 pages of the PDF file is:"]
        prompt_string += [raw_text]
        prompt_string += ["Your answer should be the abstract of the paper"]
        prompt_string += prompt.general_text_cleaning
        prompt_string += ["Here is the abstract:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def extract_introduction(self,raw_text):
        prompt_string = ["Given some raw text extracted from a PDF file, your task is to extract the introduction from the raw text."]
        prompt_string += ["The raw text up to the first 5 pages of the PDF file is:"]
        prompt_string += [raw_text]
        prompt_string += ["Your answer should be the introduction of the paper"]
        prompt_string += ["Note that the paper might not have a section named 'Introduction', but the first few pages of the paper usually contain the equivalent of an introduction."
                          "For example, there might be a section named 'Background' or 'Related Work' that serves as the introduction."]
        prompt_string += ["If the paper has more than one sections related to the introduction, you should only include the first section that serves as the introduction."]
        prompt_string += prompt.general_text_cleaning
        prompt_string += ["Here is the introduction:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def extract_discussion(self,raw_text):
        prompt_string = ["Given some raw text extracted from a PDF file, your task is to extract the discussion from the raw text."]
        prompt_string += ["The raw text of the last 3 pages of the PDF file is:"]
        prompt_string += [raw_text]
        prompt_string += ["Your answer should be the discussion of the paper"]
        prompt_string += ["Note that the paper might not have a section named 'Discussion', but the last few pages of the paper usually contain the equivalent of a discussion."
                          "For example, there might be a section named 'Analysis', 'Limitations', or 'Future Work' that serves as the discussion."]
        prompt_string += ["If the paper has more than one sections related to the discussion, you should only include the first section that serves as the discussion."]
        prompt_string += ["If the paper does not have a discussion section, or you cannot identify the discussion section from the provided text, your answer is simply 'N/A'."]
        prompt_string += prompt.general_text_cleaning
        prompt_string += ["Here is the discussion:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def extract_conclusion(self,raw_text):
        prompt_string = ["Given some raw text extracted from a PDF file, your task is to extract the conclusion from the raw text."]
        prompt_string += ["The raw text of the last 3 pages of the PDF file is:"]
        prompt_string += [raw_text]
        prompt_string += ["Your answer should be the conclusion of the paper"]
        prompt_string += ["Note that the paper might not have a section named 'Conclusion', but the last few pages of the paper usually contain the equivalent of a conclusion."
                          "For example, there might be a section named 'Summary' or 'Concluding Remarks' that serves as the conclusion."]
        prompt_string += ["If the paper has more than one sections related to the conclusion, you should only include the last section that serves as the conclusion."]
        prompt_string += ["If the paper does not have a conclusion section, or you cannot identify the conclusion section from the provided text, your answer is simply 'N/A'."]
        prompt_string += prompt.general_text_cleaning
        prompt_string += ["Here is the conclusion:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def extract_algorithm(self,raw_text):
        prompt_string = ["Given some raw text extracted from a PDF file, your task is to extract the algorithm from the raw text."]
        prompt_string += ["The raw text up to the first 12 pages of the PDF file is:"]
        prompt_string += [raw_text]
        prompt_string += ["Your answer should be a Python list of string that describes algorithm described in the paper (in the format of pseudo-code)."]
        prompt_string += ["If the paper has more than one algorithm, your answer should be a Python list of strings, each string representing one algorithm."]
        prompt_string += prompt.general_text_cleaning
        prompt_string += ["Here is the Python list:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def explain_algorithm(self,paper,algorithm):
        prompt_string = ["Given the algorithm described in a paper, your task is to explain the algorithm by reading the first 12 pages of the paper."]
        prompt_string = ["The first 12 pages of the paper is:"]
        prompt_string += [paper]
        prompt_string += ["The algorithm is:"]
        prompt_string += [algorithm]
        prompt_string += ["Your answer should include the following information:"]
        prompt_string += ["1. Meaning of each variable/part of the algorithm"]
        prompt_string += ["2. Explanation of any terms/concepts/operations that are beyond the common knowledge to an undergraduate computer science student"]
        prompt_string += ["3. A step-by-step explanation of the algorithm in layman's terms"]
        prompt_string += ["Your answer should be in the following format:"]
        prompt_string += ["1. Meaning of each variable/parameter: [answer]\n\n"
                          "2. Explanation of terms/concepts/operations: [answer]\n\n"
                          "3. Step-by-step explanation: [answer]"]
        prompt_string += ["Each one of the [answer] should be specific enough to enable the reader to implement the algorithm using code."]
        prompt_string += ["Here is the explanation:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)

    def summarize_default_computer_science(self , abstract , introduction , discussion , conclusion):
        prompt_string = ["Given the abstract, introduction, discussion, and conclusion of a paper, your task is to summarize the paper."]
        prompt_string += ["The abstract of the paper is:"]
        prompt_string += [abstract]
        prompt_string += ["The introduction of the paper is:"]
        prompt_string += [introduction]
        prompt_string += ["The discussion of the paper is:"]
        prompt_string += [discussion]
        prompt_string += ["The conclusion of the paper is:"]
        prompt_string += [conclusion]
        prompt_string += ["Your answer should include the following information:"]
        prompt_string += ["1. The main topic of the paper"]
        prompt_string += ["2. Existing problems in the field, such as limitations of previous studies or unsolved issues"]
        prompt_string += ["3. The main contributions of the paper, such as new methods or insights, especially compared to previous studies and/or baselines"]
        prompt_string += ["4. Experimental results, which include the datasets or benchmark used, the evaluation metrics,"
                          " and the comparison with previous studies and/or baselines"]
        prompt_string += ["5. Conclusions from the paper, such as the major findings, implications, and future directions"]
        prompt_string += ["Your answer should be in the following format:\n\n"
                          "1. The main topic: [answer]\n\n"
                          "2. Existing problems: [answer]\n\n"
                          "3. The main contributions: [answer]\n\n"
                          "4. Experimental results: [answer]]\n\n"
                          "5. Conclusions: [answer]"]
        prompt_string += ["Each one of the [answer] should have a length between 1 to 5 sentences."]
        prompt_string += ["Each one of the [answer] should be specific"]
        prompt_string += ["Here is the summary:"]
        self.prompt = self.prompt_formatting_GPT(prompt_string)
from auto_research.utils.inquiry import gpt
from auto_research.survey.paper_reader import paper
from auto_research.survey.prompter import prompt

class auto_survey():
    def __init__(self,api_key,model,paper_path,debug=False,mode="summarize_default"):
        self.gpt_instance=gpt(api_key, model=model, debug=debug)
        self.paper_path=paper_path
        self.paper_instance=paper(paper_path, model=model)
        self.paper_instance.read_pymupdf()
        self.prompt_instance=prompt()
        self.mode=mode
        self.output=None

    def run(self):
        if self.mode=="summarize_default":
            print(f"Begin analyzing the article located at {self.paper_path}")
            self.extraction()
            self.summary()
            print("The summary is:")
            print()
            print(self.output)
        elif self.mode=="explain_algorithm":
            self.extract_algorithm()
            self.explain_algorithm()


    def extract_algorithm(self):
        raw_text=self.paper_instance.first_n_pages(12)
        self.prompt_instance.extract_algorithm(raw_text)
        print(self.gpt_instance.ask(self.prompt_instance.prompt))
        self.paper_instance.extracted_information["algorithm"]=self.gpt_instance.ask(self.prompt_instance.prompt)

    def explain_algorithm(self):
        self.prompt_instance.explain_algorithm(self.paper_instance.first_n_pages(12),self.paper_instance.extracted_information["algorithm"])
        print(self.gpt_instance.ask(self.prompt_instance.prompt))

    def review(self):
        pass

    def extraction(self):
        self.extract_abstract()
        self.extract_introduction()
        self.ending_pages=self.paper_instance.extract_ending_pages(3)
        self.extract_discussion()
        self.extract_conclusion()

    def extract_abstract(self):
        print("---extracting abstract---")
        raw_text=self.paper_instance.first_n_pages(2)
        self.prompt_instance.extract_abstract(raw_text)
        self.paper_instance.extracted_information["abstract"]=self.gpt_instance.ask(self.prompt_instance.prompt)

    def extract_introduction(self):
        print("---extracting introduction---")
        raw_text=self.paper_instance.first_n_pages(5)
        self.prompt_instance.extract_introduction(raw_text)
        self.paper_instance.extracted_information["introduction"]=self.gpt_instance.ask(self.prompt_instance.prompt)

    def extract_discussion(self):
        print("---extracting discussion---")
        self.prompt_instance.extract_discussion(self.ending_pages)
        self.paper_instance.extracted_information["discussion"]=self.gpt_instance.ask(self.prompt_instance.prompt)

    def extract_conclusion(self):
        print("---extracting conclusion---")
        self.prompt_instance.extract_conclusion(self.ending_pages)
        self.paper_instance.extracted_information["conclusion"]=self.gpt_instance.ask(self.prompt_instance.prompt)

    def summary(self):
        print("---summarizing---")
        self.prompt_instance.summarize_default_computer_science(self.paper_instance.extracted_information["abstract"] , self.paper_instance.extracted_information["introduction"]
                                                                , self.paper_instance.extracted_information["discussion"] , self.paper_instance.extracted_information["conclusion"])
        self.output=self.gpt_instance.ask(self.prompt_instance.prompt)

    def explain(self):
        pass

    def findings(self):
        pass
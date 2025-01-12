from LLM_utils.prompter import PromptBase
from LLM_utils.inquiry import OpenAI_interface, extract_code

def base_prompt_list(research_topic_prompt_string) :
    prompt_string=[]
    prompt_string += [
        "A researcher is trying to search related articles for a given research topic. Your task is to analyze the description for the research topic and then provide a list of related keywords. The keywords are the keywords typed into a search engine for scholarly articles, such as Google Scholar."]
    prompt_string += ["Below is the description for the research topic:"]
    prompt_string += [research_topic_prompt_string]
    prompt_string += ["Your answer must be a Python list of strings."]
    prompt_string += [
        "For each keyword, there should also be the acronyms, full form of acronyms, synonyms, interchangeable terminologies, similar methods, similar topics, and paraphrases for the keyword, if applicable.  Ignore the difference between plural and singular forms and capitalized and decapitalized forms."]
    prompt_string += [
        "For example, an answer can be ['reinforcement learning and evolutionary computation', 'RL and EC', 'reinforcement learning for evolutionary computation', 'reinforcement learning with evolutionary computation', 'interaction betweeen reinforcement learning and evolutionary computation', 'reinforcement learning and evolutionary algorithms', 'reinforcement learning for evolutionary algorithms', ...]. Your answer should avoid the abbreviation sign and include the full list."]
    prompt_string += [
        "The keywords in the list should be ranked from the most relevant to the least relevant. Each keyword should be an academic terminologies suitable as the keyword for a search engine for academic articles."]
    prompt_string += ["Your answer must be only the Python list, no other text."]
    prompt_string += ["Here is the Python list:"]
    return prompt_string

def test_as_list(raw_response):
    extraction=extract_code(raw_response,mode="python_object")
    assert isinstance(extraction, list), f"The answer is {extraction} but it should be a list"
    return extraction


def suggest_keywords(user_prompt, model, api_key):
    OpenAI_instance=OpenAI_interface(api_key=api_key , model=model)
    prompt_list=base_prompt_list(user_prompt)
    prompt_formatted=PromptBase.list_to_formatted_OpenAI(prompt_list)
    response, _=OpenAI_instance.ask_with_test(prompt_formatted,test_as_list)
    return response


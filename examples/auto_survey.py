from auto_research.survey.core import AutoSurvey
from auto_research.utils.inquiry import check_and_read_key_file


key = check_and_read_key_file("../", "OpenAI")
if key == -1:
    key = "type_your_key_here_or_use_key.json"

sample_folder = "../auto_research/survey/sample_articles/"

file_list = [
    "A survey on evaluation of large language models.pdf",
    "BOHB Robust and Efficient Hyperparameter Optimization at Scale.pdf",
    "The Shaped Transformer Attention Models in the Infinite Depth-and-Width Limit.pdf",
    "Random Search for Hyper-Parameter Optimization.pdf",
    "MnasNet Platform-Aware Neural Architecture Search for Mobile.pdf",
    "Neural Fine-Tuning Search for Few-Shot Learning.pdf",
]

file_name = file_list[1]
file_path = sample_folder + file_name
auto_survey_instance = AutoSurvey(key, "gpt-4o-mini", file_path, False, "summarize_default")
auto_survey_instance.run()

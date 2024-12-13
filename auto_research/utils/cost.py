import tiktoken


class Calculator:
    # Pricing per 1M input tokens in USD for OpenAI models
    OpenAI_input_pricing = {
        "gpt-4o": 2.50,
        "gpt-4o-2024-11-20": 2.50,
        "gpt-4o-2024-08-06": 2.50,
        "gpt-4o-2024-05-13": 5.00,
        "gpt-4o-mini": 0.15,
        "gpt-4o-mini-2024-07-18": 0.15,
        "o1-preview": 15.00,
        "o1-preview-2024-09-12": 15.00,
        "o1-mini": 3.00,
        "o1-mini-2024-09-12": 3.00,
        "chatgpt-4o-latest": 5.00,
        "gpt-4-turbo": 10.00,
        "gpt-4-turbo-2024-04-09": 10.00,
        "gpt-4": 30.00,
        "gpt-4-32k": 60.00,
        "gpt-4-0125-preview": 10.00,
        "gpt-4-1106-preview": 10.00,
        "gpt-4-vision-preview": 10.00,
        "gpt-3.5-turbo-0125": 0.50,
        "gpt-3.5-turbo-instruct": 1.50,
        "gpt-3.5-turbo-1106": 1.00,
        "gpt-3.5-turbo-0613": 1.50,
        "gpt-3.5-turbo-16k-0613": 3.00,
        "gpt-3.5-turbo-0301": 1.50,
        "davinci-002": 2.00,
        "babbage-002": 0.40,
    }

    # Pricing per 1M output tokens in USD for OpenAI models
    OpenAI_output_pricing = {
        "gpt-4o": 10.00,
        "gpt-4o-2024-11-20": 10.00,
        "gpt-4o-2024-08-06": 10.00,
        "gpt-4o-2024-05-13": 15.00,
        "gpt-4o-mini": 0.60,
        "gpt-4o-mini-2024-07-18": 0.60,
        "o1-preview": 60.00,
        "o1-preview-2024-09-12": 60.00,
        "o1-mini": 12.00,
        "o1-mini-2024-09-12": 12.00,
        "chatgpt-4o-latest": 15.00,
        "gpt-4-turbo": 30.00,
        "gpt-4-turbo-2024-04-09": 30.00,
        "gpt-4": 60.00,
        "gpt-4-32k": 120.00,
        "gpt-4-0125-preview": 30.00,
        "gpt-4-1106-preview": 30.00,
        "gpt-4-vision-preview": 30.00,
        "gpt-3.5-turbo-0125": 1.50,
        "gpt-3.5-turbo-instruct": 2.00,
        "gpt-3.5-turbo-1106": 2.00,
        "gpt-3.5-turbo-0613": 2.00,
        "gpt-3.5-turbo-16k-0613": 4.00,
        "gpt-3.5-turbo-0301": 2.00,
        "davinci-002": 2.00,
        "babbage-002": 0.40,
    }

    def __init__(self, model, formatted_input_sequence=None, formatted_output_sequence=None):
        self.model = model
        self.formatted_input_sequence = formatted_input_sequence
        self.formatted_output_sequence = formatted_output_sequence
        self.input_token_length = None
        self.output_token_length = None

    def calculate_input_token_length_OpenAI(self):
        """Calculate the number of tokens used by a list of messages."""
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            print(
                "Warning: model not found for tokenization. Using cl100k_base encoding for cost "
                "calculation."
            )
            encoding = tiktoken.get_encoding("cl100k_base")

        tokens_per_message = 3
        tokens_per_name = 1

        num_tokens = 0
        for message in self.formatted_input_sequence:
            num_tokens += tokens_per_message
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":
                    num_tokens += tokens_per_name
        num_tokens += 3  # Every reply is primed with <|start|>assistant<|message|>
        return num_tokens

    def calculate_output_token_length_OpenAI(self):
        """
        Calculates the number of tokens in a given output sequence.

        Parameters:
            output_sequence (str): The text output generated by the model.
            model (str): The name of the model for tokenization. Default is "gpt-3.5-turbo".

        Returns:
            int: The number of tokens in the output sequence.
        """
        try:
            # Initialize tokenizer for the specific model
            tokenizer = tiktoken.encoding_for_model(self.model)
        except KeyError:
            print("Warning: Model not found. Using cl100k_base encoding as a fallback.")
            tokenizer = tiktoken.get_encoding("cl100k_base")

        # Tokenize the output sequence
        tokens = tokenizer.encode(self.formatted_output_sequence)

        # Return the token count
        return len(tokens)

    def calculate_cost_OpenAI(self):
        if self.formatted_input_sequence is not None:
            self.input_token_length = self.calculate_input_token_length_OpenAI()
            input_cost = self.input_token_length * self.OpenAI_input_pricing[self.model] / 1e6
        else:
            input_cost = 0
        if self.formatted_output_sequence is not None:
            self.output_token_length = self.calculate_output_token_length_OpenAI()
            output_cost = self.output_token_length * self.OpenAI_output_pricing[self.model] / 1e6
        else:
            output_cost = 0
        return input_cost + output_cost

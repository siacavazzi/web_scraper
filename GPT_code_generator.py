import openai
from key import key

openai.api_key = key

def get_completion(prompt, model="gpt-3.5-turbo-16k", temperature=0.2):
        messages = [{"role": "system", "content": prompt}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message["content"]


def check_HTML(html):
    resp = get_completion(get_HTML_check_prompt(html))
    return resp

def generate_code(html):
    code = get_completion(get_code_gen_prompt(html))
    local_vars = {"input_var": html, "result": None}
    try:
        exec(code, {}, local_vars)
        output = local_vars["result"]
    
    except:
        print("Invalid code")
         



def get_code_gen_prompt(HTML):
    return "Use the following template function to write code to extract the specifiied elements from this HTML:\n" + HTML + '''
def extract_info_from_html(html):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    """
    Your code here...
    Please only respond with code
    """

    return {
        "title": title, # the title of the event
        "start_date": start_date, # the starting date of the event
        "end_date": end_date, # the ending date of the event, may be the same as start_date
        "summary": summary, # summary of the event or any text describing the event.
        "event_img_url": event_img_url # an image url, if contained in the HTML
    }
output = extract_info_from_html(data) # do not modify this line

Please ONLY respond with your code and no other text

'''

def get_HTML_check_prompt(HTML):
    return f"""
Given the following HTML respond with a boolean (no other text or code) indicating if the HTML contains the following:
- A title of some kind
- A date

{HTML}
Respond ONLY with a boolean indicating if the conditions are met and no other text.

"""

# Prompt gpt to check HTML -> if true -> prompt GPT to generate code -> write code to file -> try to read the file -> if successful try to run function -> if successful on first attempt continue for all HTML items
                        # -> if false -> move to next HTML collection                       -> if fail delete the file and prompt to write code again
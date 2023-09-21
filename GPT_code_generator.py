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

def extract_contents(rep_elem):
    first_element_contents = str(rep_elem.content[0])
    code = generate_code(first_element_contents)
    events = []
    if code is not None:
        for element in rep_elem.content:
            print(element)
            events.append(execute_extraction_code(code, str(element)))
    return events


def check_HTML(html):
    resp = get_completion(get_HTML_check_prompt(html))
    return resp

def generate_code(html):
    print("Generating extraction code...")
    code = get_completion(get_code_gen_prompt(html))
    print(code)
    
    try:
    #if True:
        output = execute_extraction_code(code, html)
        
        print(output)
        if output is not None:
            return code
        else:
            return None
        
    except Exception as e:
        print(e)
        return None
         
def execute_extraction_code(code, html):
    local_vars = {"html": html, "output": None}
    try:
    #if True:
        exec(code, {}, local_vars)
        output = local_vars["output"]
    except Exception as e:
        output = str(e)

    return output




def get_code_gen_prompt(HTML):
    return "Use the following template function to write robust code WITH ERROR HANDLING to extract the specifiied elements from this HTML:\n" + HTML + '''
    Do not include the HTML itself in your code. Do not attempt to define the html variable. Only write your code in the specified section.
    Code template:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'lxml')
    """
    ONLY MODIFY THIS SECTION.
    """

    output = {
        "title": title, # the title of the event
        "start_date": start_date, # the starting date of the event
        "end_date": end_date, # the ending date of the event, may be the same as start_date
        "summary": summary, # summary of the event or any text describing the event.
        "event_img_url": event_img_url # an image url, if contained in the HTML
    }


Please ONLY respond with your code and no other text. Do not define the html variable or include the html in your code. This code is meant to be reusable for other html elements. Make sure to add error handling, as certain tags or elements might not exist.

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
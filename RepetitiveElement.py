from bs4 import BeautifulSoup, Tag
import re
import json

class RepetitiveElement:

    def __init__(self, ident, count ,content, source=None):
        self.content = list(content)
        self.count = count
        self.ident = ident
        self.source = source

    def __repr__(self):
        return f"<Identifier: {self.ident}, Elements present: {self.count}>"
    
    def debug(self):
        for element in self.content:
            #print(element)
            if element is not None:
                soup = BeautifulSoup(str(element), 'lxml')
                title = soup.find('h4').text.strip()
                print(title)

    # Writes the raw HTML of repetitive elements to a file within the raw_html folder
    def write_elements(self):
        name = "".join([c for c in self.source if re.match(r'\w', c)]) # consider adding date gere
        file_path = f"raw_html/{name}.html"
        with open(file_path, "x") as f:
            formatted_text = []
            for item in self.content:
                formatted_text.append(str(item))

            json.dump(formatted_text, f)
    

class ElementContainer:

    def __init__(self, url):
        self.elements = []
        self.url = url

    def add(self, ident, count, content):
        new_element = RepetitiveElement(ident, count, content, self.url)
        for element in self.elements:
            #for element in elements.content:
            if new_element.ident == element.ident:
                element.content = element.content + new_element.content
                element.count += new_element.count
                return
        
        self.elements.append(new_element)
    
    def print(self):
        for element in self.elements:
            print("======= ELEMENT ========")
            print(element.content)

    def get_most_likely_content(self):
        self.elements.sort(key = lambda x: x.count, reverse=True)
        return self.elements[0]

        
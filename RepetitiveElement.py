
class RepetitiveElement:

    def __init__(self, ident, count ,content):
        self.content = list(content)
        self.count = count
        self.ident = ident

    def __repr__(self):
        return f"<Identifier: {self.ident}, Elements present: {self.count}>"
    

class ElementContainer:

    def __init__(self):
        self.elements = []

    def add(self, ident, count, content):
        new_element = RepetitiveElement(ident, count, content)
        for element in self.elements:
            #for element in elements.content:
            if new_element.ident == element.ident:
                element.content = element.content + new_element.content
                element.count += new_element.count
                return
        
        self.elements.append(new_element)
    
    def print(self):
        for element in self.elements:
            print(element)

    def get_most_likely_content(self):
        self.elements.sort(key = lambda x: x.count, reverse=True)
        return self.elements[0]

        
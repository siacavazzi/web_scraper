from bs4 import BeautifulSoup, Tag
from collections import defaultdict
from RepetitiveElement import ElementContainer

class ProcessHTML:
    min_like_values = 5

    def __init__(self):
        self.rep_elems = ElementContainer()

    def reset(self):
        self.rep_elems.content = []

    def get_items(self, html):
        soup = BeautifulSoup(html, 'lxml')
        self.traverse_tree(soup.body, soup)
        return self.rep_elems

    def get_shared_values_at_same_level(self, element, soup):
        value_counts = defaultdict(int)
        for child in element.children:
            if isinstance(child, Tag):
                #values = set()
                classes = child.get('class', [])
                for c in classes:
                    value_counts[c] += 1
                #values.update(classes)

                itemType = child.get('itemtype')
                if itemType:
                    value_counts[itemType] += 1

        output = []
        for value in value_counts.keys():
            count = value_counts[value]
            if count > self.min_like_values:
                items = soup.find_all(class_=value)
                if len(items) == 0:
                    items = soup.find_all(attrs={"itemtype": value})
                #rep_elem = RepetitiveElement(items, count, value)
                self.rep_elems.add(value, count ,items)
                #output.append(rep_elem)

        return output
    

    def traverse_tree(self, element, soup):
        shared_values = self.get_shared_values_at_same_level(element, soup)
        if shared_values:
            for value in shared_values:
                self.rep_elems.append(value)
        for child in element.children:
            if isinstance(child, Tag):
                self.traverse_tree(child, soup)



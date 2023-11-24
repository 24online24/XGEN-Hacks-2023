import re

def preprocess(documents):
    for doc in documents:
        content = re.sub(r'\s+', ' ', doc.page_content)
        content = content.replace('\n', '').replace('\r', '')
        content = re.sub(r'^[0-9]+\s', '', content, flags=re.MULTILINE)
        
        if content.strip():
            doc.page_content = content
        else:
            documents.remove(doc)
    
    
    
    
    
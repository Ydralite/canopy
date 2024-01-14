import json
from pathlib import Path
from typing import Callable, Dict, List, Optional, Union

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader
import matplotlib.patches as patches
import matplotlib.pyplot as plt

class JSONLoader(BaseLoader):
    def __init__(
        self,
        file_path: Union[str, Path],
        content_key: Optional[str] = None,
        ):
        self.file_path = Path(file_path).resolve()
        self._content_key = content_key
    
    def create_documents(self, processed_data):
        documents = []
        for item in processed_data:
            content = ''.join(item)
            document = Document(page_content=content, metadata={})
            documents.append(document)
        return documents
    
    def process_item(self, item, prefix=""):
        if isinstance(item, dict):
            result = []
            for key, value in item.items():
                new_prefix = f"{prefix}.{key}" if prefix else key
                result.extend(self.process_item(value, new_prefix))
            return result
        elif isinstance(item, list):
            result = []
            for value in item:
                result.extend(self.process_item(value, prefix))
            return result
        else:
            return [f"{prefix}: {item}"]

    def process_json(self,data):
        if isinstance(data, list):
            processed_data = []
            for item in data:
                processed_data.extend(self.process_item(item))
            return processed_data
        elif isinstance(data, dict):
            return self.process_item(data)
        else:
            return []

    def load(self) -> List[Document]:
        """Load and return documents from the JSON file."""

        docs=[]
        with open(self.file_path, 'r') as json_file:
            try:
                data = json.load(json_file)
                processed_json = self.process_json(data)
                docs = self.create_documents(processed_json)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format in the file.")
        return docs


class JSONDocLoader(BaseLoader):
    def __init__(
        self,
        file,
        content_key: Optional[str] = None,
        ):
        self.file = file
        self._content_key = content_key
        
    def load(self) -> List[Document]:
        """Load and return documents from the JSON file."""

        # Load JSON file
        data = self.file
        
        docs = []
        for page in data['hierarchies']:
            filename = page['filename']
            level_1 = page['children_1']
            level_2 = page['children_2']
            level_3 = page['children_3']
            topic = page['topic']
            elements = page['elements']
            style = page['style']
            composition = page['composition']
            text= str(page['content'])
            metadata = dict(
                filename = filename,
                level_1 = level_1,
                level_2 = level_2,
                level_3 = level_3,
                composition = composition,
                style = style,
                elements = elements,
                topic = topic)
        
            docs.append(Document(page_content=text, metadata=metadata))
        return docs



def simplify_class_name(class_name):
    """
    Simplify the class name by keeping only the part after the last dot.
    """
    return class_name.split('.')[-1].replace('AppCompat','') if '.' in class_name else class_name

def add_prettier_rectangles(ax, children):
    """
    Recursive function to add prettier rectangles (representing UI elements) to the plot.
    This version simplifies the class names and adjusts styling.
    """
    for child in children:
        # Extract bounds and calculate width and height
        bounds = child.get('bounds', [0, 0, 0, 0])
        x0, y0, x1, y1 = bounds
        width = x1 - x0
        height = y1 - y0

        # Create a rectangle
        rect = patches.Rectangle((x0, y0), width, height, linewidth=1, edgecolor='blue', facecolor='skyblue', alpha=0.3)
        ax.add_patch(rect)

        # Add label with simplified class name
        class_name = simplify_class_name(child.get('class', 'Unknown'))
        ax.text(x0 + width/2, y0 + height/2, class_name, ha='center', va='center', fontsize=8, color='black')

        # Recursively add children of this node
        if 'children' in child:
            add_prettier_rectangles(ax, child['children'])

def show_ui(ui_data):
    # Create a figure and axis with an aspect ratio of 1080x1920
    fig, ax = plt.subplots(1, figsize=(5, 10))  # Adjusted for the aspect ratio of 1080x1920
    
    # Add the rectangles
    add_prettier_rectangles(ax, ui_data['children'])
    
    # Set limits and labels
    screen_bounds = ui_data.get('bounds', [0, 0, 1080, 1920])
    ax.set_xlim(0, screen_bounds[2])
    ax.set_ylim(screen_bounds[3], 0)
    plt.axis('off')
    
    # Show the plot
    plt.show()


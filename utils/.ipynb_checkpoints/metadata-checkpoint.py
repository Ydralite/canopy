from langchain.chains.query_constructor.base import AttributeInfo
from langchain.retrievers.self_query.base import SelfQueryRetriever

def info():
    metadata_field_info = [
        AttributeInfo(
            name="filename",
            description="The name of the file.",
            type="string",
        ),
        AttributeInfo(
            name="children_1",
            description="The number of disaggregations on the first level. These are direct descendants of the root element. In an Android app, this could be top-level layout elements like a LinearLayout or RelativeLayout.",
            type="integer",
        ),
        AttributeInfo(
            name="children_2",
            description="The number of disaggregations on the second level. Represents a further nesting of UI components. For instance, within a LinearLayout in an Android app, you might have TextViews, Buttons, or even another nested layout",
            type="integer",
        ),
        AttributeInfo(
            name="children_3", description="The number of disaggregations on the third level. These represent most granular UI components", type="integer"
        ),
        AttributeInfo(
            name="style", description="An interpretation of the style (aesthetics and overall look and feel of the UI)", type="string"
        ),
        AttributeInfo(
            name="composition", description="An interpretation of the layout structures that match the kind of information or interaction you want to facilitate", type="string"
        ),
        AttributeInfo(
            name="elements", description="An interpretation of the most prominant components", type="string"
        ),
        AttributeInfo(
            name="topic", description="The design topic of the file", type="string"
        ),
    ]
    document_content_description = 'View Hierarchy Tree Structure in a form of a Json file, that contains the main elements present in a user interface'
    return metadata_field_info, document_content_description
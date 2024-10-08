from flask import Flask, request
from flask_cors import CORS
from models.feed import Source, Story
import controller
import persistence
import urllib
app = Flask(__name__)
CORS(app)


def source_to_json(s: Source):
    return {
        "id": s.id,
        "url": s.url,
        "name": s.name
    }

def story_to_json(st: Story):
    parsedURL = urllib.parse.urlparse(st.source.url)
    baseURL = f"{parsedURL.scheme}://{parsedURL.netloc}"
    return {
        "id": st.id,
        "url": st.url,
        "title": st.title,
        "date": st.date,
        "rank": st.rank,
        "summary": st.summary,
        "source": st.source.name,
        "base_domain": baseURL
    }

@app.post("/sources")
def add_source():
    content = request.json
    s = controller.addSource(content["url"], content["name"])
    return source_to_json(s)

@app.post("/sources/delete")
def del_source():
    content = request.json
    s = controller.delSource(content["id"])
    return {
        "code": 200
    }

@app.get("/sources")
def get_sources():
    print("Get sources request received")
    myList = []
    for s in persistence.sourceList:
        myList.append(source_to_json(s))
    return {
        "sources": myList
    }

@app.get("/stories")
def fetch_all_stories():
    page_number = int(request.args.get("page_number"))
    search_query = request.args.get("search_query", default="")
    print("Fetching all stories...")
    if page_number == 0: 
        controller.getAllStories()
    myList = []
    print("Categorizing stories...")
    categories = controller.getCategorizedStories(page_number, search_query)
    print("Generating labels for categories...")
    labels = controller.getCategoryLabels(categories)
    for idx, c in enumerate(categories):
        clist = []
        stories = c[1]

        # Sort stories by rank value, bigger is better
        stories.sort(key=(lambda x: x.rank), reverse=True)
        for s in stories:
            clist.append(story_to_json(s))
        myList.append(clist)
    return {
        "stories": myList,
        "labels": labels
    }

    # for st in controller.allStories:
    #     myList.append(story_to_json(st))
    # return {
    #     "stories": myList
    # }

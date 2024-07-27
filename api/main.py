import os
import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from functions.url import url_parser
from functions.lexical_analysis import lexical_analysis
from functions.webfeatures_ananlysis import get_features
from functions.deep_analysis import analyze_link

load_dotenv()

CHECK_TYPES = {
    "quick": pickle.load(open(os.path.join("models", "quick.pkl"), "rb")),
    "moderate": pickle.load(open(os.path.join("models", "moderate.pkl"), "rb")),
}

path = ChromeDriverManager().install()

# Define the class encoding for the model's output. This is used to convert the model's output to human-readable form.
CLASS_ENCODING = {
    0: "safe",
    1: "unsafe"
}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"code": 200, "message": "Server is live"}


@app.get("/check/{type}")
async def check_url(type: str, url: str):
    if not url:
        return {"code": 400, "message": "URL not provided"}

    validate = url_parser(url)
    if validate is None:
        return {"code": 400, "message": "Invalid URL"}

    if type == "quick":
        features = lexical_analysis(url)
        prediction = CHECK_TYPES[type].predict([features])

        return {"code": 200, "message": "URL checked", "result": CLASS_ENCODING[prediction[0]]}

    if type == "moderate":
        lexical_features = lexical_analysis(url)
        features = get_features(url, path)
        if features == 0:
            type = "quick"
            total_features = lexical_features
        else:
            total_features = lexical_features + features
        prediction = CHECK_TYPES[type].predict([total_features])
        return {"code": 200, "message": "URL checked", "result": CLASS_ENCODING[prediction[0]]}

    if type == "deep":
        result = analyze_link(url)
        if result == 0:
            return {"code": 400, "message": "URL could not be checked, please try again"}

        return {"code": 200, "message": "URL checked", "result": result}

from flask import Flask, Response, request
from flask import jsonify

import logging

from github import GithubREST
from response_handler import ResponseHandler
from query_params import QueryParams, DEFAULT_PAGE, DEFAULT_PER_PAGE

dev_mode = True
app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(asctime)s %(message)s",
)


@app.route("/")
def health_check() -> dict:
    return {
        "data": "Hello, welcome to Sleuth backend interview task. Please see instructions in README.md"
    }


@app.route("/health/github")
def github_api_root_example() -> dict:
    return GithubREST().get("/")


@app.route("/github/repos/<path:repository>/pulls", methods=["GET"])
def github_repository_pull_requests(repository: str):
    page = request.args.get("page", DEFAULT_PAGE)
    per_page = request.args.get("per_page", DEFAULT_PER_PAGE)

    #git defaults to return only 'open' prs. included this line should the query be for ['open', 'closed', 'all'] state(s) instead of exclusively 'open'
    #this is set to 'open' by default as well
    pr_state = {'state':request.args.get("state", 'open')}

    query_params = QueryParams(page=page, per_page=per_page)
    query_params.__dict__.update(pr_state)

    request_url = f"/repos/{repository}/pulls"

    res = GithubREST().get(request_url, query_params.__dict__)

    return {"additional_pages": ResponseHandler.additional_pages(res['links']),
           "data": ResponseHandler.get_pr_info(repository, res)}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

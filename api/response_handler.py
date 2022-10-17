import re

from github import GithubREST

class ResponseHandler:

    @staticmethod
    def get_pr_title(res: dict) -> str:
        return res['title']

    @staticmethod
    def get_pr_author(res: dict) -> str:
        return res['user']['login']

    @staticmethod
    def get_pr_head_sha(res: dict) -> str:
        return res['head']['sha']

    @staticmethod
    def get_pr_number(res: dict) -> int:
        return res['number']

    @staticmethod
    def get_pr_last_updated(res: dict) -> str:
        return res['updated_at']

    @staticmethod
    def pr_commit_count(repository: str, pr: int) -> int:
        request_url = f"/repos/{repository}/pulls/{pr}/commits"
        res = GithubREST().get(request_url)
        return len(res['data'])

    @staticmethod
    def additional_pages(links: dict) -> str:
        if not links:
            return "All PRs in this repository have been returned in this query."
        else:
            #string manipulation to get the count of other pages
            page_count = int(re.search('page=(.*)&per_page=', links['last']['url']).group(1))
            return f"There are an additional {page_count-1} page(s) of PRs for this repository."

    @classmethod
    def get_pr_info(cls, repository, res: dict) -> dict:
        output = {}
        for item in res['data']:
            prNumber = cls.get_pr_number(item)
            output.update({
                f"Pull Request#{prNumber}":
                    {
                        'PR Title': cls.get_pr_title(item),
                        'PR Author': cls.get_pr_author(item),
                        'Commits on PR': cls.pr_commit_count(repository, prNumber),
                        'Head SHA': cls.get_pr_head_sha(item),
                        'Last Update': cls.get_pr_last_updated(item)
                    }
                })
        return output

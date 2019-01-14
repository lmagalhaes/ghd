from github import Github
from github.GithubException import UnknownObjectException
import requests
import click


### github related
available_teams_list = {
    'admin': ['admin', 'admin'],
    'engineering': ['engineering', 'push'],
    'tech champions': ['tech champions', 'admin'],
}


def list_companies_repo(company):
    repos = company.get_repos(type='private')
    for repo in repos:
        print(len(repo))


def create_repo(company, repo_name):
    try:
        repo = company.get_repo(repo_name)
    except UnknownObjectException as exc:
        repo = company.create_repo(repo_name, private=True, auto_init=True)
        teams = company.get_teams()
        add_teams_to_repo(repo=repo, teams=teams)
    return repo


def add_teams_to_repo(repo, teams):
    all_teams = list(filter(lambda team: team.name.lower() in available_teams_list.keys(), teams))
    teams_permission_list = get_teams_permission(all_teams)

    for item in teams_permission_list:
        team = item.get('team')
        team.add_to_repos(repo)
        team.set_repo_permission(repo, permission=item.get('permission'))


def get_teams_permission(teams):
    return [
        {
            'team': team,
            'permission': available_teams_list.get(team.name.lower())[1]
        }
        for team in teams if team.name.lower() in available_teams_list.keys()
    ]


### codeclimate related
def get_codeclimate_organization():
    response = requests.get('https://api.codeclimate.com/v1/orgs', headers={
        'Accept': 'application/vnd.api+json',
        'Authorization': 'Token token={}'.format(open('.cc_token').read().strip())
    })

    return response.json()


def add_repo_to_codeclimate(organization, repo):
    payload = {
        "data": {
            "type": "repos",
            "attributes": {
                "url": repo.svn_url
            }
        }
    }
    response = requests.post(
        'https://api.codeclimate.com/v1/orgs/{}/repos'.format(organization['data'][0]['id']),
        headers={
            'Accept': 'application/vnd.api+json',
            'Authorization': 'Token token={}'.format(open('.cc_token').read().strip()),
            'Content-Type': 'application/vnd.api+json'
        }, json=payload)

    import pprint
    pprint.pprint(response.json())


def setup_github_repository(repository_name, github_token):
    git = Github(github_token)
    company = git.get_organization("theiconic")

    repository = create_repo(company, repository_name)

    master = repository.get_branch('master')
    master.edit_protection(
        dismiss_stale_reviews=True,
        required_approving_review_count=1
    )

    return repository


def setup_codeclimate_repository(repository):
    cc_org = get_codeclimate_organization()
    add_repo_to_codeclimate(cc_org, repository)


@click.command()
@click.argument('repository-name')
@click.option('--github-token', envvar='GITHUB_TOKEN')
@click.option('--enable-code-climate', is_flag=True)
@click.option('--code-climate-token', envvar='CODE_CLIMATE_TOKEN')
def run(repository_name, enable_code_climate, github_token, code_climate_token):
    """
    Manage github repositories using command line
    """
    repository = setup_github_repository(repository_name, github_token)

    if enable_code_climate:
        setup_codeclimate_repository(repository, code_climate_token)


if __name__ == '__main__':
    run()

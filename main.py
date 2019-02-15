from github import Github
from github.GithubException import UnknownObjectException
import click
from ghd.clients import CodeClimate

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


def setup_codeclimate_repository(code_climate_token, repository):
    client = CodeClimate(api_token=code_climate_token)

    organizations = client.get_organizations()
    repository_info = client.add_private_repository(
        organization_id=organizations[0]['id'],
        repository_url=repository.svn_url
    )


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
        setup_codeclimate_repository(code_climate_token, repository)


if __name__ == '__main__':
    run()

from github import Github
from github.GithubException import UnknownObjectException


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
        repo = company.create_repo(repo_name, private=True)
    return repo


def add_teams_to_repo(company, repo):
    teams = list(filter(lambda team: team.name.lower() in available_teams_list.keys(), company.get_teams()))
    teams_permission_list = [
        create_team_permission(*team) for team in available_teams_list.values()
    ]
    print(teams)
    print(teams_permission_list)
    # # add_teams_to_repo(repo)
    #
    # for team in teams:
    #     team.add_to_repos(repo)
    #     team.set_repo_permission(repo, permission=team_permissions[team.name.lower()])


def create_team_permission(team_name, permission):
    return {
        'name': team_name,
        'permission': permission
    }


def run():
    repo_name = "test_repo"
    git = Github(open('.ghd_token').read().strip())
    company = git.get_organization("theiconic")

    #new_repo = create_repo(company, repo_name)
    new_repo = company.get_repo(repo_name)
    add_teams_to_repo(company, new_repo)


if __name__ == '__main__':
    run()

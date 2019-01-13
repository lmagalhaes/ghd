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


def run():
    repo_name = "test_repo"
    git = Github(open('.ghd_token').read().strip())
    company = git.get_organization("theiconic")

    repo = create_repo(company, repo_name)
    master = repo.get_branch('master')

    master.edit_protection(
        dismiss_stale_reviews=True,
        required_approving_review_count=1
    )


if __name__ == '__main__':
    run()

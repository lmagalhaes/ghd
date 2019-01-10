from github import Github
from github.GithubException import UnknownObjectException


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


def run():
    allowed_team = [
        'tech champions',
        'admin',
        'engineering'
    ]

    team_permissions = {
        'tech champions': 'admin',
        'admin': 'admin',
        'engineering': 'push'
    }

    repo_name = "test_repo"
    git = Github(open('.ghd_token').read().strip())
    company = git.get_organization("theiconic")

    repo = create_repo(company, repo_name)
    # repo = git.get_repo("lmagalhaes/teste_repo")
    # user = git.get_user('pcelta')
    # repo.add_to_collaborators(user, permission='admin')

    teams = list(filter(lambda team: team.name.lower() in allowed_team, company.get_teams()))

    for team in teams:
        team.add_to_repos(repo)

    # print(list(team))
    # brands_reco = company.get_repo("brands-recommendation")
    # collaboratos = brands_reco.get_teams()
    #
    # for collaborator in collaboratos:
    #     print(collaborator)
    # brands_reco.get_te

    # test_repo = git.get_repo('teste_repo')
    # test_repo.add_to_collaborator()


if __name__ == '__main__':
    run()

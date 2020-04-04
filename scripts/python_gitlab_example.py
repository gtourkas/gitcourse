#!/usr/bin/env python3

import sys, os, urllib3, argparse, pdb
# Silence the irritating insecure warnings. I'm not insecure you're insecure!
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Add the location of python-gitlab to the path so we can import it
repo_top = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
python_gitlab_dir = os.path.join(repo_top, "external/python-gitlab")
sys.path.append(python_gitlab_dir)
import gitlab

def getArgs():
    parser = argparse.ArgumentParser(description='Three examples of using the REST API. 1st: Summarize all open MRs, 2nd: Post note to existing MR, 3rd: Create new issue in project.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument( "authkey", type=str, help="Personal access token for authentication with GitLab. Create one at https://gitlab.com/profile/personal_access_tokens" )
    parser.add_argument( "project", type=str,default="gitschooldude/hello",help="Path to GitLab project in the form <namespace>/<project>")
    parser.add_argument( "--url",  help="Gitlab URL.", default='https://gitlab.com/')
    return parser, parser.parse_args()

class PythonGitlabExample():
    def __init__(self, url, authkey, project):
        # Parse command line arguments
        self.url = url
        self.authkey = authkey
        self.project_name = project
        self.project = None
        self.mrs = None  # list of all merge requests
        # Create python-gitlab server instance
        server = gitlab.Gitlab(self.url, myargs.authkey, api_version=4, ssl_verify=False)
        # Get an instance of the project and store it off
        self.project = server.projects.get(self.project_name)

    def list_mrs(self):
        # Get all MRs in the project and print some info about them
        mrs = self.project.mergerequests.list(all=True, state='opened')
        print("All Merge Requests in project: %s" % self.project_name)
        for mr in mrs:
            print("  Merge Requst ID: %d, Title: %s" % (mr.iid, mr.title))
            print('    Labels: ' + ','.join(mr.labels))
            closes = [str(c.iid) for c in mr.closes_issues()]
            print('    Closes Issues: ' + ','.join(closes))
            print('    Number of notes in discussion: ' + str(len(mr.notes.list())))

    def post_note(self):
        mr_id   = int(input("Which MR id do you want to post a message to (integer id)?: "))
        note = input("Input message: ")
        mr = self.project.mergerequests.get(mr_id)  # Get the MR
        mr.notes.create({'body': note})             # Post the note to the MR

    def create_issue(self):
        title   = input("New Issue Title: ")
        description = input("New Issue Description: ")
        issue = self.project.issues.create({'title': title, 'description': description})

    def run(self):
        if input("Example 1: Summarize all open merge requests.    Press enter to run, any other key to skip: ") == '': self.list_mrs()
        if input("Example 2: Post note to existing merge request.  Press enter to run, any other key to skip: ") == '': self.post_note()
        if input("Example 3: Create new issue in project.          Press enter to run, any other key to skip: ") == '': self.create_issue()

if __name__ == '__main__':
    myParser, myargs = getArgs()
    sys.exit(PythonGitlabExample(url=myargs.url, authkey=myargs.authkey,
        project=myargs.project).run())

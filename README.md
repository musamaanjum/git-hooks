# git-hooks

[![Build Status](https://travis-ci.com/musamaanjum/git-hooks.svg?branch=master)](https://travis-ci.com/musamaanjum/git-hooks)

## Sources
**tabs_to_spaces.py** - Contains the code which converts tabs to spaces

**pre-commit** - Contains bash script which'll call the tabs to spaces conversion script

**README.md** - This file.

**test_files** - Test files which can be used while development

## Usage
Copy the following files to your repository's .git/hooks folder:
* pre-commit
* tabs_to_spaces.py

Just after copying, this hook will be functional. 

### Hands on:
For example: I've changed a file test-file/git.txt. 

I'll add its changes:
`git add test-file/git.txt`

Now I'll commit:
`git commit`

If tabs are found in the staged file which is test-file/git.txt file in this case, the commit will abort and following message will appear:
`(X, ' Line(s) replaced tabs with spaces')`
`Aborting...`
`Please stage the changed files and try again!`

Stage the file again and commit again:
`git add test-file/git.txt`
`git commit`

Thus the tabs have been converted to spaces.

## Caution
* If the pre-commit hook rejects the commit and asks to stage the file again, please do so. If this file isn't staged, next time the pre-commit hook will pass.
* If `output.magic` file is found, it can be deleted.
* Use at your own risk. More testing on real scenerios is needed.

## TO-DOs
* Disable debug prints with command line option
* Do more testing on real time scenerios


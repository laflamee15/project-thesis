# fix_email.py
import os

def fix_commit(commit):
    if commit.committer_email == b'emmandotcom@gmail.com':
        commit.committer_name = b'laflamee15'
        commit.committer_email = b'204869950+laflamee15@users.noreply.github.com'
    if commit.author_email == b'emmandotcom@gmail.com':
        commit.author_name = b'laflamee15'
        commit.author_email = b'204869950+laflamee15@users.noreply.github.com'

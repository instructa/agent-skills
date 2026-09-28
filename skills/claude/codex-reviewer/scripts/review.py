#!/usr/bin/env python3
"""Run one read-only Codex review; the calling Claude agent owns all corrections."""
import argparse
import datetime
import json
import shutil
import signal
import subprocess
import sys
from pathlib import Path


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, required=True)
    parser.add_argument('--prompt', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--model', default='gpt-6-astra')
    parser.add_argument('--effort', default='high')
    args = parser.parse_args()
    project, prompt, output = (p.expanduser().resolve() for p in
                               (args.project, args.prompt, args.output))
    if not project.is_dir():
        parser.error('project must be an existing directory')
    try:
        brief = prompt.read_text(encoding='utf-8')
    except OSError as error:
        parser.error(str(error))
    if not brief.strip():
        parser.error('prompt must not be empty')
    codex = shutil.which('codex')
    if not codex:
        parser.error('Codex CLI is missing from PATH; install and authenticate it first')
    try:
        version = subprocess.run([codex, '--version'], capture_output=True,
                                 text=True, timeout=15, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError) as error:
        parser.error('Cannot run Codex CLI: ' + str(error))
    git = shutil.which('git')
    is_git = bool(git and subprocess.run(
        [git, '-C', str(project), 'rev-parse', '--is-inside-work-tree'],
        capture_output=True, text=True).stdout.strip() == 'true')
    try:
        output.mkdir(parents=True, exist_ok=False)
    except FileExistsError:
        parser.error('output directory already exists; choose a fresh directory')
    (output / 'prompt.md').write_text(brief, encoding='utf-8')
    command = [codex, 'exec', '--model', args.model, '-c',
               'model_reasoning_effort=' + json.dumps(args.effort),
               '--sandbox', 'read-only', '--json', '--output-last-message',
               str(output / 'review.md')]
    if not is_git:
        command.append('--skip-git-repo-check')
    command.append('-')
    record = dict(started_at=now(), project=str(project), command=command,
                  codex_version=version, requested_model=args.model,
                  requested_effort=args.effort, reported_model='unknown',
                  reported_effort='unknown', state='running', exit_code=None)

    def save():
        (output / 'run.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')

    save()
    child = None
    interrupted = False

    def stop(signum, frame):
        nonlocal interrupted
        interrupted = True
        if child and child.poll() is None:
            child.terminate()
            try:
                child.wait(timeout=5)
            except subprocess.TimeoutExpired:
                child.kill()

    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, stop)
    try:
        with (output / 'prompt.md').open('rb') as stdin, \
                (output / 'events.jsonl').open('wb') as stdout, \
                (output / 'stderr.log').open('wb') as stderr:
            child = subprocess.Popen(command, cwd=project, stdin=stdin,
                                     stdout=stdout, stderr=stderr)
            code = child.wait()
        completed = False
        session_ids = []
        with (output / 'events.jsonl').open(encoding='utf-8', errors='replace') as events:
            for line in events:
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(event, dict):
                    continue
                completed |= event.get('type') == 'turn.completed'
                if event.get('type') == 'thread.started' and event.get('thread_id'):
                    session_ids.append(event['thread_id'])
        final = output / 'review.md'
        has_review = final.is_file() and bool(final.read_text(encoding='utf-8').strip())
        record.update(exit_code=code, session_ids=session_ids,
                      state='interrupted' if interrupted else
                      'completed' if code == 0 and completed and has_review else 'failed')
    except (OSError, subprocess.SubprocessError) as error:
        record.update(state='failed', error=str(error))
    record['finished_at'] = now()
    save()
    print(json.dumps({'state': record['state'], 'output': str(output),
                      'exit_code': record['exit_code']}))
    return 0 if record['state'] == 'completed' else 1


if __name__ == '__main__':
    sys.exit(main())

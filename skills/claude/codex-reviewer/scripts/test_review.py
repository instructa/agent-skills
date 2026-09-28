"""Runner contract tests with a fake Codex process; no model/API calls."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

RUNNER = Path(__file__).with_name('review.py')


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='review runner ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / 'project with spaces $literal'
        self.project.mkdir()
        self.prompt = self.root / 'brief.md'
        self.prompt.write_text('Review the assigned feature. Preserve $literal and `text`.')
        self.output = self.root / 'review 01'
        binary = self.root / 'codex'
        binary.write_text('#!' + sys.executable + '\n' + '''
import json, os, pathlib, sys
if '--version' in sys.argv:
    print('codex-cli fixture')
    sys.exit(0)
pathlib.Path(os.environ['CAPTURE']).write_text(json.dumps({
    'argv':sys.argv[1:], 'cwd':os.getcwd(), 'stdin':sys.stdin.read()}))
print(json.dumps({'type':'thread.started','thread_id':'fixture-session'}))
mode=os.environ.get('FIXTURE_MODE','success')
if mode=='failure':
    print('fixture failure',file=sys.stderr)
    print(json.dumps({'type':'turn.failed','error':{'message':'fixture failure'}}))
    sys.exit(9)
if mode!='empty':
    pathlib.Path(sys.argv[sys.argv.index('--output-last-message')+1]).write_text('No supported findings. Unchecked items remain unverified.')
print(json.dumps({'type':'turn.completed','usage':{'input_tokens':10,'output_tokens':5}}))
''')
        binary.chmod(0o755)
        self.env = {**os.environ, 'PATH':str(self.root)+os.pathsep+os.environ['PATH'],
                    'CAPTURE':str(self.root/'capture.json')}

    def run_review(self, *extra):
        return subprocess.run([sys.executable, str(RUNNER), '--project', str(self.project),
                               '--prompt', str(self.prompt), '--output', str(self.output),
                               *extra], env=self.env, capture_output=True, text=True)

    def test_non_git_paths_prompt_and_read_only(self):
        result = self.run_review()
        self.assertEqual(result.returncode, 0, result.stderr)
        capture = json.loads((self.root/'capture.json').read_text())
        self.assertEqual(Path(capture['cwd']).resolve(), self.project.resolve())
        self.assertEqual(capture['stdin'], self.prompt.read_text())
        args = capture['argv']
        self.assertIn('--skip-git-repo-check', args)
        self.assertEqual(args[args.index('--sandbox')+1], 'read-only')
        self.assertEqual(args[args.index('--model')+1], 'gpt-6-astra')
        self.assertEqual(args[args.index('-c')+1], 'model_reasoning_effort="high"')
        record = json.loads((self.output/'run.json').read_text())
        self.assertEqual(record['session_ids'], ['fixture-session'])
        self.assertEqual(record['reported_model'], 'unknown')
        self.assertIn('"input_tokens": 10', (self.output/'events.jsonl').read_text())

    def test_git_project_and_explicit_model_override(self):
        subprocess.run(['git','init','--quiet',str(self.project)], check=True)
        result = self.run_review('--model','explicit-model','--effort','medium')
        self.assertEqual(result.returncode, 0, result.stderr)
        args = json.loads((self.root/'capture.json').read_text())['argv']
        self.assertNotIn('--skip-git-repo-check', args)
        self.assertEqual(args[args.index('--model')+1], 'explicit-model')
        self.assertEqual(args[args.index('-c')+1], 'model_reasoning_effort="medium"')

    def test_failure_preserves_native_exit_and_logs(self):
        self.env['FIXTURE_MODE'] = 'failure'
        self.assertNotEqual(self.run_review().returncode, 0)
        record = json.loads((self.output/'run.json').read_text())
        self.assertEqual((record['state'], record['exit_code']), ('failed', 9))
        self.assertIn('fixture failure', (self.output/'stderr.log').read_text())

    def test_empty_final_is_not_success(self):
        self.env['FIXTURE_MODE'] = 'empty'
        self.assertNotEqual(self.run_review().returncode, 0)
        self.assertEqual(json.loads((self.output/'run.json').read_text())['state'], 'failed')

    def test_existing_evidence_cannot_be_overwritten(self):
        self.assertEqual(self.run_review().returncode, 0)
        original = (self.output/'run.json').read_bytes()
        self.assertNotEqual(self.run_review().returncode, 0)
        self.assertEqual((self.output/'run.json').read_bytes(), original)


if __name__ == '__main__':
    unittest.main()

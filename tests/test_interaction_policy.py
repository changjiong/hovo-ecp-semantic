from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class InteractionPolicyTests(unittest.TestCase):
    def test_skill_has_bounded_clarification_budget(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('最多 1 轮', text)
        self.assertIn('最多 5 个', text)
        self.assertIn('Workshop', text)

    def test_uncertainty_states_are_complete(self):
        text=(ROOT/'references/interaction-policy.md').read_text(encoding='utf-8')
        for state in ['CONFIRMED','INFERRED','ASSUMED','OPEN','BLOCKED']:
            self.assertIn(state,text)

    def test_local_blocking_is_explicit(self):
        text=(ROOT/'references/interaction-policy.md').read_text(encoding='utf-8')
        self.assertIn('Asset Dependency Graph', text)
        self.assertIn('禁止把一个 `BLOCKED` 输入升级成整个任务停止', text)

    def test_workshop_is_opt_in(self):
        text=(ROOT/'references/interaction-policy.md').read_text(encoding='utf-8')
        self.assertIn('仅当用户明确要求', text)

if __name__ == '__main__':
    unittest.main()

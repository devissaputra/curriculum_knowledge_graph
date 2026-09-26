"""Reproduce the labeled worked example; this is not an empirical study."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from curriculum_knowledge_graph import core
outputs={'coverage: 3 assessed / 4 outcomes': 3/4}
result={'kind':'illustrative_calculation','note':'Illustrative relation-count arithmetic, not a real curriculum.','outputs':outputs}
(ROOT/'results/review_examples.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))

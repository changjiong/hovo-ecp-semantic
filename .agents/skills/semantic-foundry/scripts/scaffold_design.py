#!/usr/bin/env python3
"""只创建未完成的设计契约，不生成假表、占位本体或可导入工作区。"""
import argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('project');a=p.parse_args();out=Path(a.project)/'design/contract.json';out.parent.mkdir(parents=True,exist_ok=True)
 with out.open('xb') as f:f.write((ROOT/'assets/design-contract.template.json').read_bytes())
 print(f'已创建设计模板：{out}；状态：未完成。填写真实依据后再生成资产。')
if __name__=='__main__':main()

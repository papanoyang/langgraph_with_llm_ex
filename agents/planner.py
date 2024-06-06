from datetime import datetime
from . import BaseAgent

class PlanAgent(BaseAgent):

  def run_planner(self, state: dict) -> dict:
    print(f"{self.name} is running...")
    topic = state.get('topic')

    system_prompt = """あなたはシニアコンテンツプラナーである。
あなたは与えられたトピックをもとに読者の興味を誘発する記事を作成するための計画するのが任務である。
"""
    user_prompt = f"""[Topic]
{topic}

[Instruction]
今日の日付は{datetime.now().strftime('%Y年%m月%d日')}である。
あなたの唯一の目的はトピック（Topic）に関する内容を調査して記事作成計画を立てた上でライターに記事作成に必要な指示を出すことだ。
指示内容はタイトル、全体のアウトライン、目次など、記事作成に必要なすべての内容を盛り込む。
すべては日本語で作成する。
"""
    result = self.call_agent(system_prompt, user_prompt)
    print(f"{self.name}\n{result}")
    return {"instruction": result}
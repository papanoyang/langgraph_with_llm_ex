import json5 as json
from . import BaseAgent

sample_json = """
{
  "revision_message": レビュアーへのメッセージ,
  "article": 修正された記事
}
"""
class WriteAgent(BaseAgent):

  def run_writer(self, state: dict):
    topic = state.get('topic')
    instruction = state.get('instruction')

    system_prompt = """あなたはシニアコンテンツライターである。
あなたの任務はプラナーからの指示をもとに記事を作成することだ。
"""
    user_prompt = f"""あなたの唯一の目的はTopicについてプラナーが指示（Instruction）した記事を作成する計画をもとに記事をよく書くことである。
結果はよく作成されたマークダウン形式で返す。

[Topic]
{topic}

[Instruction]
{instruction}
"""
    result = self.call_model(system_prompt, user_prompt)
    print(f"{self.name}\n{result}")
    return {"article": result}
  
  def run_reviser(self, state: dict):
    article = state.get('article')
    review_message = state.get('review_message')

    system_prompt = """あなたはシニアコンテンツライターである。
あなたの任務はプラナーからの指示をもとに記事を作成することだ。
また、レビュアーからのフィードバックに対して内容を検討し、記事を修正する。
"""
    user_prompt = f"""[Article]
{article}

[Review message]
{review_message}

[Instruction]
あなたの唯一の目的はあなたが作成した記事（Article）に対してレビュアーからのフィードバック(Review message)の内容を確認し、記事を修正することである。
修正したあとは次のサンプルのようなJSON形式で返す。
{sample_json}
"""
    result = self.call_model(system_prompt, user_prompt, response_format='json')
    data = json.loads(result)
    print(f"{self.name}\n{json.dumps(data, indent=2, ensure_ascii=False)}")
    return {"article": data.get('article'), "revision_message": data.get('revision_message')}
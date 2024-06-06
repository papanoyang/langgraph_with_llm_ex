from . import BaseAgent

class ReviewAgent(BaseAgent):
    
  def run_reviewer(self, state: dict):
    instruction = state.get("instruction")
    article = state.get("article")
    revision_message = state.get("revision_message")

    system_prompt = """あなたは記事のレビュアーである。
次の内容をチェックし、ライターへフィードバックする。
- 記事がプラナーの計画通りになっているか
- 記事の内容が法律的に問題ないか
- 記事の内容が倫理的に健全であるか
"""
    revise_prompt = f"""[Revision message]
ライターはあなたのフィードバックに対して修正を行った。
次はライターからのメッセージである。

{revision_message}
"""
    user_prompt = f"""あなたの唯一の目的は与えられたプラナーの企画（Instruction）とライターが作成した記事（Article）をもとにレビューを実施することである。
与えられた記事をレビューし、修正が必要な場合、修正に必要なコメントを返してライターが適切に修正できるようにする。
もし、記事が完璧でそのまま掲示可能な場合、修正は必要ないのでNoneのみを返す。

[Instruction]
{instruction}

[Article]
{article}

{ revise_prompt if revision_message else ""}
"""
    result = self.call_model(system_prompt, user_prompt)
    print(f"{self.name}\n{result}")
    if 'None' in result:
      return {"review_message": None}
    return {"review_message": result}
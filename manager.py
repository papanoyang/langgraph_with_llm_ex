import json5 as json
from datetime import datetime
from langgraph.graph import StateGraph, END

from agents import PlanAgent, WriteAgent, ReviewAgent
from memory import AgentState

class ArticleTeamManager:
  def __init__(self) -> None:
    pass

  def run_workflow(self, topic: str):
    print('Team Manager Start')
    planner = PlanAgent(name='Planner')
    writer = WriteAgent(name='Writer')
    reviewer = ReviewAgent(name='Reviewer')

    workflow = StateGraph(AgentState)

    workflow.add_node('planner', planner.run_planner)
    workflow.add_node('writer', writer.run_writer)
    workflow.add_node('reviewer', reviewer.run_reviewer)
    workflow.add_node('reviser', writer.run_reviser)

    workflow.add_edge('planner', 'writer')
    workflow.add_edge('writer', 'reviewer')
    workflow.add_edge('reviser', 'reviewer')
    workflow.add_conditional_edges(
      'reviewer',
      (lambda x: "accept" if x['review_message'] is None else "revise"),
      {"accept": END, "revise": 'reviser'}
    )

    workflow.set_entry_point('planner')

    chain = workflow.compile()

    result = chain.invoke({"topic": topic})

    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.md"
    with open(file_name, 'w') as f:
      f.write(result['article'])
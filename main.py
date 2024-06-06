from dotenv import load_dotenv
from manager import ArticleTeamManager

def main():
    manager = ArticleTeamManager()
    manager.run_workflow(topic="生成型AIの概要と活用方法について")

if __name__ == "__main__":
    load_dotenv()
    main()